#!/usr/bin/env python3
"""Claude Code PreToolUse guard (dev-process template). Copied to .claude/hooks/ with guard_config.json.

Blocks tool calls that would:
  1. Read or print stored credentials from a shell (OS credential stores, env dumps of keys).
  2. Put a secret-looking value into a command or a file (API keys, tokens, Bearer values, private keys).
     Values containing a fake marker (FAKE, REDACTED, EXAMPLE) are allowed, for test placeholders.
  3. Use the OS credential library in any Python file other than the app's one secret-store module.

All patterns live in guard_config.json, so a project adapts the guard without editing code.
Exit code 2 blocks the call, and stderr is fed back to Claude as the reason.
Exit code 0 lets the normal permission flow continue.
Self-test:  python .claude/hooks/guard_secrets.py --self-test
"""

import json
import re
import sys
from pathlib import Path

CONFIG = json.loads((Path(__file__).with_name("guard_config.json")).read_text(encoding="utf-8"))

OWNER = CONFIG.get("owner", "the owner")
SECRET_STORE_SUFFIX = CONFIG.get("secret_store_suffix") or None
FAKE = re.compile(CONFIG.get("fake_marker", "FAKE"))
SECRET_VALUES = [(re.compile(p), what) for p, what in CONFIG["secret_values"] + CONFIG.get("project_patterns", [])]
SHELL_ACCESS = [(re.compile(p), what) for p, what in CONFIG["shell_credential_access"]]
STORE_CODE = re.compile(CONFIG["secret_store_code"])

SHELL_TOOLS = {"Bash", "PowerShell"}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

BLOCK_SUFFIX = (
    " Credentials must never enter the Claude Code transcript or the repo. Use the app's secret store through "
    f"normal app code paths, use obvious placeholders containing FAKE in tests, or ask {OWNER} to run this step."
)


def strings_in(obj):
    """Yield every string value nested in the tool input."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings_in(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings_in(v)


def check(payload):
    """Return a block reason, or None to allow."""
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    texts = list(strings_in(tool_input))

    for text in texts:
        for pattern, what in SECRET_VALUES:
            for m in pattern.finditer(text):
                if not FAKE.search(m.group(0)):
                    return f"Blocked: this {tool} call contains what looks like {what}."

    if tool in SHELL_TOOLS:
        command = tool_input.get("command", "") or ""
        for pattern, what in SHELL_ACCESS:
            if pattern.search(command):
                return f"Blocked: this shell command {what}."

    if tool in WRITE_TOOLS and SECRET_STORE_SUFFIX:
        path = (tool_input.get("file_path") or tool_input.get("notebook_path") or "").replace("\\", "/")
        if path.endswith(".py") and not path.endswith(SECRET_STORE_SUFFIX):
            for text in texts:
                if STORE_CODE.search(text):
                    return (
                        f"Blocked: the credential library may only be used in {SECRET_STORE_SUFFIX}; "
                        f"'{path or 'this file'}' must call that module instead."
                    )
    return None


def self_test():
    cases = [(c["tool"], c["input"], c["block"]) for c in CONFIG.get("self_test", [])]
    # Key-shaped values are built from pieces so this file never holds one.
    real_looking = "sk-ant-" + "api03-" + "a" * 40
    fake = "sk-ant-" + "FAKE-" + "a" * 30
    cases += [
        ("Write", {"file_path": "tests/fixtures/x.json", "content": real_looking}, True),
        ("Write", {"file_path": "tests/fixtures/x.json", "content": fake}, False),
        ("Write", {"file_path": "x.txt", "content": "gh" + "p_" + "A" * 36}, True),
        ("Bash", {"command": "curl -H 'Authorization: Bearer " + "abcdefghij" * 3 + "' https://example.org"}, True),
    ]
    ok = True
    for tool, tool_input, should in cases:
        should_block = SECRET_STORE_SUFFIX is not None if should == "if_secret_store" else bool(should)
        blocked = check({"tool_name": tool, "tool_input": tool_input}) is not None
        ok &= blocked == should_block
        status = "ok " if blocked == should_block else "FAIL"
        print(f"[{status}] {tool}: expected {'block' if should_block else 'allow'}, got {'block' if blocked else 'allow'}")
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # malformed input: don't break the session
    reason = check(payload)
    if reason:
        print(reason + BLOCK_SUFFIX, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
