#!/usr/bin/env python3
"""Build a Researcher brief from council member profile markdown files."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER = SKILL_DIR / "references" / "council_roster.json"
DEFAULT_PROFILES_DIR = SKILL_DIR / "references" / "council_members"

QUESTION_RE = re.compile(r"\?\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$")

CATEGORY_PATTERNS = {
    "business_model_and_unit_economics": re.compile(
        r"business|revenue|customer|product|unit economic|cash flow|owner earnings|simple|category|story",
        re.IGNORECASE,
    ),
    "market_runway_and_growth": re.compile(
        r"market|runway|growth|tam|share|saturation|industry|fast grower|stalwart|slow grower",
        re.IGNORECASE,
    ),
    "moat_competition_and_disruption": re.compile(
        r"moat|competition|competitor|switching|pricing power|brand|scale|network|disruption|substitution|low-cost",
        re.IGNORECASE,
    ),
    "management_incentives_and_capital_allocation": re.compile(
        r"management|manager|ceo|board|incentive|compensation|capital allocation|buyback|dividend|acquisition|candor|skin",
        re.IGNORECASE,
    ),
    "financial_quality_and_accounting": re.compile(
        r"financial|margin|roe|roic|debt|leverage|inventory|earnings|accounting|ebitda|cash conversion|free cash|capex",
        re.IGNORECASE,
    ),
    "valuation_and_price_inputs": re.compile(
        r"price|valuation|margin of safety|intrinsic|earnings power|peg|p/e|cheap|yield|opportunity cost",
        re.IGNORECASE,
    ),
    "risk_negative_evidence_and_kill_conditions": re.compile(
        r"risk|red flag|fail|lose money|kill|wrong|deteriorate|fragile|survive|permanent|zero|too tough",
        re.IGNORECASE,
    ),
    "fieldwork_scuttlebutt_and_external_checks": re.compile(
        r"scuttlebutt|store|customer|supplier|distributor|ex-employee|expert|review|app ranking|foot traffic|observable",
        re.IGNORECASE,
    ),
    "behavioral_process_and_psychology": re.compile(
        r"psycholog|bias|fomo|social proof|temperament|environment|inner scorecard|ego|rushing|process",
        re.IGNORECASE,
    ),
    "ownership_dilution_and_share_count": re.compile(
        r"owner|insider|ownership|share count|dilution|repurchase|13f|13d|13g|clone",
        re.IGNORECASE,
    ),
}

BMP_ITEMS = {
    "B1": "B1_large_growing_market",
    "B2": "B2_low_market_share",
    "B3": "B3_moat",
    "B BONUS": "B_bonus_disruption_shield",
    "BBONUS": "B_bonus_disruption_shield",
    "M1": "M1_owner_mindset",
    "M2": "M2_value_drivers",
    "P1": "P1_price",
}

BMP_ITEM_LABELS = {
    "B1_large_growing_market": "B1 Large And Growing Market",
    "B2_low_market_share": "B2 Low Market Share",
    "B3_moat": "B3 Sustainable Moat",
    "B_bonus_disruption_shield": "B Bonus Disruption Shield",
    "M1_owner_mindset": "M1 Owner Mindset",
    "M2_value_drivers": "M2 Value Creation",
    "P1_price": "P1 Earnings Yield At Least 5 Percent",
}

PLAYBOOK_FIELD_PATTERNS = [
    ("how_lens_thinks", re.compile(r"^how\b.*\bthinks?\b.*question:?$", re.IGNORECASE)),
    ("evidence_demands", re.compile(r"^evidence\b.*\bdemands?\b|^evidence they would demand", re.IGNORECASE)),
    ("yes_standard", re.compile(r"^what makes\b.*\bsay\s+`?yes`?|^what would make them say yes", re.IGNORECASE)),
    ("no_standard", re.compile(r"^what makes\b.*\bsay\s+`?no`?|^what would make them say no", re.IGNORECASE)),
    ("kill_condition", re.compile(r"^kill condition", re.IGNORECASE)),
    ("improvement_condition", re.compile(r"^improvement condition", re.IGNORECASE)),
    ("distinctive_questions", re.compile(r"^distinctive questions", re.IGNORECASE)),
    ("source_basis", re.compile(r"^source basis", re.IGNORECASE)),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def roster_profiles(roster_path: Path) -> dict[str, dict[str, Any]]:
    roster = load_json(roster_path)
    profiles: dict[str, dict[str, Any]] = {}
    for item in roster.get("members", []):
        member_id = str(item.get("id", "")).strip()
        profile = str(item.get("profile", "")).strip()
        if not member_id or not profile:
            continue
        path = Path(profile)
        if not path.is_absolute():
            path = SKILL_DIR / path
        profiles[member_id] = {
            "id": member_id,
            "display_name": item.get("display_name") or member_id,
            "enabled": bool(item.get("enabled", True)),
            "profile_path": str(path),
        }
    return profiles


def profile_files(profiles_dir: Path, roster: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    by_path = {Path(item["profile_path"]).resolve(): dict(item) for item in roster.values()}
    for path in sorted(profiles_dir.glob("*.md")):
        resolved = path.resolve()
        if resolved not in by_path:
            by_path[resolved] = {
                "id": path.stem,
                "display_name": path.stem.title(),
                "enabled": False,
                "profile_path": str(path),
            }
    return [by_path[path] for path in sorted(by_path)]


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_bmp_item(title: str) -> str:
    title = clean_text(re.sub(r"`", "", title))
    upper = title.upper()
    for prefix, item_id in BMP_ITEMS.items():
        if upper.startswith(prefix + " ") or upper == prefix:
            return item_id
    if upper.startswith("B-BONUS") or upper.startswith("B BONUS"):
        return "B_bonus_disruption_shield"
    return ""


def normalize_playbook_field(title: str) -> str:
    normalized = clean_text(title).rstrip(":")
    for field, pattern in PLAYBOOK_FIELD_PATTERNS:
        if pattern.search(normalized):
            return field
    return ""


def append_field(playbook: dict[str, dict[str, list[str]]], item_id: str, field: str, text: str) -> None:
    text = clean_text(text)
    if not item_id or not field or not text or text in {"---"}:
        return
    playbook.setdefault(item_id, {key: [] for key, _ in PLAYBOOK_FIELD_PATTERNS})
    playbook[item_id].setdefault(field, [])
    playbook[item_id][field].append(text)


def extract_bmp_playbook(text: str) -> dict[str, dict[str, list[str]]]:
    playbook: dict[str, dict[str, list[str]]] = {}
    in_playbook = False
    current_item = ""
    current_field = ""

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = clean_text(heading_match.group(2))
            if level == 2:
                in_playbook = title.lower() == "bmp checklist playbook"
                current_item = ""
                current_field = ""
                continue
            if in_playbook and level == 3:
                current_item = normalize_bmp_item(title)
                current_field = ""
                if current_item:
                    playbook.setdefault(current_item, {key: [] for key, _ in PLAYBOOK_FIELD_PATTERNS})
                continue
            if in_playbook and level >= 4:
                current_field = normalize_playbook_field(title)
                continue
            continue

        if not in_playbook or not current_item or not stripped:
            continue

        label_field = normalize_playbook_field(stripped)
        if label_field and stripped.endswith(":"):
            current_field = label_field
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            append_field(playbook, current_item, current_field, bullet_match.group(1))
            continue

        append_field(playbook, current_item, current_field, stripped)

    return playbook


def extract_profile(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    headings: list[str] = []
    questions: list[dict[str, str]] = []
    research_bullets: list[dict[str, str]] = []
    current_heading = ""
    role_lines: list[str] = []
    capture_role = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading_match = HEADING_RE.match(line)
        if heading_match:
            current_heading = clean_text(heading_match.group(2))
            headings.append(current_heading)
            capture_role = current_heading.lower() in {"role", "core identity", "core directive", "core directives"}
            continue
        if capture_role and line.strip() and not line.lstrip().startswith(("-", "*", "#")):
            role_lines.append(clean_text(line))
        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            bullet = clean_text(bullet_match.group(1))
            if QUESTION_RE.search(bullet):
                questions.append({"heading": current_heading, "question": bullet})
            if re.search(
                r"evidence|research|source|filing|customer|supplier|competitor|financial|management|price|valuation|risk|question|check",
                bullet,
                re.IGNORECASE,
            ):
                research_bullets.append({"heading": current_heading, "need": bullet})
        elif QUESTION_RE.search(line.strip()):
            questions.append({"heading": current_heading, "question": clean_text(line)})

    combined_needs = [item["question"] for item in questions] + [item["need"] for item in research_bullets]
    categories: dict[str, list[str]] = defaultdict(list)
    for need in combined_needs:
        for category, pattern in CATEGORY_PATTERNS.items():
            if pattern.search(need):
                categories[category].append(need)

    return {
        "headings": headings,
        "style_summary": " ".join(role_lines[:3])[:1000],
        "bmp_playbook": extract_bmp_playbook(text),
        "question_count": len(questions),
        "questions": questions,
        "research_need_count": len(research_bullets),
        "research_needs": research_bullets,
        "categorized_needs": {key: values[:30] for key, values in sorted(categories.items())},
    }


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Council Research Brief: {payload['ticker']}",
        "",
        f"- Company: {payload.get('company') or ''}",
        f"- Analysis date: {payload['analysis_date']}",
        f"- Profiles read: {len(payload['members'])}",
        "",
        "## Researcher Use",
        "",
        "Read this before local source-library review, public filing review, public market-data checks, and fresh web research. Use it to shape the evidence inventory, coverage matrix, missing-evidence queue, and follow-up searches. Do not treat this as analysis; it is a research demand map.",
        "",
        "## Cross-Council Research Demand Map",
        "",
    ]
    for category, items in payload.get("combined_categories", {}).items():
        lines.append(f"### {category.replace('_', ' ').title()}")
        if not items:
            lines.append("- No extracted needs.")
        for item in items[:25]:
            lines.append(f"- {item['member']}: {item['need']}")
        lines.append("")

    lines.append("## BMP Checklist Playbook Evidence Map")
    lines.append("")
    lines.append("Use this map to make sure every checklist item has evidence for each council lens before council work begins.")
    lines.append("")
    for item_id, label in BMP_ITEM_LABELS.items():
        lines.append(f"### {label}")
        entries = payload.get("combined_bmp_playbook", {}).get(item_id, [])
        if not entries:
            lines.append("- No extracted playbook demands.")
            lines.append("")
            continue
        for entry in entries:
            member = entry["member"]
            evidence = "; ".join(entry.get("evidence_demands", [])[:4]) or "No explicit evidence demand extracted."
            kill = "; ".join(entry.get("kill_condition", [])[:2]) or "No explicit kill condition extracted."
            questions = "; ".join(entry.get("distinctive_questions", [])[:3]) or "No distinctive questions extracted."
            lines.append(f"- {member} evidence: {evidence}")
            lines.append(f"  - Kill condition: {kill}")
            lines.append(f"  - Distinctive questions: {questions}")
        lines.append("")

    lines.append("## Member Profiles")
    lines.append("")
    for member in payload["members"]:
        lines.append(f"### {member['display_name']} (`{member['id']}`)")
        lines.append("")
        lines.append(f"- Enabled in roster: {member['enabled']}")
        lines.append(f"- Profile: `{member['profile_path']}`")
        if member.get("style_summary"):
            lines.append(f"- Style summary: {member['style_summary']}")
        extracted_playbook = sorted(member.get("bmp_playbook", {}).keys())
        if extracted_playbook:
            labels = [BMP_ITEM_LABELS.get(item_id, item_id) for item_id in extracted_playbook]
            lines.append(f"- BMP playbook items extracted: {', '.join(labels)}")
        lines.append(f"- Extracted questions: {member['question_count']}")
        lines.append(f"- Extracted research needs: {member['research_need_count']}")
        lines.append("")
        for question in member.get("questions", [])[:30]:
            lines.append(f"- {question['heading']}: {question['question']}")
        if member.get("question_count", 0) > 30:
            lines.append(f"- ... {member['question_count'] - 30} more questions in JSON.")
        lines.append("")
    return "\n".join(lines)


def update_research_packet(run_dir: Path, payload: dict[str, Any]) -> None:
    path = run_dir / "research" / "research_packet.json"
    if not path.exists():
        return
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    packet["council_research_brief_status"] = {
        "checked": True,
        "profiles_read": [member["profile_path"] for member in payload["members"]],
        "brief_json": "research/council_research_brief.json",
        "brief_md": "research/council_research_brief.md",
        "key_member_needs": sorted(payload.get("combined_categories", {}).keys()),
        "bmp_playbook_items": sorted(payload.get("combined_bmp_playbook", {}).keys()),
        "notes": "Built before source gathering from council member markdown profiles.",
    }
    write_json(path, packet)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Researcher brief from council member markdown profiles.")
    parser.add_argument("run_dir", help="BMP run directory")
    parser.add_argument("--ticker", default="", help="Ticker for output context")
    parser.add_argument("--company", default="", help="Company for output context")
    parser.add_argument("--date", default=date.today().isoformat(), help="Analysis date")
    parser.add_argument("--roster", default=str(DEFAULT_ROSTER), help="Council roster JSON path")
    parser.add_argument("--profiles-dir", default=str(DEFAULT_PROFILES_DIR), help="Council profile markdown directory")
    parser.add_argument("--enabled-only", action="store_true", help="Only include enabled roster members")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    roster_path = Path(args.roster).expanduser().resolve()
    profiles_dir = Path(args.profiles_dir).expanduser().resolve()
    roster = roster_profiles(roster_path)
    members = []
    combined_categories: dict[str, list[dict[str, str]]] = defaultdict(list)
    combined_bmp_playbook: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for info in profile_files(profiles_dir, roster):
        if args.enabled_only and not info["enabled"]:
            continue
        path = Path(info["profile_path"]).expanduser().resolve()
        extracted = extract_profile(path)
        member = {**info, **extracted, "profile_path": str(path)}
        members.append(member)
        for category, needs in extracted["categorized_needs"].items():
            for need in needs:
                combined_categories[category].append({"member": member["id"], "need": need})
        for item_id, fields in extracted.get("bmp_playbook", {}).items():
            combined_bmp_playbook[item_id].append({"member": member["id"], **fields})

    payload = {
        "status": "built",
        "ticker": args.ticker,
        "company": args.company,
        "analysis_date": args.date,
        "source": {
            "roster": str(roster_path),
            "profiles_dir": str(profiles_dir),
            "enabled_only": args.enabled_only,
        },
        "members": members,
        "combined_categories": {key: values for key, values in sorted(combined_categories.items())},
        "combined_bmp_playbook": {key: values for key, values in sorted(combined_bmp_playbook.items())},
        "researcher_instructions": [
            "Use this artifact before source-library inventory and fresh research.",
            "Use combined_bmp_playbook as the checklist-by-checklist evidence demand map.",
            "Map every material council playbook demand to coverage_matrix gaps or evidence IDs.",
            "Convert material missing items into research_coverage_matrix gaps or missing_evidence_requests.",
            "Do not treat profile questions as evidence; they are evidence demand signals.",
        ],
    }

    output_json = run_dir / "research" / "council_research_brief.json"
    output_md = run_dir / "research" / "council_research_brief.md"
    write_json(output_json, payload)
    output_md.write_text(build_markdown(payload), encoding="utf-8")
    update_research_packet(run_dir, payload)
    print(output_json)
    print(output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
