#!/usr/bin/env python3
"""Manage BMP Stock Council roster entries."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER = SKILL_DIR / "references" / "council_roster.json"
DEFAULT_MEMBER_DIR = SKILL_DIR / "references" / "council_members"
MEMBER_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_member_id(member_id: str) -> None:
    if not MEMBER_ID_RE.match(member_id):
        raise SystemExit("member id must use lowercase letters, digits, and hyphens only")


def profile_template(member_id: str, display_name: str) -> str:
    return f"""# {display_name}

Member id: {member_id}

## Role

Describe this member's investing lens in one short paragraph.

## Primary Filters

- Filter one.
- Filter two.
- Filter three.

## Default Skepticism

- What this lens tends to penalize.
- What evidence makes it cautious.

## Price Behavior

- How this lens thinks about valuation, downside, and margin of safety.

## Special Questions

- Question this member should always ask.

## Red Flags

- Red flag one.
- Red flag two.

## Output Emphasis

- What this subagent should make especially clear in its JSON output.
"""


def find_member(roster: dict, member_id: str) -> dict | None:
    for member in roster.get("members", []):
        if member.get("id") == member_id:
            return member
    return None


def handle_list(args: argparse.Namespace) -> int:
    roster = read_json(args.roster)
    for member in roster.get("members", []):
        status = "enabled" if member.get("enabled", True) else "disabled"
        print(f"{member.get('id')}\t{status}\t{member.get('display_name')}\t{member.get('profile')}")
    return 0


def handle_add(args: argparse.Namespace) -> int:
    validate_member_id(args.member_id)
    roster = read_json(args.roster)
    if find_member(roster, args.member_id):
        raise SystemExit(f"member already exists in roster: {args.member_id}")
    display_name = args.display_name or f"{args.member_id.replace('-', ' ').title()} Lens"
    profile_rel = args.profile or f"references/council_members/{args.member_id}.md"
    profile_path = (SKILL_DIR / profile_rel).resolve() if not Path(profile_rel).is_absolute() else Path(profile_rel)
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    if not profile_path.exists() or args.overwrite_profile:
        profile_path.write_text(profile_template(args.member_id, display_name), encoding="utf-8")
    roster.setdefault("members", []).append(
        {
            "id": args.member_id,
            "display_name": display_name,
            "profile": profile_rel,
            "enabled": not args.disabled,
        }
    )
    write_json(args.roster, roster)
    print(profile_path)
    return 0


def handle_set_enabled(args: argparse.Namespace) -> int:
    roster = read_json(args.roster)
    member = find_member(roster, args.member_id)
    if not member:
        raise SystemExit(f"member not found: {args.member_id}")
    member["enabled"] = args.enabled
    write_json(args.roster, roster)
    print(f"{args.member_id}: {'enabled' if args.enabled else 'disabled'}")
    return 0


def handle_remove(args: argparse.Namespace) -> int:
    roster = read_json(args.roster)
    before = len(roster.get("members", []))
    roster["members"] = [member for member in roster.get("members", []) if member.get("id") != args.member_id]
    if len(roster["members"]) == before:
        raise SystemExit(f"member not found: {args.member_id}")
    write_json(args.roster, roster)
    print(f"removed {args.member_id} from roster")
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER, help="Roster JSON path")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage BMP Stock Council members.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_cmd = subparsers.add_parser("list", help="List council members")
    add_common(list_cmd)
    list_cmd.set_defaults(func=handle_list)

    add_cmd = subparsers.add_parser("add", help="Add a council member and profile template")
    add_common(add_cmd)
    add_cmd.add_argument("member_id")
    add_cmd.add_argument("--display-name")
    add_cmd.add_argument("--profile", help="Profile path, default references/council_members/<id>.md")
    add_cmd.add_argument("--disabled", action="store_true", help="Add member disabled")
    add_cmd.add_argument("--overwrite-profile", action="store_true", help="Overwrite profile file if it exists")
    add_cmd.set_defaults(func=handle_add)

    enable_cmd = subparsers.add_parser("enable", help="Enable a council member")
    add_common(enable_cmd)
    enable_cmd.add_argument("member_id")
    enable_cmd.set_defaults(func=handle_set_enabled, enabled=True)

    disable_cmd = subparsers.add_parser("disable", help="Disable a council member")
    add_common(disable_cmd)
    disable_cmd.add_argument("member_id")
    disable_cmd.set_defaults(func=handle_set_enabled, enabled=False)

    remove_cmd = subparsers.add_parser("remove", help="Remove a council member from roster")
    add_common(remove_cmd)
    remove_cmd.add_argument("member_id")
    remove_cmd.set_defaults(func=handle_remove)

    args = parser.parse_args()
    args.roster = args.roster.expanduser().resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
