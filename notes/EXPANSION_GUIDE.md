# StoryForge Adventure Expansion Guide

A repeatable process for expanding short StoryForge adventures (~40–70 passages, one ending) into full branching gamebooks (~200–300 passages, multiple path-gated endings). Based on the methodology used to expand *Tide of the Leviathan* from 64 to 290 passages across 4 acts.

---

## Design Principles

These apply to every expansion regardless of theme or genre.

1. **Every flag that is set must be checked somewhere meaningful.** No silent tracking. If a flag has no payoff, remove the `set_flags` rather than leaving it unchecked.
2. **Every item must have at least one explicit narrative moment.** A scene that calls the item out by name and changes what happens because of it — not just a stat bonus.
3. **Endings are path-gated, not score-gated.** The player earns each ending by making specific decisions, not by being statistically lucky. Flags are the gates, not SKILL/STAMINA thresholds.
4. **The existing passages are a skeleton.** Retain, expand, or re-number them. New passages fill the bones. Don't discard what already works.
5. **Acts have distinct tones.** Roughly: Act 1 = characterisation and setup, Act 2 = dread and revelation, Act 3 = escalating confrontation, Act 4 = consequence. Tune to your story's genre.

---

## Phase 0 — Audit the Existing Adventure

Before planning anything, understand exactly what you have.

### 0.1 Run the passage audit

```bash
python3 -c "
import json
with open('adventures/MY_ADVENTURE.json') as f:
    d = json.load(f)
p = d['passages']

types = {}
for pp in p.values():
    t = 'ending' if pp.get('ending') else 'combat' if pp.get('combat') else 'luck' if pp.get('test_luck') else 'choices'
    types[t] = types.get(t,0)+1

flags_set, flags_chk = set(), set()
for pp in p.values():
    for f in pp.get('set_flags',[]): flags_set.add(f)
    for c in pp.get('choices',[]):
        if c.get('requires_flag'): flags_chk.add(c['requires_flag'])
        if c.get('requires_no_flag'): flags_chk.add(c['requires_no_flag'])

endings = [(id, pp.get('ending_type','?')) for id,pp in p.items() if pp.get('ending')]

print('Passages:', len(p), '| Types:', types)
print('Endings:', endings)
print('Flags set (never checked):', sorted(flags_set - flags_chk))
print('Flags checked (never set):', sorted(flags_chk - flags_set))
print('Items:', list(d.get('items',{}).keys()))
"
```

### 0.2 Answer these questions before writing a single new passage

- Which flags are currently set but never checked? These are your raw material — they want to become meaningful decisions.
- Which items have no narrative use beyond stats? Each needs at least one scene.
- How many endings exist? What does the player need to do to reach each one? Is there only one "real" ending?
- What are the key character relationships in the story? Which ones could branch based on earlier choices?
- What is the central mystery or conflict? What are 3–4 different ways it could resolve?
- What decisions feel most morally weighted? Those should drive ending gates.

---

## Phase 1 — Write the Spec First

Write a spec document (`adventures/MY_ADVENTURE_spec.md`) before writing any passages. This is the contract. Opus will follow it; you will review against it.

The spec must contain:

### 1.1 Target structure

```
Target: [current] passages → ~[target] passages
Acts: [N] acts + [N] endings
Passage ID scheme: [prefixes for each act]
```

### 1.2 Passage numbering scheme

Use act prefixes for all passage IDs. The engine accepts any string.

| Prefix | Act | Example IDs |
|--------|-----|-------------|
| `a_` | Act 1 | `a_1` … `a_60` |
| `b_` | Act 2 | `b_1` … `b_70` |
| `c_` | Act 3 | `c_1` … `c_100` |
| `d_` | Act 4 | `d_1` … `d_70` |
| `end_` | Endings | `end_victory`, `end_sacrifice` |
| `death_` | Deaths | `death_fall`, `death_betrayal` |

Choose prefixes that match your story's acts. Rename existing numeric IDs (`"1"`, `"2a"`) as part of the expansion.

> **Critical:** When your first passage is no longer `"1"` (e.g. it becomes `"a_1"`), you **must** add a `start_passage` field to the adventure JSON top level:
> ```json
> {
>   "title": "...",
>   "start_passage": "a_1",
>   ...
> }
> ```
> Without this, the engine defaults to navigating to `"1"`, which won't exist. The character creation screen will complete normally but the game board will load blank — no stat bars, no text. This is easy to miss because the adventure JSON validates cleanly and the bug only shows at runtime.

### 1.3 The master flag table

The most important section of the spec. Every flag that will exist, before writing begins.

| Flag | Set at | Checked at | What it unlocks |
|------|--------|------------|-----------------|
| `flag_name` | `a_5` | `b_10`, `end_best` | [description] |

**Rules for the flag table:**
- Every row must have at least one entry in "Checked at" before you start writing. If you can't fill it in, the flag should not exist.
- Flags should represent decisions, relationships, or discoveries — not mechanical state. `helped_companion` is a good flag. `was_in_room_3` is not.
- Aim for 8–15 flags for a full 4-act expansion. Fewer is better than more.
- At least 2–3 flags should be required for the best ending. This is what makes it feel earned.

### 1.4 The ending condition matrix

| Ending ID | Label | Required flags | Engine fields |
|-----------|-------|---------------|---------------|
| `end_best` | Best victory | `flag_a + flag_b + flag_c` | `ending_type: "victory"` |
| `end_sacrifice` | Pyrrhic victory | `flag_a`, NOT `flag_b` | `add_luck: -1, ending_type: "victory"` |
| `end_warrior` | Hard-won | `flag_d + fought_final_boss` | `ending_type: "victory"` |
| `end_bargain` | Discovery | `flag_e + flag_f` | `add_luck: 2, ending_type: "victory"` |
| `end_drowned` | Death | Failed final luck test | `ending_type: "death"` |
| `end_hollow` | Failure | Lucky escape, too late | `ending_type: "death"` |

**Minimum recommended ending set:**
- 1 best victory (all key flags earned)
- 1–2 partial victories (some flags, meaningful cost)
- 1 "discovery" or hidden ending (unusual path, rare flag combination)
- 1–2 death/failure endings (fallback for underprepared players)

### 1.5 The item narrative payoff table

| Item ID | Name | At least one narrative use |
|---------|------|---------------------------|
| `item_a` | Sword | `b_15`: bypasses a combat entirely |
| `item_b` | Key | `c_3`: unlocks the sanctum |

Every item must have an entry. If an item has no narrative use, either give it one or remove it from `"items"` and `starting_items`.

### 1.6 Act structure (one section per act)

For each act, write:
- **Tone** (one sentence)
- **Passage budget** — explicit counts, not approximations (see below)
- **The spine** — the mandatory path, the minimum passages a rushing player takes
- **Major branches** — 2–4 optional branches, each with a flag payoff
- **Key beats** — passage-by-passage notes for the structurally critical moments

You do not need to write the prose in the spec. Notes are enough. Opus will write the prose.

#### Passage budget (required field for every act)

```
Migrated passages:    N   (existing passages being renamed into this act)
Named new passages:   N   (passages explicitly described in the spec)
Fill passages:        N   (exploration, atmosphere, connective tissue — unnamed but required)
─────────────────────────
Act minimum:          N   (Opus must reach this before submitting)
```

**Fill passages are not optional.** They are the exploration branches, atmospheric side rooms, and connector passages that make the act feel like a world rather than a logic diagram. Name the required ones; specify a hard minimum count for the rest.

Opus will implement every named passage and then stop unless you give it a number to hit. A spec that says "~10–15 passages of expanded exploration" gets 3. A spec that says "Fill passages: 12 minimum" gets 12.

> **Experience note:** On the Scavenger and Leviathan expansions, every act came in 30–50% short of the planned target. The cause was identical each time — approximate language in the spec ("~N passages", "some atmospheric passages") which Opus treated as an upper bound rather than a floor. Hard minimums fix this.

---

## Phase 2 — Flag Architecture Rules

These are the engine constraints that govern how flags can be used. Know them before designing the flag table.

### What the engine supports per choice

```json
{
  "text": "Button label",
  "goto": "b_10",
  "requires_flag": "one_flag",
  "requires_no_flag": "one_other_flag",
  "requires_item": "item_id"
}
```

Each choice supports **one** `requires_flag`, **one** `requires_no_flag`, and **one** `requires_item`. These are ANDed — all conditions must be true for the choice to appear.

### The engine does NOT support

- OR conditions on a single choice (`requires_flag_a OR requires_flag_b`)
- Conditional arrival effects (you cannot apply `add_stamina` only when a flag is set)
- `requires_no_item` on choices

### Workarounds for common patterns

**OR flag condition** (either flag_a or flag_b gives the same benefit):
```
Option A: At the source passage that sets flag_b, also set flag_a.
          Both paths share flag_a as the single gate. Cleaner.
Option B: Two choices with same text and goto, one per flag:
          { requires_flag: "flag_a" } → dest
          { requires_flag: "flag_b", requires_no_flag: "flag_a" } → dest
          (ungated fallback has requires_no_flag: "flag_b" — works for 2 flags, breaks for 3+)
```

**Conditional arrival effect** (stamina penalty only if flag NOT set):
```
Split the choice into two routes:
- requires_flag: "protective_flag" → dest (no penalty)
- requires_no_flag: "protective_flag" → dest_b (new passage with add_stamina: -N → dest)
```

**Duplicate choice labels** (flag-gated choice + ungated fallback, same text):
Always add `requires_no_flag` to the ungated fallback. If you don't, both choices show simultaneously when the flag is set.
```json
{ "text": "Attack", "goto": "b_20", "requires_flag": "kael_distracted" }
{ "text": "Attack", "goto": "b_18", "requires_no_flag": "kael_distracted" }
```
This is the most common bug in Opus-written drafts. Always scan for it on review.

---

## Phase 3 — Act Writing with Opus

Write one act at a time. Do not give Opus the whole spec and ask for everything at once.

### 3.1 Opus prompt template

```
You are writing [Act N] of [ADVENTURE TITLE], a Fighting Fantasy-style gamebook
in the StoryForge engine.

Output a JSON file to: adventures/[ADVENTURE]_act[N]_draft.json
Format: { "passages": { "id": {...}, ... } } — new passages only, not the full adventure.

[PASTE THE FULL PASSAGE SCHEMA SECTION FROM CLAUDE.md HERE]
[PASTE THE ENGINE CONSTRAINTS SECTION — one choice/combat/luck/ending per passage, etc.]

## Entry point
[Passage ID that enters this act, and what just happened in the previous act to set the scene]

## Flags arriving from earlier acts
[List every flag that may be set when the player enters this act, and what it means]

## Items that may be in inventory
[List every item and its narrative significance for this act]

## Enemies available
[List enemy IDs from the live JSON, with SKILL/STAMINA values]

## Act structure — follow this closely
[Paste the relevant act section from the spec, passage by passage]

## New flags to set this act
[List flags that should be set in this act, which passages set them, what they unlock]

## Prose style
[Genre, tone, tense (second person present), any specific voice notes]

## Passage count requirement
This act must contain at least [N] passages. After writing all named passages,
count your total. If you are below [N], you are not finished — add more
exploration branches, atmospheric side passages, and optional encounters until
you reach the minimum. Do not submit the draft until the count is met.

To count: the number of keys in your "passages" object must be ≥ [N].

## Validation requirement
After writing, run this validator and fix any errors before finishing:
[Paste the validation script from CLAUDE.md, adapted for this act's start ID]
```

### 3.2 What Opus does well

- Writing evocative prose in an established tone
- Following a passage-by-passage spec
- Wiring flags correctly when the spec is explicit
- Creating connector passages and atmospheric filler between key beats

### 3.3 What to check in Opus's draft

Run this scan before merging any draft:

```python
# Check for duplicate choice label bugs
for id, pp in sorted(passages.items()):
    choices = pp.get('choices', [])
    texts = [c['text'] for c in choices]
    if len(texts) != len(set(texts)):
        print(f"DUPLICATE LABELS at {id}:")
        for c in choices:
            reqs = [c.get('requires_flag'), c.get('requires_no_flag')]
            print(f"  '{c['text']}' → {c['goto']} flags={reqs}")
```

**Duplicate labels are a logic bug, not a cosmetic issue.** When a flag-gated choice and its ungated fallback share the same label, both buttons appear when the flag is set. Fix by adding `requires_no_flag` to the fallback (see Phase 2).

**Other things to check:**
- Flags set in this act but never checked anywhere — are they in the spec? If not, remove them.
- Flags set by Opus that weren't in the spec — evaluate whether they add value. If not, remove `set_flags`.
- Enemy IDs — Opus will sometimes invent enemy names. They must match existing enemy IDs in the live JSON.
- `requires_no_item` — this field does not exist in the engine. Remove it if Opus uses it.

---

## Phase 4 — Merge Process

### 4.1 Validate the draft in isolation

```python
import json
with open('adventures/MY_ADVENTURE_act[N]_draft.json') as f:
    d = json.load(f)
passages = d['passages']
external = {'death_a', 'death_b'}  # known passage IDs in live adventure

errors = []
visited = set()
queue = ['[start_id]']  # first passage of this act
while queue:
    cur = queue.pop()
    if cur in visited: continue
    visited.add(cur)
    if cur not in passages and cur not in external:
        errors.append(f'Referenced but missing: {cur}')
        continue
    if cur in external: continue
    pp = passages[cur]
    for c in pp.get('choices', []):
        g = c['goto']
        if g not in passages and g not in external: errors.append(f'[{cur}] bad goto {g}')
        else: queue.append(g)
    for field in ['win_goto','flee_goto']:
        t = pp.get('combat', {}).get(field)
        if t:
            if t not in passages and t not in external: errors.append(f'[{cur}] bad {field} {t}')
            else: queue.append(t)
    for field in ['lucky_goto','unlucky_goto']:
        t = pp.get('test_luck', {}).get(field)
        if t:
            if t not in passages and t not in external: errors.append(f'[{cur}] bad {field} {t}')
            else: queue.append(t)
unreachable = set(passages.keys()) - visited
if unreachable: errors.append(f'Unreachable: {sorted(unreachable)}')
print('OK' if not errors else '\n'.join(errors))
```

Resolve all errors before merging. Never merge a draft with broken gotos.

### 4.2 Inject into the live adventure

```python
import json
with open('adventures/MY_ADVENTURE.json') as f:
    live = json.load(f)
with open('adventures/MY_ADVENTURE_act[N]_draft.json') as f:
    draft = json.load(f)

live['passages'].update(draft['passages'])
live['version'] = '2.0-act[N]'

with open('adventures/MY_ADVENTURE.json', 'w') as f:
    json.dump(live, f, indent=2, ensure_ascii=False)
```

### 4.3 Full validate from start passage

After injecting, run the full BFS validator from the adventure's first passage (`s_1`, `a_1`, or `1`). Every passage must be reachable and every goto must resolve.

---

## Phase 5 — Flag Audit After Each Act

After merging, open the adventure map (`adventure_map.html`) and check the **Flag Audit** panel.

| Status | Meaning | Action |
|--------|---------|--------|
| ✓ ok | Set somewhere, checked somewhere | Nothing |
| ⚠ unchecked | Set but never checked | Is this a spec miss or a redundant flag? |
| ✗ unset | Checked but never set | Bug — fix immediately |

### Resolving unchecked flags

Ask: **Why was this flag set?** If you can answer "to gate [specific passage] later," add the gate. If you can't, remove `set_flags`.

**Genuine spec miss** (the payoff exists in the spec but wasn't implemented):
- Add the check to the passage the spec describes.

**Redundant tracking flag** (set to record something happened, but nothing checks it):
- Remove `set_flags` from the source passage.

**Mechanical flag** (drives routing or enemy selection, no check needed):
- The effect IS the routing. Leave it. `morrow_surprised` routes to a lower-STAMINA combat — no check needed.

**OR-condition workaround** (two flags with the same intended effect):
- At the source of the weaker flag, also set the stronger flag. Then use one gate. Example: `pell_warned_you` → also sets `knows_first_mate` → single check at the payoff passage.

---

## Phase 6 — Applying This to an Existing Short Adventure

The three existing short adventures all show the same pattern:

| Adventure | Passages | Unchecked flags | Endings |
|-----------|----------|-----------------|---------|
| Crypt of Count Valdric | 43 | 9 of 11 | 1 victory, 3 death |
| Scavenger of New Babylon Station | 57 | 8 of 11 | 2 victory, 4 death |
| Throne of the Hollow King | 70 | 3 of 12 | 2 victory, 3 defeat |

For each, the expansion process is:

1. **Read the existing adventure** — understand the protagonist, the central conflict, the main NPCs, and the existing items.
2. **List what's already set up** — the unchecked flags are an accidental spec. They tell you what decisions the original author tracked. Build on them.
3. **Design the endings first** — pick 4–6 endings that reflect genuinely different resolutions of the central conflict, each requiring a different combination of the existing (or new) flags.
4. **Write the spec** (see Phase 1 above), filling in the flag table from the existing flags plus any new ones the endings require.
5. **Plan the act structure** — how many acts, where the existing passages land, what new material fills each act.
6. **Rename existing IDs** — convert numeric IDs to act-prefixed IDs before writing new passages. Keep a migration map in the spec.
7. **Write act by act with Opus** — one act per background task, review and merge before starting the next.

### Naming your passage prefixes

Choose prefixes that evoke the act's setting. Keep them short (1–2 letters + underscore).

*Crypt of Count Valdric* example:
- `v_` — the village/approach
- `c_` — the crypt entrance and upper levels
- `d_` — the deep crypts
- `k_` — the keep / Valdric's throne

*Scavenger of New Babylon Station* example:
- `s_` — the station exterior / docking
- `h_` — the hab ring
- `e_` — engineering / lower decks
- `b_` — the bridge / final confrontation

---

## Engine Quick Reference

### Passage schema

```json
"id": {
  "text": "Narrative. Use \\n for paragraph breaks.",

  "add_items":    ["item_id"],
  "remove_items": ["item_id"],
  "set_flags":    ["flag_name"],
  "clear_flags":  ["flag_name"],
  "add_stamina":  -2,
  "add_skill":    1,
  "add_luck":     -1,

  "choices": [ ... ]
}
```

Arrival effects (`add_items`, `set_flags`, `add_stamina`, etc.) always apply when the passage is entered, before anything is rendered. They are unconditional.

A passage must have **exactly one** of: `choices`, `combat`, `test_luck`, or `ending`.

### Combat

```json
"combat": {
  "enemy": "enemy_id",
  "win_goto": "next_id",
  "flee_goto": "fallback_id",
  "flee_allowed": true,
  "flee_stamina_cost": 2
}
```

Enemy IDs must be defined in the adventure's top-level `"enemies"` object. Enemies have `skill` and `stamina`. To have the same enemy appear weaker in certain circumstances, define a second enemy ID with lower stats (e.g. `enemy_weakened`).

### Test luck

```json
"test_luck": {
  "lucky_text": "...",   "lucky_goto": "a",
  "unlucky_text": "...", "unlucky_goto": "b",
  "lucky_stamina_cost": 0,
  "unlucky_stamina_cost": 3,
  "lucky_add_items": [],
  "unlucky_add_items": []
}
```

### Ending

```json
"ending": true,
"ending_type": "victory"
```

`ending_type` is `"victory"` or `"death"`. Arrival effects apply before the ending renders — use this to remove items, adjust luck, etc.

### Choice conditions

| Field | Meaning |
|-------|---------|
| `requires_item` | Item must be in inventory |
| `requires_flag` | Flag must be in flag set |
| `requires_no_flag` | Flag must NOT be in flag set |

All conditions are ANDed. Only one of each per choice. No OR conditions. No `requires_no_item`.

### Item fields

| Field | Effect |
|-------|--------|
| `skill_bonus` | Added to attack roll in combat (best in inventory wins, not stacked) |
| `damage_bonus` | Added to base damage per hit (best in inventory wins) |
| `stamina_restore` | Stamina restored when used as consumable |

---

## Checklist

### Before writing (spec review)

- [ ] Every flag in the master flag table has at least one "Checked at" entry
- [ ] Every ending in the matrix has a unique, achievable flag combination
- [ ] Every item has a narrative use beyond stats
- [ ] The best ending requires 3+ flags (feels earned)
- [ ] There is a fallback path (no flags) that reaches an ending — players who miss everything should still reach a resolution

### After each Opus draft

- [ ] Passage count meets the act minimum from the spec — if short, send it back
- [ ] Validator passes (no broken gotos, no unreachable passages)
- [ ] No duplicate choice labels (both gated and ungated versions of the same label)
- [ ] No Opus-invented enemy IDs (must match live JSON)
- [ ] No `requires_no_item` usage
- [ ] All new flags Opus introduced are either in the spec or removed

### After merging each act

- [ ] Full validator from start passage passes
- [ ] Flag audit in adventure map shows no `✗ unset` flags
- [ ] All `⚠ unchecked` flags have been evaluated (fix or remove)
- [ ] New passages are reachable in the adventure map

### Before calling the expansion complete

- [ ] All 4 acts written and merged
- [ ] All 4–6 endings reachable from start passage
- [ ] Flag audit panel shows all flags as `✓ ok`
- [ ] `start_passage` field is set in the adventure JSON if the first passage is not `"1"`
- [ ] Path lengths in adventure map show reasonable shortest/longest routes to each ending
- [ ] Version bumped to `2.0` in the adventure JSON
