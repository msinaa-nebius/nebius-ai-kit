"""Pure configuration helpers. Own only the named Nebius handlers, not settings."""
import copy
import hashlib
import json
import shlex

LABEL = "Nebius: retrieve workspace memory"
FILES = (".codex/hooks.json", ".claude/settings.json")
# No absolute laptop paths, Git, shell interpolation of filenames, or dependencies.
LAUNCH = ('from pathlib import Path; import runpy; p=Path.cwd().resolve(); '
          'r=next((d for d in (p,*p.parents) if (d/".nebius-kit/install.json").is_file()),None); '
          'assert r is not None,"Open the installed Nebius workspace"; '
          'runpy.run_path(str(r/".nebius-kit/memory_hook.py"),run_name="__main__")')
COMMAND = "python3 -c " + shlex.quote(LAUNCH)


def parse(data):
    obj = json.loads(data) if data else {}
    if not isinstance(obj, dict) or not isinstance(obj.get("hooks", {}), dict):
        raise ValueError("Hook settings must be a JSON object with an object hooks field")
    for groups in obj.get("hooks", {}).values():
        if not isinstance(groups, list):
            raise ValueError("Invalid hook groups; preserve settings and review manually")
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                raise ValueError("Invalid hook group; preserve settings and review manually")
            if any(not isinstance(h, dict) for h in group["hooks"]):
                raise ValueError("Invalid hook handler")
    return obj


def owned(obj):
    result = {}
    for event, groups in obj.get("hooks", {}).items():
        for group in groups:
            handlers = [h for h in group["hooks"] if h.get("statusMessage") == LABEL]
            if handlers:
                part = dict(group, hooks=handlers)
                result.setdefault(event, []).append(part)
    return result


def fingerprint(data):
    return hashlib.sha256(json.dumps(owned(parse(data)), sort_keys=True).encode()).hexdigest()


def merge(data, codex=False):
    obj = copy.deepcopy(parse(data))
    hooks = obj.setdefault("hooks", {})
    for event, groups in list(hooks.items()):
        keep = []
        for group in groups:
            remaining = [h for h in group["hooks"] if h.get("statusMessage") != LABEL]
            if remaining:
                keep.append(dict(group, hooks=remaining))
        hooks[event] = keep
    for event in ("SessionStart", "UserPromptSubmit"):
        handler = {"type": "command", "command": COMMAND, "timeout": 5, "statusMessage": LABEL}
        if codex:
            handler["additionalContextLimit"] = 0
        group = {"hooks": [handler]}
        if event == "SessionStart":
            group["matcher"] = "startup|resume|clear|compact"
        hooks.setdefault(event, []).append(group)
    if data and obj == parse(data):
        return data
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
