# Council Profiles

Council members are modular subagents. The roster is the source of truth:

- `references/council_roster.json` lists enabled members.
- `references/council_members/<member_id>.md` stores the detailed investing lens for each member.
- `scripts/scaffold_bmp_run.py` creates one `council/<member_id>.json` output per enabled member.
- `scripts/validate_bmp_artifacts.py` validates the member files listed in the run manifest.

Do not impersonate real investors, fabricate quotes, or claim private thoughts. Profiles describe analytical lenses inspired by public investing principles.

## Add A Council Member

1. Choose a stable lowercase id using letters, digits, and hyphens only, for example `terry-smith`.
2. Create `references/council_members/<id>.md` using the template below.
3. Add an object to `references/council_roster.json`:

```json
{
  "id": "terry-smith",
  "display_name": "Terry Smith Lens",
  "profile": "references/council_members/terry-smith.md",
  "enabled": true
}
```

4. Run the skill validator and scaffold a test run.

Helper command:

```bash
python3 scripts/manage_council_roster.py add terry-smith --display-name "Terry Smith Lens"
```

## Disable Or Delete A Council Member

To temporarily remove a member from future runs, set `enabled` to `false` in `references/council_roster.json`.

To delete permanently, remove the roster entry and optionally delete that member's profile file. Existing historical run folders remain valid because their `manifest.json` stores the member list used at creation time.

Helper commands:

```bash
python3 scripts/manage_council_roster.py disable guy
python3 scripts/manage_council_roster.py enable guy
python3 scripts/manage_council_roster.py remove guy
```

## Member Profile Template

```markdown
# Display Name

Member id: member-id

## Role

One short paragraph describing the investing lens.

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
```

## Cross-Council Conflict Rules

- The Reporter must preserve disagreements and explain what fact would resolve each major dispute.
- A member can reject a stock for a reason others tolerate.
- A member can support a special situation even when long-term compounder quality is imperfect, if that profile allows it.
- Price consensus must explain which member assumptions received weight and why.
