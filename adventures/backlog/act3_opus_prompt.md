# Black Flag Running — Act 3 Writing Prompt for Claude Opus

You are writing Act 3 of a Fighting Fantasy-style gamebook adventure called **Black Flag Running**. The adventure is 175 passages through two completed acts. Act 3 must produce a **minimum of 70 passages** using the `s_` prefix. Under-counting is a critical failure mode — count your passages before finishing and add fill passages if needed.

---

## Engine Schema

Adventures are defined in JSON. The passage object supports exactly these fields:

```json
"s_1": {
    "text": "Narrative text. Use \\n for paragraph breaks.",

    "choices": [
        { "text": "Button label", "goto": "s_2" },
        { "text": "Requires item",  "goto": "s_3", "requires_item": "captain_chart" },
        { "text": "Requires flag",  "goto": "s_4", "requires_flag": "crew_loyal" },
        { "text": "Requires no flag", "goto": "s_5", "requires_no_flag": "morrow_rival" },
        { "text": "Danger style",   "goto": "s_6", "style": "danger" }
    ]
}
```

A passage has **one** of: `choices`, `combat`, `test_luck`, or `ending`. Not more than one.

```json
"combat": {
    "enemy": "naval_officer",
    "win_goto": "s_10",
    "flee_goto": "s_9",
    "flee_allowed": true,
    "flee_stamina_cost": 2
}

"test_luck": {
    "lucky_text": "...", "lucky_goto": "s_10",
    "unlucky_text": "...", "unlucky_goto": "s_11",
    "lucky_stamina_cost": 0,
    "unlucky_stamina_cost": 3,
    "lucky_add_items": [],
    "unlucky_add_items": []
}

"ending": true,
"ending_type": "death"
```

**Arrival effects** (always apply before rendering, can appear on any passage alongside choices/combat/test_luck):
```json
"add_items":    ["red_correspondence"],
"remove_items": ["war_chest"],
"set_flags":    ["red_correspondence_held"],
"clear_flags":  ["crew_loyal"],
"add_stamina":  -3,
"add_skill":    0,
"add_luck":     -1
```

**Rules:**
- Duplicate choice labels within one passage are a validator error. Never give two choices in the same passage the same `"text"` string.
- All `goto` values must point to passages that exist in this act OR in Acts 1–2 (`a_`, `n_` prefixes, provided) OR to `r_1` (Act 4 start — not yet written, but the reference is valid for this draft).
- Death passages use `"ending": true, "ending_type": "death"`. Use `death_shallows` as the ID for the primary Shallows death.
- Passage IDs are strings: `"s_1"`, `"s_2"` etc.

---

## Adventure Context

**Setting:** The Shallows of Perdition, 8 leagues south of Nassau. A maze of coral reef, crystal-clear lagoon water, and the wreck of the San Cristóbal — a Crown galleon that went down a decade ago.

**The player is:** Captain of The Adamant, a capable sloop. They have just entered the lagoon through the reef (passage n_61 → s_1) and are looking at a crystal lagoon with the wreck somewhere below.

**What the San Cristóbal contains:**
- The **Red Correspondence** — sealed brass tube in the captain's cabin. Letters with Commodore Ashford's signature implicating him in a fraudulent prize claim that killed 200 sailors. Reading the first letter should be a passage beat — show a fragment of the content.
- The **Crown War Chest** — heavy, stamina cost to move. Can slow the Adamant on the return.
- The **Dragon's Breath** — sealed explosive canisters in the armoury. Still volatile. Taking them is a risk. Not taking them closes an Act 4 option.

**Items already in the adventure JSON:**
- `captain_chart` (key) — `san_cristobal_chart` is also in JSON as an alias
- `red_correspondence` (key)
- `war_chest` (key)
- `dragons_breath` (weapon, damage_bonus: 1)
- `provisions` (consumable, stamina_restore: 4)
- `cutlass` (weapon, skill_bonus: 1)
- `flintlock` (weapon, skill_bonus: 2)
- `morrow_seal` (key)
- `harbour_bond` (key)

**Enemies in the adventure JSON:**
- `naval_marine` — SKILL 7, STAMINA 6
- `naval_officer` — SKILL 8, STAMINA 8
- `rival_crew` — SKILL 6, STAMINA 6
- `morrow_enforcer` — SKILL 7, STAMINA 7
- `harbour_thug` — SKILL 5, STAMINA 5
- `morrow` — SKILL 8, STAMINA 9 (only if full morrow_rival path)
- `ashford` — SKILL 9, STAMINA 10 (Act 4 only)

Do NOT invent new enemy IDs. Use only the above.

---

## Flag State Entering Act 3

Flags that may be set when Act 3 starts (depending on player path through Acts 1–2):

**Always set:**
- `knows_location` — set at end of Act 1. The player has Morrow's chart.

**Crew loyalty (build/spend resource):**
- `crew_trusts_you` — may be set from Act 1 crew decisions
- `crew_loyal` — may be set if `crew_trusts_you` held through Act 2

**Morrow relationship (mutually exclusive groups):**
- `morrow_committed` — player discovered Morrow's secret and chose compassion. **If this flag is set, Morrow's ship left Nassau before the Adamant. She is already at the Shallows.**
- `morrow_cornered` — player used Morrow's secret as leverage. She will help reluctantly.
- `morrow_rival` — player challenged or exposed Morrow. She will contest the prize.
- `morrow_ally` — base ally path from Act 1 (no secret involved)
- *(no Morrow flag)* — Morrow is neutral; she does not appear at the Shallows

**Other flags:**
- `ashford_contact` — player opened a back-channel with Commodore Ashford. His patrol is lighter.
- `council_backed` — Harbour Council formally backs the player
- `has_pilot` — Sable, a skilled reef pilot, is aboard the Adamant
- `morrow_secret_known` — player knows about Morrow's history with the San Cristóbal
- `crew_fractured` — may be set this act if crew loyalty breaks

**Flags to SET in Act 3:**
- `red_correspondence_held` — when player recovers the Red Correspondence
- `war_chest_held` — when player recovers the war chest
- `crew_fractured` — if crew loyalty breaks during forced dive or failed pursuit
- Any items added via `add_items` should have a corresponding flag set (e.g., `add_items: ["red_correspondence"]` + `set_flags: ["red_correspondence_held"]`)

---

## Act 3 Structure

### Passage prefix: `s_`
### Minimum passages: **70** (count carefully before finishing)
### Start passage: `s_1`
### End: All paths eventually reach `r_1` (Act 4 start — write the goto but r_1 does not exist yet)

---

### Spine

`s_1` — The lagoon. The wreck is below. The player has arrived.
→ The dive. Finding the San Cristóbal. The descent.
→ Inside the wreck. Recovery passages. `red_correspondence` and `war_chest` available.
→ Morrow arrives (flag-dependent — see branches below).
→ Pursuit. Naval patrol or rival crew appears (flag-dependent).
→ Return to Nassau. Running the blockade.
→ Hand off to `r_1`.

---

### Major Branches

#### 1. The Dive — Crew Loyalty

`crew_loyal` set:
- The crew goes willingly. One named crewman (Pell, who has appeared in Acts 1–2) volunteers to lead the first dive. The recovery is efficient — player gets first choice of what to recover.
- No luck test required for basic recovery.

`crew_loyal` NOT set:
- The crew hesitates. A confrontation passage: the player must convince, pay, or order. 
- If convinced: proceed, but set `crew_fractured` if the method was coercive.
- A luck test covers the dive itself. Unlucky result = injury, add_stamina: -3.

#### 2. The Wreck Interior — Recovery

The San Cristóbal lies on her side. Key locations to write:
- The entry point — coral-encrusted gunport, squeeze through.
- The cargo hold — the war chest is here. Heavy. Requires multiple dives.
- The captain's cabin — the brass tube with the Red Correspondence.
- The armoury — Dragon's Breath canisters. Optional recovery, risk involved.

Player may take:
- `red_correspondence` only → `set_flags: ["red_correspondence_held"]`
- `war_chest` only → `set_flags: ["war_chest_held"]`
- Both (requires crew_loyal or extra time — risk of discovery)
- `dragons_breath` → `add_items: ["dragons_breath"]`

**Mandatory beat:** When the Red Correspondence is found and opened, show a fragment — Ashford's handwriting, a date, a sentence that makes the crime clear. The reader must feel why this document matters.

**Mandatory beat:** The captain_chart is read aloud before or during the dive — the specific notation Morrow made, the depth, the bearing. This is the item's narrative moment.

#### 3. Morrow's Arrival

**`morrow_committed`:** Morrow's sloop is already anchored in the lagoon when the Adamant arrives. Her crew is diving. She does not interfere with your recovery — they work alongside. A brief exchange with Morrow herself. She has already made her choice. This should be written with restraint — she is not warm, but she is committed. End the exchange cleanly.

**`morrow_ally` or `morrow_cornered`:** Morrow's sloop arrives during the recovery. Tense standoff. She waits. A brief exchange. She will not take the prize — but she wants to know what you found. You may show her the Correspondence (she already knows what it says) or tell her nothing. She leaves without incident.

**`morrow_rival`:** Morrow's crew moves to cut off the Adamant's boat. Confrontation: fight (combat with `rival_crew`), negotiate (costs something — share or stamp of authority), or flee (leave some of the prize behind). If `morrow_secret_known` and secret not yet used, a last-resort leverage option: reveal it here, sets `morrow_cornered` late — partial benefit, Morrow backs off but the relationship is poisoned.

**No Morrow flag:** Morrow does not appear. The wreck is uncontested.

#### 4. The Naval Patrol

**`ashford_contact` set:** Ashford's patrol is one vessel, watching at distance. They do not intercept while you are in the lagoon. On departure, a signalled warning — his flag lieutenant signals from the patrol vessel. The player may signal back (acknowledge the deal) or ignore it. Either is valid.

**`ashford_contact` NOT set:** A naval patrol closes on the lagoon as you are preparing to leave. Two vessels. Combat possible (`naval_officer`). The player may fight, run the channel under fire, or bluff (luck test). Heavy tension — this is the moment the return could fall apart.

#### 5. The Passage Through the Reef — Return

The return through the reef channel should be a distinct sequence:
- `has_pilot`: Sable brings the Adamant out clean. A line about what she sees in the water that no one else could read.
- No `has_pilot`: Luck test, harder than the entry. Unlucky = hull damage, add_stamina: -4 (crew pays the cost).

#### 6. The Run to Nassau

The return passage. The blockade is tighter. What the player carries determines what options they have. At least one passage on the open water between the Shallows and Nassau — weather, the Adamant's speed, the weight of what was recovered. Atmospheric. The player should feel the weight of the approaching reckoning.

Death passage available here: `death_shallows` — if the player failed the reef exit AND failed a luck test AND has `crew_fractured`, the Adamant breaks apart. Use `ending: true, ending_type: "death"`. The spec text for this ending:

> *The sea took her ten years ago. Today it takes you. The shallows hold the light differently down here — green and gold and very still. The Adamant is somewhere above the surface. Your crew will make for Nassau. Someone else will find the Red Correspondence eventually. You just won't be there to see it.*

---

## Tone Notes

- **No magic. No supernatural.** This is gritty pirate fiction.
- The wreck is beautiful and terrifying. Cold dark water. The San Cristóbal is a real ship — she has a name carved in her stern, a captain's log that's been underwater for ten years, a crest that's still legible under the marine growth.
- Pell appears throughout Act 3. He is the named crewman who leads dives, calls warnings, handles the Adamant when the player is below. He should feel real.
- The Red Correspondence matters. The fragment the player reads should be specific — a name, a sum, a date, a phrase that shows a man covering up a massacre with paperwork. Ashford did this. It should feel true.
- Act 3 is physical. It is cold water, heavy gold, burning lungs, and the sound of cannon in the distance. It should be written with sensory specificity.
- The transition to Act 4 should feel like coming up for air — Nassau on the horizon, what you're carrying, and the full weight of what comes next.

---

## Known Failure Modes — Avoid These

1. **Passage count shortfall.** The minimum is 70. Count before you finish. If you are at 55 passages, add fill — more recovery detail, an extra weather passage, more crew interaction on the return. A 40-passage act is a failure.

2. **Flag implementation too flat.** The Morrow arrival branch should genuinely change. `morrow_committed` is not just a text swap — Morrow is physically in the water alongside your crew. Write it as a scene. `morrow_rival` should feel dangerous. Make the branches earn their flag cost.

3. **Duplicate choice labels.** Never give two choices in the same passage the same `text` string. If two paths from one point use identical button text (e.g. both say "Dive"), differentiate them: "Dive first — check the cargo hold" vs "Dive first — find the captain's cabin."

4. **Inventing enemy IDs.** Use only the enemy IDs listed above. No new enemies.

5. **Skipping the narrative payoffs.** The spec requires specific narrative moments for items. The `captain_chart` must be read aloud. The `red_correspondence` must show a content fragment when opened. `dragons_breath` must be described in physical terms when recovered. Do not reference these items generically.

6. **Rushing the Morrow scenes.** The Morrow arrival is a major emotional beat. `morrow_committed` especially — this is the payoff for one of the hardest flag combinations to earn. Give it space.

7. **Tone drift toward fantasy.** No sea monsters, no supernatural events, no magic items. The danger is reef, depth, cold, rival captains, and Crown warships.

---

## Output Format

Output a single valid JSON object containing only a `"passages"` key:

```json
{
  "passages": {
    "s_1": { ... },
    "s_2": { ... },
    ...
  }
}
```

No preamble. No commentary. No markdown wrapper around the JSON. Just the JSON object.

The last passage(s) in the act should send the player to `r_1` (Act 4 start). Include any deaths as `ending: true, ending_type: "death"` passages within the act.

**Minimum: 70 passages. Target: 75–80 passages.** Count them.
