# Act 1 Opus Prompt — Black Flag Running

---

You are writing **Act 1** of **BLACK FLAG RUNNING**, a Fighting Fantasy-style gamebook in the StoryForge engine.

Output a single valid JSON object with this exact format:

```json
{ "passages": { "a_1": { ... }, "a_2": { ... }, ... } }
```

New passages only. Do not include items, enemies, character, or any top-level fields — only the `passages` object.

Save to: `adventures/black_flag_running_act1_draft.json`

---

## Engine — Passage Schema

Each passage is a JSON object. Every field is optional except that each passage must have **exactly one** of: `choices`, `combat`, `test_luck`, or `ending`.

```json
"a_1": {
    "text": "Narrative text. Use \\n for paragraph breaks.",

    "add_items":    ["item_id"],
    "remove_items": ["item_id"],
    "set_flags":    ["flag_name"],
    "clear_flags":  ["flag_name"],
    "add_stamina":  -2,
    "add_skill":    1,
    "add_luck":     -1,

    "choices": [
        { "text": "Button label", "goto": "a_2" },
        { "text": "Requires item",    "goto": "a_3", "requires_item": "item_id" },
        { "text": "Requires flag",    "goto": "a_4", "requires_flag": "flag_name" },
        { "text": "Requires no flag", "goto": "a_5", "requires_no_flag": "flag_name" },
        { "text": "Flee choice",      "goto": "a_6", "style": "danger" }
    ]
}
```

**Arrival effects** (`add_items`, `set_flags`, `add_stamina`, etc.) always apply when the passage is entered, before anything is rendered. They are unconditional — you cannot make them conditional on a flag.

### Combat passage

```json
"a_7": {
    "text": "...",
    "combat": {
        "enemy": "naval_marine",
        "win_goto": "a_8",
        "flee_goto": "a_2",
        "flee_allowed": true,
        "flee_stamina_cost": 2
    }
}
```

### Test luck passage

```json
"a_9": {
    "text": "...",
    "test_luck": {
        "lucky_text": "...",   "lucky_goto": "a_10",
        "unlucky_text": "...", "unlucky_goto": "a_11",
        "lucky_stamina_cost": 0,
        "unlucky_stamina_cost": 3
    }
}
```

### Ending passage

```json
"death_example": {
    "text": "...",
    "ending": true,
    "ending_type": "death"
}
```

`ending_type` is `"victory"` or `"death"`.

### Engine constraints — hard rules

- A passage must have **exactly one** of: `choices`, `combat`, `test_luck`, or `ending`. Never two of these in the same passage.
- Each choice supports **one** `requires_flag`, **one** `requires_no_flag`, and **one** `requires_item`. All conditions are ANDed.
- There is **no** `requires_no_item` field. Do not use it.
- There are **no** OR conditions on a single choice.
- Passage IDs are strings: `"a_1"`, `"a_12"`, `"death_docks"` — all valid.
- **Duplicate choice label rule:** If a passage has two choices with the same text (one flag-gated, one ungated fallback), the ungated fallback MUST have `requires_no_flag` set to that flag. Without it, both buttons show simultaneously when the flag is set. This is a logic bug. Always add `requires_no_flag` to the fallback.

---

## Adventure Context

You are writing for a new player arriving at Nassau for the first time. The player is the **captain of The Adamant**, a capable but unremarkable sloop. They have a crew who know them well enough to trust them — and well enough to watch them carefully. They are new to Nassau. Their reputation exists elsewhere. Every faction in the Free Republic will measure them before letting them in.

**The situation:**
Nassau is a pirate republic under pressure. **Commodore Ashford** of the Crown's Atlantic Fleet has three warships sitting at the mouth of the harbour — *Crown's Justice*, *Fervent*, and *Resolve*. He has been there eleven days. He has not fired a shot. He is waiting for something.

The key to breaking the blockade lies in the wreck of the **San Cristóbal** — a Crown galleon that sank in the Shallows of Perdition, eight leagues south, a decade ago. She carried a war chest and a sealed diplomatic pouch called **the Red Correspondence**, which implicates Ashford in a fraudulent prize claim that cost two hundred sailors their lives. The player does not know all of this yet. In Act 1 they learn the San Cristóbal exists and that its location is being kept quiet.

**Key NPCs:**
- **Captain Reyna Morrow** — Nassau's dominant captain. Measured, political, in control. She has been sitting on the San Cristóbal's location for three years and has not acted. She does not explain why.
- **The Harbour Council** — The merchant faction. Represented by a factor named **Aldous Crane** — precise, well-dressed, entirely pragmatic. The merchants want stability. They will back whoever can provide it.
- **Commodore Ashford** — Not present in Act 1. Referenced only. Three ships on the horizon.
- **The Adamant's crew** — Named individuals include the first mate **Pell** (loyal, watchful, has sailed with the captain for years) and at least two other crew members introduced in passing.

---

## Starting Inventory (what the player has entering Act 1)

- `cutlass` — Cutlass, weapon, skill_bonus: 1
- `flintlock` — Flintlock Pistol, weapon, skill_bonus: 2
- `captain_chart` — Captain's Chart, key item (no combat stats)
- 4 provisions

---

## Enemies Available in Act 1

Only use these enemy IDs. Do not invent new ones.

| ID | Name | SKILL | STAMINA |
|----|------|-------|---------|
| `naval_marine` | Crown Marine | 7 | 6 |
| `harbour_thug` | Harbour Thug | 5 | 5 |

---

## Flags to Set in Act 1

These are the only flags Act 1 should set. Do not introduce flags not listed here.

| Flag | Set when | How |
|------|----------|-----|
| `crew_trusts_you` | Player makes 2–3 small decisions that favour the crew's interests | See crew loyalty rules below — this must feel like natural roleplay, not an announced system |
| `morrow_ally` | Player earns Morrow's trust through the Morrow path | Mutually exclusive with `morrow_rival` |
| `morrow_rival` | Player challenges or undermines Morrow | Mutually exclusive with `morrow_ally` — use `requires_no_flag: "morrow_ally"` on the choice that sets `morrow_rival` |
| `council_backed` | Player successfully negotiates with Crane (Council path) | Partial at this stage — solidifies in Act 2 |

---

## Crew Loyalty — Critical Implementation Note

`crew_trusts_you` must be set through **small, natural roleplay decisions** — not through a single "be nice to your crew" choice. The player must not feel like they are filling a loyalty meter. The flag accumulates invisibly through 2–3 separate moments.

**Examples of valid crew loyalty moments:**
- How the player handles a crew complaint about provisions during the approach to Nassau
- Whether they allow first mate Pell to go ashore when it costs the player time
- How they respond when Nassau locals look down at the Adamant or her crew
- Whether they share early intelligence with the crew or keep it to themselves

Each of these is a branching passage where one option earns crew trust and the other does not. The flag `crew_trusts_you` should be set using a `set_flags` arrival effect on a passage the player reaches only by making the crew-favouring choice — not on a choice button.

The flag is **not** set in a single passage. Spread the moments naturally across the act.

---

## Act 1 Structure — Follow This Closely

### Tone
Atmosphere and establishment. Nassau breathes. It smells of tar, rot, and money. The blockade sits on the horizon like a threat no one wants to name first. Everyone is watching the new captain off the Adamant. This is not an adventure yet — it is a world being read.

### Spine (mandatory path every player takes)

- **`a_1`** — The Adamant approaches Nassau harbour at dawn. The three blockade ships are visible on the horizon — name them: *Crown's Justice*, *Fervent*, *Resolve*. A harbour pilot comes alongside in a small boat. He is nervous. He gives the player a quick read of the situation: blockade eleven days, no shots fired, Morrow holding things together, tension in the port. The player chooses how to respond to him. One crew loyalty moment available here (share something with the pilot that reassures the crew, or keep everything close).

- **`a_2`** — Dockside. The Adamant is tied up. First impressions of Nassau: the fort, the market, the ships with their rigging stripped for sale. Pell gives his read. Three directions available: seek out Morrow, find the Harbour Council's factor, or ask around independently.

- **`a_3`** — **The Broken Wheel tavern** — central hub. Three NPCs are present: a Morrow lieutenant (gives nothing away), Aldous Crane the Council factor (precise, interested in the new arrival), and an old sailor named **Drest** who knew the San Cristóbal's last captain and will talk freely if bought a drink. The player can engage any of them. Drest is the one who introduces the San Cristóbal as a rumour — he does not know where it is, but he knows what it was carrying.

- **Act 1 close** — By the end of the act the player knows: the blockade is real and tightening, the San Cristóbal exists and its cargo could change everything, and the location is being held back by someone (Morrow, most likely). They have made at least one meaningful faction contact.

### Major Branches

**Branch 1 — The Morrow Path**
The player seeks an audience with Reyna Morrow. She does not grant it immediately — they must do something to earn it. A Morrow lieutenant in the Broken Wheel tests the player's intentions first. The audience itself is a measured exchange: Morrow is not hostile, but she is sizing the player up. She sets a small task or asks a pointed question. The player's response either earns `morrow_ally` (if they demonstrate capability and respect her authority) or sets `morrow_rival` (if they push too hard, challenge her, or make a mistake). She does not reveal the San Cristóbal's location — not yet. She knows more than she says and the player should feel that.

This branch should contain at least 12–15 passages including approach, lieutenant encounter, the audience itself, and the aftermath.

**Branch 2 — The Council Path**
The player seeks out Aldous Crane. He is in the Broken Wheel or at the Harbour Council's small office near the dock. He is interested in the Adamant — a new ship is a potential asset. The negotiation passage: Crane wants assurances that the player is committed to Nassau's survival, not just passing through for a score. A choice here that demonstrates commitment (even at personal cost) can set `council_backed` at this stage. Crane also knows the San Cristóbal is real — he has seen old survey records — but he does not have the location. He is the one who tells the player that Morrow has it and is sitting on it.

This branch should contain at least 10–12 passages including finding Crane, the negotiation, and the aftermath.

**Branch 3 — The Independent Path**
The player asks around the harbour without targeting either faction. Slower, less immediately flagged. They talk to dockworkers, other captains, merchants. They find Drest more easily on this path — he is a known figure in the harbour. This path does not set `morrow_ally` or `council_backed` in Act 1, but it surfaces more raw information: the shape of the political situation, the fact that Morrow has been sitting on something for years, and the first hint of Ashford's personal stake in whatever is on the San Cristóbal (a rumour, nothing confirmed). Optional `harbour_thug` combat here — a dockside dispute over the Adamant's berth.

This branch should contain at least 10–12 passages.

**Branch 4 — Crew Passages**
3–4 passages establishing the Adamant's crew. First mate Pell is introduced early. Other crew members in passing. The crew loyalty moments are distributed here and across the other branches — not concentrated in a single crew-focused section.

**Dockside Altercation — Optional Combat**
A Crown marine in civilian clothes is watching the Adamant from the dockside. He makes no move unless approached. If the player investigates: a brief confrontation. The player can diffuse it (information gained — the marine was sent by Ashford's ship, confirms Ashford is watching new arrivals), or let it escalate to combat (`naval_marine`, SKILL 7, STAMINA 6). The cutlass should be referenced by name in whichever passage this resolves in — this is its Act 1 narrative moment.

### Key Beats (must appear regardless of path)

1. The three blockade ship names on the horizon — *Crown's Justice*, *Fervent*, *Resolve* — mentioned by `a_1`.
2. Drest in the Broken Wheel introduces the San Cristóbal as a rumour — what it was carrying, that someone knows where it is, that no one is acting on it.
3. The cutlass is named in at least one passage (the dockside altercation or the Morrow audience).
4. Act 1 ends with the player knowing they need the location. They do not have it. Someone has it. Nassau is running out of time.

---

## Prose Style

**Register:** Second person, present tense throughout. "You stand on the deck. The harbour opens before you."

**Tone reference:** Black Sails, not Pirates of the Caribbean. Gritty, politically aware, morally weighted. Nassau is a real place with real politics — not a theme park. The pirates are people with legitimate grievances and complicated histories, not romanticised adventurers.

**What this means in practice:**
- No magical thinking, no supernatural elements, no fantasy flourishes
- Violence is consequential, not exciting — a dead marine is a problem, not a victory
- Every NPC has a reason for what they want — no cartoonish villains
- The sea and the port are described with physical specificity: smells, sounds, the weight of humid air, the sound of rigging
- Pirate slang is grounded — "Dragon's Breath" for explosives, "widow maker" for a pistol — recognisable, thematic, never whimsical
- Morrow is not eccentric or theatrical. She is competent and contained. She commands through the quality of her attention, not through performance.

**Passage length:** 80–150 words per passage. Long enough to be immersive, short enough to read quickly. Do not pad. Do not summarise. Show, don't tell.

---

## Passage Count Requirement

**Act 1 minimum: 55 passages.**

After writing all named passages and branches, count the number of keys in your `"passages"` object. If the count is below 55, you are not finished.

Add more passages — exploration branches, atmospheric side passages, additional crew moments, dockside encounters, conversations that branch further. Every fill passage must serve the world: a conversation that reveals something, a choice that feels meaningful, a moment of atmosphere that makes Nassau feel inhabited.

**Do not submit this draft until the passages object contains at least 55 keys.**

To count: `len(data["passages"])` must be ≥ 55.

---

## Validation Requirement

After writing, run this validator. Fix all errors before finishing.

```python
import json
with open('adventures/black_flag_running_act1_draft.json') as f:
    d = json.load(f)
passages = d['passages']

# Passages that will exist in later acts — valid gotos from Act 1's close passages
future_passages = set()  # Act 1 should be self-contained; close passages should end at choices, not goto Act 2

errors = []
visited = set()
queue = ['a_1']
while queue:
    cur = queue.pop()
    if cur in visited: continue
    visited.add(cur)
    if cur not in passages:
        errors.append(f'Referenced but missing: {cur}')
        continue
    pp = passages[cur]
    for c in pp.get('choices', []):
        g = c['goto']
        if g not in passages: errors.append(f'[{cur}] bad goto {g}')
        else: queue.append(g)
    for field in ['win_goto', 'flee_goto']:
        t = pp.get('combat', {}).get(field)
        if t:
            if t not in passages: errors.append(f'[{cur}] bad {field} {t}')
            else: queue.append(t)
    for field in ['lucky_goto', 'unlucky_goto']:
        t = pp.get('test_luck', {}).get(field)
        if t:
            if t not in passages: errors.append(f'[{cur}] bad {field} {t}')
            else: queue.append(t)

unreachable = set(passages.keys()) - visited
if unreachable: errors.append(f'Unreachable passages: {sorted(unreachable)}')
print(f'Passage count: {len(passages)}')
print('OK' if not errors else '\n'.join(errors))
```

Also run this duplicate label check:

```python
import json
with open('adventures/black_flag_running_act1_draft.json') as f:
    d = json.load(f)
for pid, pp in sorted(d['passages'].items()):
    choices = pp.get('choices', [])
    texts = [c['text'] for c in choices]
    if len(texts) != len(set(texts)):
        print(f'DUPLICATE LABELS at {pid}:')
        for c in choices:
            print(f"  '{c['text']}' → {c['goto']} requires_flag={c.get('requires_flag')} requires_no_flag={c.get('requires_no_flag')}")
```

Fix all errors and duplicate labels before submitting. The passage count must be printed and must be ≥ 55.
