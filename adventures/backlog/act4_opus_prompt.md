# Black Flag Running — Act 4 Writing Prompt for Claude Opus

You are writing Act 4 (the final act) and all endings of a Fighting Fantasy-style gamebook adventure called **Black Flag Running**. The adventure is 248 passages through three completed acts. Act 4 must produce a **minimum of 65 passages** using the `r_` prefix, plus **all 8 ending passages** using the `end_` prefix and any remaining death passages. Total output minimum: **75 passages**. Count before finishing.

---

## Engine Schema

Passage object — exactly these fields:

```json
"r_1": {
    "text": "Narrative text. Use \\n for paragraph breaks.",
    "choices": [
        { "text": "Button label", "goto": "r_2" },
        { "text": "Requires item",  "goto": "r_3", "requires_item": "red_correspondence" },
        { "text": "Requires flag",  "goto": "r_4", "requires_flag": "nassau_rallied" },
        { "text": "Requires no flag", "goto": "r_5", "requires_no_flag": "morrow_rival" },
        { "text": "Danger style",   "goto": "r_6", "style": "danger" }
    ]
}
```

A passage has **one** of: `choices`, `combat`, `test_luck`, or `ending`. Not more than one.

```json
"combat": {
    "enemy": "ashford",
    "win_goto": "r_20",
    "flee_goto": "r_19",
    "flee_allowed": true,
    "flee_stamina_cost": 2
}

"test_luck": {
    "lucky_text": "...", "lucky_goto": "r_10",
    "unlucky_text": "...", "unlucky_goto": "r_11",
    "lucky_stamina_cost": 0,
    "unlucky_stamina_cost": 3
}

"ending": true,
"ending_type": "victory"
```

Arrival effects (apply before rendering):
```json
"add_items": ["morrow_seal"],
"remove_items": ["war_chest"],
"set_flags": ["nassau_rallied"],
"clear_flags": [],
"add_stamina": -3,
"add_luck": -1
```

**Rules:**
- Never give two choices in the same passage the same `"text"` string.
- Passage IDs: `"r_1"`, `"r_2"` etc. for Act 4. Endings: `"end_saviour_true"`, `"end_saviour"`, `"end_free_captain"`, `"end_deal"`, `"end_betrayal"`, `"end_pyrrhic"`. Deaths: `"death_betrayed"`, `"death_ashford"`.
- All endings and deaths use `"ending": true` with the appropriate `"ending_type"`.

---

## Enemies in the adventure JSON

- `naval_marine` — SKILL 7, STAMINA 6
- `naval_officer` — SKILL 8, STAMINA 8
- `rival_crew` — SKILL 6, STAMINA 6
- `morrow_enforcer` — SKILL 7, STAMINA 7
- `harbour_thug` — SKILL 5, STAMINA 5
- `morrow` — SKILL 8, STAMINA 9 (only on full morrow_rival path)
- `ashford` — SKILL 9, STAMINA 10 (direct combat path only)

Do NOT invent new enemy IDs.

---

## Items in the adventure JSON

- `cutlass` (weapon, skill_bonus: 1)
- `flintlock` (weapon, skill_bonus: 2) — **narrative use required in Act 4: a single shot that opens or ends the final confrontation**
- `red_correspondence` (key) — letters implicating Ashford
- `war_chest` (key) — Crown gold
- `dragons_breath` (weapon, damage_bonus: 1) — **narrative use required: explicit scene deploying explosive charges**
- `morrow_seal` (key) — Morrow's formal endorsement — **narrative use required: presented publicly at the rally, turns the crowd**
- `harbour_bond` (key) — Council's signed backing — **narrative use required: council resources arrive at a specific passage**
- `provisions` (consumable, stamina_restore: 4)

---

## Flag State Entering Act 4

**From Act 3 (may be set):**
- `red_correspondence_held` — player recovered the letters from the wreck
- `war_chest_held` — player recovered the war chest
- `crew_fractured` — crew loyalty broke during Act 3
- `morrow_cornered` (late set) — Morrow backed off under leverage at the Shallows

**From Acts 1–2 (may be set):**
- `crew_loyal` — full crew loyalty maintained
- `morrow_committed` — kept Morrow's secret with compassion (strongest ally path)
- `morrow_cornered` — used secret as leverage (reluctant ally)
- `morrow_ally` — base ally path from Act 1
- `morrow_rival` — Morrow is an enemy
- `morrow_secret_known` — knows about Morrow's history
- `ashford_contact` — back-channel open with Ashford
- `council_backed` — Harbour Council formally backs the player
- `council_burned` — Council refused or was betrayed

**Flags to SET in Act 4:**
- `nassau_rallied` — player successfully unites Nassau's captains
- `ashford_exposed` — Red Correspondence used publicly against Ashford
- `morrow_seal` (add_items) — Morrow gives her seal to the player at the rally

---

## Act 4 Structure

### Passage prefix: `r_`
### Minimum: 65 Act 4 passages + 8 endings + 2 deaths = **75 passages total**
### Start passage: `r_1`

---

### Spine

`r_1` — The Adamant returns to Nassau. Ashford's four ships have tightened the blockade — they are now in a line across the entire harbour mouth. The player arrives by the back channel at night.
→ What did you bring back? The scene establishes what the player is carrying.
→ The rally (or its absence). The critical political moment.
→ Confront Ashford — by leverage, bribe, direct assault, or deal.
→ Endings branch.

---

### Branch 1 — The Rally

The player calls Nassau's captains together. This is the pivot point of the whole adventure. Write it as a scene — the captains gathered on the fort's lower walls, the blockade ships visible in the harbour mouth, the player making their case.

**What determines whether the rally succeeds:**

A luck test is required at the core rally passage if the player has no allies. With allies, the test is bypassed or made favourable:

- `morrow_committed` → Morrow speaks unprompted. The crowd turns before the player finishes. Give Morrow a line of dialogue here — the first time in the adventure she has spoken *for* Nassau rather than *for herself*. If player has `morrow_seal` from Morrow, it is shown to the assembled captains here.
- `morrow_cornered` → Morrow is present but silent. She stands behind the player — visible, committed by obligation. She does not speak.
- `morrow_ally` → Morrow speaks. Brief, professional. It helps.
- `morrow_rival` → Morrow is not present. If `council_backed`, the Council's factor speaks instead.
- `council_backed` → The harbour bond (if held) is shown — the merchants' resources, visible, specific. Ships refitted, crews paid.
- `crew_loyal` → The Adamant's crew stands at the player's back, visible to the assembled captains. It is a small thing, but it is noticed.
- `crew_fractured` → The Adamant's crew is present but visibly diminished. Captains notice.

On success: set `nassau_rallied`.
On failure (luck test failed, no allies): the rally falls apart. Player still has other paths — but `end_saviour` and `end_free_captain` are closed.

**If `morrow_seal` is in inventory:** Morrow already gave it at the Shallows (morrow_committed path). Present it at the rally. The seal turns one wavering captain — a specific, named moment. Then set `nassau_rallied` without requiring a luck test on the morrow_committed path.

---

### Branch 2 — The Leverage Path (Red Correspondence)

Requires: `red_correspondence_held`

The player sends Ashford a message — or acts publicly. Two sub-paths:

**Public:** The Red Correspondence is read aloud in the harbour square. The letters' content is shown — not summarised, shown. Ashford's name, the date, the prize claim, the 214 men. Nassau's captains hear it. Ashford's ships begin to move by evening. Set `ashford_exposed`. Leads to `end_saviour` (with `nassau_rallied`) or `end_deal` (without).

**Private (requires `ashford_contact`):** A sealed copy of the first letter is sent to Ashford aboard one of his ships. The response comes by flag signal within the hour. His ships begin to stand down — not immediately, but the movement starts. Leads to `end_deal`.

The `flintlock` narrative moment should occur on the leverage path if the player attempts to board or confront Ashford directly — one shot, fired or not, that decides something.

---

### Branch 3 — The Bribe Path (War Chest)

Requires: `war_chest_held`

The Crown gold is heavy and specific. Write the chest being opened — the coin counted, the weight felt.

Two options:
- **Offer it to Ashford directly:** He takes it. He is not shamed. He is bought. His ships leave. Nassau survives — but it is an ugly survival. No `nassau_rallied` required. Leads to `end_free_captain` (if player then leaves Nassau) or folds into `end_deal`.
- **Use it to fund Nassau's defence:** Ships provisioned, crews paid. `council_backed` path benefits. Leads to `end_free_captain` if `nassau_rallied`.

---

### Branch 4 — The Direct Assault (Dragon's Breath)

Requires: `nassau_rallied` + `dragons_breath`

Nassau's ships engage Ashford's fleet. This is a naval battle passage — write it as one extended sequence, not a single combat node. The Dragon's Breath is deployed explicitly: sealed canisters, fired from a sloop's bow, the explosion described in physical terms (the smell, the shockwave, the sound).

Heavy cost. The Adamant takes damage. Player stamina loss. Possible death on this path if `crew_fractured`.

Leads to `end_pyrrhic`.

---

### Branch 5 — The Deal / Betrayal (Ashford Contact)

Requires: `ashford_contact`

**Deal path:** Player has the Red Correspondence and `ashford_contact`. Private exchange — player keeps the letters as insurance, Ashford withdraws publicly citing "changed strategic priorities." Both parties understand. Nassau survives under a secret that can never be spoken. Leads to `end_deal`.

**Betrayal path:** `ashford_contact` set, `nassau_rallied` NOT achieved. Player has nothing left — or chooses to take Ashford's original offer. The Correspondence (or its location) goes to Ashford. Nassau falls. Player escapes. `end_betrayal`. This path should not be easy to fall into accidentally — it requires the player to actively make the choice to hand it over.

---

### Deaths

**`death_betrayed`** — The player backed the wrong faction, has no allies, and Nassau's most dangerous party moves against them. Not Ashford — someone in Nassau. An ambush before the rally or before the confrontation. Write it as a betrayal by someone the player trusted, not as a random attack.

**`death_ashford`** — Captured attempting to board or negotiate with Ashford's flagship without sufficient leverage. Ashford's marines are efficient. The paperwork is done before sundown. Write the legal language — pirate taken in lawful action, etc. The Commodore's voice is heard, formal and final.

---

## The Endings

All eight endings must be written as full passages — not stubs. Each ending is the last thing the reader sees. Write them with weight. They must feel earned.

### `end_saviour_true` — The Saviour of Nassau *(true best ending)*
**Required flags:** `nassau_rallied` + `ashford_exposed` + `morrow_committed` + `council_backed`

This is the ending where the player did everything right — discovered Morrow's secret, chose compassion over leverage, rallied Nassau, and exposed Ashford publicly. Morrow is beside the player on the fort wall when the Crown ships withdraw. The spec text:

> *Nassau's captains stand on the fort walls and watch Ashford's ships withdraw. Morrow is beside you. She did not have to be — you gave her the choice, and she made it, and that is the difference between a republic that lasts and one that doesn't. The Red Correspondence is read aloud in the harbour square. Ashford's name is in every sentence. His ships are gone before the sun sets. Morrow steps back when it is over and looks at you with something that is not quite respect and not quite gratitude and says nothing at all. She doesn't need to. Nassau remembers who stood on the wall.*

Expand on this. Give it 150–200 words. This is the best ending — it must feel like the best ending.

### `end_saviour` — The Saviour of Nassau
**Required flags:** `nassau_rallied` + `ashford_exposed` + (`morrow_ally` OR `morrow_cornered` OR `council_backed`)

Nassau is saved. The Red Correspondence was read publicly. But Morrow is not beside the player — she is somewhere in the crowd, or she has already left the fort wall. The victory is real but it is not complete.

### `end_free_captain` — The Free Captain
**Required flags:** `nassau_rallied` + `war_chest_held` + NOT `ashford_contact`

The blockade breaks. Nassau cheers. The player stood on the Adamant's deck and watched the Crown's ships turn south. The war chest is in the hold. The crew are rich. Nassau is free — and it can be free without you. The player sails.

### `end_deal` — The Uneasy Truce
**Required flags:** `ashford_contact` + `red_correspondence_held`

No one is satisfied. The republic survives under the quiet weight of a deal that can never be spoken of. Ashford withdraws. The player keeps the letters as insurance. Both parties know exactly how this ends if either moves first. It is not justice. It is survival.

### `end_betrayal` — The Reckoning
**Required flags:** `ashford_contact` + NOT `nassau_rallied`

The Adamant clears Nassau on a running tide. The war chest is in the hold. The Red Correspondence is in Ashford's hands. Nassau is someone else's problem now. The player tells themselves that is what the sea asks of them. By the time land disappears, they almost believe it.

### `end_pyrrhic` — The Last Argument
**Required flags:** `nassau_rallied` + `crew_fractured` (direct assault path, Adamant lost)

The Adamant is gone. She burns at the mouth of the harbour. Ashford's ships are withdrawing in disorder. Nassau is free. The player swam ashore. They sit on the fort wall with nothing but what they are wearing and watch the republic celebrate and decide that is enough. It nearly is.

### `death_betrayed` — Taken Before Dawn
Someone the player trusted made one move. An ambush. Nassau goes on. It does not go on for the player.

### `death_ashford` — Flag and Rope
Ashford's marines are thorough. His paperwork is meticulous. The player's name will appear in the Crown's records as a pirate taken in lawful action on the waters of the Atlantic, sentenced and executed under articles of admiralty. Nassau will hear about it. Nassau will not come for them.

---

## Tone Notes

- This is the payoff for everything. Every flag the player earned, every loyalty they built or burned, lands here.
- Ashford must feel like a real antagonist — not a villain, a man protecting himself at enormous cost to others. If he speaks, he speaks like an officer. If he loses, he loses like one.
- The rally is the emotional centrepiece of Act 4. If `morrow_committed` is set, Morrow's speech is the highlight of the whole adventure. Give her a line that earns it.
- The `flintlock` must appear on at least one path — a single shot, the pistol named, the moment described.
- The `dragons_breath` must appear on the direct assault path — physical, specific, dangerous.
- The `morrow_seal` must be shown publicly at the rally if held.
- The `harbour_bond` resources must arrive at a specific passage if held.
- Act 4 tone: consequence. Things hold or break. Nassau's fate is decided. The ending must feel like a landing, not a stop.

---

## Known Failure Modes

1. **Passage count shortfall.** Minimum 75 total (65 r_ + 8 endings + 2 deaths). Count before finishing.
2. **Endings as stubs.** Every ending must be a full passage — 100 words minimum. These are the last thing the player reads.
3. **Duplicate choice labels.** Never two choices in the same passage with the same text.
4. **Inventing enemy IDs.** Use only the listed enemies.
5. **Skipping item narrative payoffs.** flintlock, dragons_breath, morrow_seal, harbour_bond all have required narrative moments. Do not skip them.
6. **Flat flag branching.** The `morrow_committed` rally scene is NOT just a text swap — Morrow speaks. Give her words. Make it different from the cornered/ally paths.
7. **Rushing the ending passages.** The endings are the reward. Write them fully.

---

## Output Format

Output a single valid JSON object containing only a `"passages"` key:

```json
{
  "passages": {
    "r_1": { ... },
    "r_2": { ... },
    ...
    "end_saviour_true": { "text": "...", "ending": true, "ending_type": "victory" },
    ...
    "death_betrayed": { "text": "...", "ending": true, "ending_type": "death" }
  }
}
```

No preamble. No commentary. No markdown wrapper. Just the JSON object.

**Minimum: 75 passages. Count them.**

Save the output to: C:\Users\ahilt\PycharmProjects\StoryForge\adventures\black_flag_running_act4_draft.json
