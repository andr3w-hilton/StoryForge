# Expansion Spec — The Scavenger of New Babylon Station
## v1.0 → v2.0 expansion

---

## Target Structure

```
Target: 57 passages → ~220 passages
Acts: 4 acts + 6 endings + 4 death passages
Passage ID scheme: s_ / h_ / e_ / b_
start_passage: "s_1"  ← MUST be added to adventure JSON top level
```

---

## Passage ID Migration Map

All existing numeric IDs are renamed. This table is the authoritative map.
When merging any act draft, cross-reference this table to ensure gotos are updated.

### Act 1 — s_ (Station / Market)
| Old ID | New ID | Description |
|--------|--------|-------------|
| `1` | `s_1` | Freeport Market |
| `2` | `s_2` | Gruub weapons dealer |
| `3` | `s_3` | Zara info broker |
| `7` | `s_4` | South cargo elevator / Harko territory |
| `7a` | `s_5` | Pay toll — through |
| `7b` | `s_6` | Bluff luck test |
| `7a_unlucky` | `s_7` | Failed bluff result |
| `7c` | `s_8` | Security office (paid/bluff-lucky route) |
| `7c_lucky` | `s_9` | Security office (bluff-lucky route) — merge with s_8, same content |
| `7d` | `s_10` | EMP grenade found in security office |

> Note: `7c` and `7c_lucky` have identical content. In the migration, merge them into a single `s_8`.

### Act 2 — h_ (Hab Ring / Maintenance Shafts)
| Old ID | New ID | Description |
|--------|--------|-------------|
| `6` | `h_1` | North shaft entrance — boot prints |
| `4` | `h_2` | Meet Voss |
| `4a` | `h_3` | Accept Voss |
| `5` | `h_4` | Decline Voss |
| `8` | `h_5` | Crawlway branches (left/right) |
| `9` | `h_6` | Service Corridor 7-Alpha — duct crawler |
| `9a` | `h_7` | Post-crawler — bulkhead door |
| `9b` | `h_8` | Force door — fails |
| `10` | `h_9` | Cargo Bay 12 |
| `10a` | `h_10` | Mutant stalker combat |
| `10b` | `h_11` | Search containers — repair kit + stim-pack |
| `11` | `h_12` | Bypass lock with repair kit |
| `11a` | `h_13` | Voss uses Imperial codes |
| `12` | `h_14` | Keycard entry |

### Act 3 — e_ (Engineering / Lower Decks)
| Old ID | New ID | Description |
|--------|--------|-------------|
| `12a` | `e_1` | Lower decks fork — Imperial comms heard |
| `13` | `e_2` | Cargo Bay 12 lower entry (mutant stalker path) |
| `13a` | `e_3` | Investigate Imperial comms |
| `13b` | `e_4` | Warn Voss — plan together |
| `13c` | `e_5` | Sneak past soldiers — luck test |
| `13d` | `e_6` | Fight Imperial soldier |
| `13e` | `e_7` | EMP grenade use |
| `13f` | `e_8` | Voss sabotages sensors |
| `13g` | `e_9` | Post-combat — soldier escapes with relay |
| `14` | `e_10` | Research Lab 7 — Void Compass on pedestal |
| `14a` | `e_11` | Check for traps |
| `14b` | `e_12` | Repair kit disables pressure plate — clean retrieval |
| `15` | `e_13` | Grab compass rough — alarm triggers |
| `16` | `e_14` | Run — soldiers block path |
| `16a` | `e_15` | Precursor hidden exit from lab |
| `16b` | `e_16` | Fight through soldiers |
| `16c` | `e_17` | EMP grenade escape |
| `16d` | `e_18` | Voss diversion |

### Act 4 — b_ (Bridge / Final Confrontation)
| Old ID | New ID | Description |
|--------|--------|-------------|
| `17` | `b_1` | Emerge into Cargo Bay 12 — Malachar waiting |
| `18` | `b_2` | Face Malachar |
| `18a` | `b_3` | Negotiate luck test |
| `18b` | `b_4` | Throw compass — run |
| `19` | `b_5` | Fight Malachar (solo) |
| `19a` | `b_6` | Fight Malachar (Voss assists — weakened) |
| `20` | `b_7` | Imperial enforcer combat |
| `21` | `b_8` | Malachar defeated |
| `22` | `b_9` | Escape to ship |
| `23` | `end_survivor` | Victory with Voss |
| `23a` | `end_lone_wolf` | Solo victory |

### Death passages (keep existing IDs)
`death_cornered`, `death_malachar`, `death_empty`, `death_station`

---

## Master Flag Table

Every flag that exists in the expanded adventure. Every row has at least one "Checked at" entry.
Flags from the original adventure are marked (existing). Flags to be removed are marked (remove).

| Flag | Set at | Checked at | What it means |
|------|--------|------------|---------------|
| `has_plasma_pistol` | `s_2` (existing) | `s_3` (gate: hide re-buy option) | Bought the plasma pistol |
| `zara_info` | `s_3` (existing) | `h_1` (gate: "follow boot prints" vs "investigate"), `s_3_resistance` context | Spoke to Zara |
| `resistance_contact` | `s_3` new branch | `end_resistance` gate | Zara hinted at an anti-Imperial network |
| `harko_deal` | `s_new_harko` | `b_new_harko_exit` gate | Made a deal with Harko for an extraction route |
| `met_voss` | `h_2` (existing) | `h_new_second_chance` (gate: second chance encounter) | Found Voss but not yet allied |
| `voss_allied` | `h_3` (existing) | `h_7`, `e_1`, `e_4`, `b_2`, `b_6`, `b_8`, `end_survivor`, `end_legend`, `end_resistance` | Voss is travelling with you |
| `has_voss_freq` | `h_new_freq` (new passage after h_3) | `e_new_signal` gate (signal choice after voss diversion) | Voss gave you his comm frequency |
| `sensors_sabotaged` | `e_8` (existing) | `b_new_voss_path1` (Voss finds gap, sets voss_survived), `b_new_cordon` (bypass option) | Voss fed false data to Imperial sensors |
| `alarm_triggered` | `e_9`, `e_13` (existing) | `b_new_patrol` (extra opposition in cargo bays), `end_pyrrhic` gate | Imperial cordon knows your position |
| `clean_retrieval` | `e_12` (existing) | `e_new_compass_vision` (unlocks attunement), `end_legend` gate | Took the compass without triggering alarm |
| `compass_attuned` | `e_new_compass_vision` | `b_2`/`b_3` new dialogue option, `end_legend` gate | Compass showed you a vision — Precursor coordinates |
| `emp_used` | `e_7`, `e_17` (existing) | `b_2` new Malachar dialogue line (his advance team went dark) | EMP grenade was used |
| `fought_imperials` | `e_6` (existing) | `b_2` new Malachar dialogue (he knows your face, references the fight) | Killed or fought Imperial soldiers in the lower decks |
| `voss_diversion` | `e_18` (existing) | `e_new_signal` (context passage before signal choice) | Voss ran a diversion to cover your escape |
| `voss_signalled` | `e_new_signal` | `b_new_voss_path1`, `b_new_voss_path2` | You sent Voss the rendezvous point |
| `voss_survived` | `b_new_voss_path1` or `b_new_voss_path2_success` | `end_legend`, `end_survivor`, `end_resistance` | Voss made it to the ship |

**Flags removed from original (spotted_imperials):** `spotted_imperials` — redundant with `fought_imperials`. Remove `set_flags` from `e_3`. It is never checked anywhere and adds nothing distinct.

**Total flags: 16.** All have at least one check point.

---

## Ending Condition Matrix

| Ending ID | Label | Required flags | Excluded flags | Notes |
|-----------|-------|---------------|----------------|-------|
| `end_legend` | The Legend | `clean_retrieval` + `compass_attuned` + `voss_survived` | — | Escaped clean, compass revealed Precursor site, Voss alive. Best ending. |
| `end_resistance` | The Cause | `voss_survived` + `resistance_contact` | — | Voss connects you to anti-Imperial network. Compass becomes more than treasure. Hidden path. |
| `end_survivor` | Survivor | `voss_survived` | `clean_retrieval` (end_legend takes priority) | Made it out with Voss. Solid victory. |
| `end_lone_wolf` | Lone Wolf | compass in inventory | `voss_allied` | Solo escape with compass. Current 23a. |
| `end_pyrrhic` | Pyrrhic | `alarm_triggered` | `voss_survived` | Escaped, barely. Malachar got something. Cost was high. |
| `death_empty` | Failure | (existing — escaped without compass) | — | Alive but empty-handed. Treated as failure ending. |

**Fallback path:** A player who takes no optional content (no Zara, no Voss, no Harko, no keycard, no repair kit) should still reach `end_lone_wolf` or `death_empty` — never a dead end.

**Gate priority at ending branch:** Check in order: `end_legend` first, then `end_resistance`, then `end_survivor`, then `end_lone_wolf`, then `end_pyrrhic`. Use `requires_flag` / `requires_no_flag` combinations to enforce this. Do not show multiple victory endings simultaneously.

---

## Item Narrative Payoff Table

Every item must have at least one passage where it is called out by name and changes what happens.

| Item ID | Name | Narrative use | Where |
|---------|------|---------------|-------|
| `vibro_knife` | Vibro-Knife | Used to cut through a seized ventilation iris blocking a shortcut in the maintenance shafts | New `h_` passage — shortcut branch |
| `plasma_pistol` | Plasma Pistol | Act 4: when wounded and outnumbered, a passage notes the plasma pistol's range advantage — player can open fire from cover rather than closing to melee. Gates a safer combat approach. | New `b_` passage |
| `void_compass` | Void Compass | Active: after `clean_retrieval`, shows a vision of Precursor coordinates. In Act 4, if `compass_attuned`, Malachar recognises what you've done with it and his tactics shift. | `e_new_compass_vision`, `b_2` dialogue |
| `security_keycard` | Security Keycard | Already gated at `h_7` / `h_14` — existing use is sufficient. | `h_7`, `h_14` |
| `repair_kit` | Repair Kit | Already gated at `h_7`, `h_12`, `e_11` — existing uses are sufficient. | existing |
| `stim_pack` | Stim-Pack | Act 4: a passage where you are wounded during the escape and explicitly use the stim-pack — described as the nano-healers engaging, not just a menu action. Gates a stamina recovery that keeps a near-dead run alive. | New `b_` passage |
| `data_chip` | Qeth Data Chip | In Research Lab 7: the Precursor chamber recognises the chip — it was keyed to this location by the Qeth archaeologists who mapped it. The chip decodes part of the chamber inscription. `remove_items: ["data_chip"]` — the chip is absorbed/spent. Feeds into `compass_attuned` if `clean_retrieval` is also set. | New `e_` passage in Lab 7 |
| `emp_grenade` | EMP Grenade | Already has two gated uses (`e_7`, `e_17`). The `emp_used` flag now also triggers a Malachar dialogue line. Sufficient. | existing |
| `provisions` | Ration Pack | Standard consumable. No narrative scene required. | — |

---

## Act Structure

---

### Act 1 — s_ (The Station)
**Tone:** Bustling, time-pressured. Factions visible. Player building their toolkit and reading the board before descending.

**Passage budget:**
```
Migrated passages:   10   (s_1 through s_10)
Named new passages:   6   (s_3a, s_harko_meet, s_harko_accept, s_harko_decline, s_colour_1–3)
Fill passages:       19   (connective tissue, market exploration, extra Harko branch beats)
─────────────────────────
Act minimum:         35
```

**Spine (minimum path):**
`s_1` → `s_4` (elevator) or `h_1` (shafts) → Act 2

**Existing passages retained:** `s_1` through `s_10` (see migration map)

**New passages to write (35 minimum total):**

#### s_3 extension — Zara and the resistance
After Zara's existing speech, add a choice:
- "Ask about the network" (requires no flag, always available)
  → New passage `s_3a`: Zara studies you for a long moment. She mentions, briefly, that there are people — not Empire, not Harko — who have an interest in Precursor artefacts not ending up in Bureau hands. She gives you nothing actionable, just a name to drop if you find the right ears. Sets `resistance_contact`. Returns to travel choices.

#### s_new_harko — Harko proper
After paying the toll (`s_5`) or getting through via bluff, a new choice becomes available:
- "Ask to speak with Harko directly" (always available on the south path)
  → New passage `s_new_harko`: Harko is not what you expected. He operates from a converted shipping container office — organised, pragmatic, and visibly unhappy about an Imperial corvette being two hours from his station. His business depends on Imperial indifference. He will make a deal: you bring him whatever intelligence you find down there about Malachar's intentions, and he will have a tunnel route open for your extraction — bypassing the main docking ring entirely. No toll on the way out. Sets `harko_deal`.
  - This should feel like a genuine alliance of convenience, not charity.
  - One choice: accept the deal → sets `harko_deal`, returns to travel.
  - One choice: decline → returns to travel without flag.

#### s_new_station_colour (~3-4 atmospheric passages)
Optional branch from `s_1`: the market edge. A refugee family, a dead scavenger being carried out of a side corridor, a PA announcement crackling with static. These passages add atmosphere, optionally yield flavour information about the lower decks, and reconnect to the main paths. No flags set. Purpose: pacing and tone-setting for Act 1.

**Key beats:**
- `s_1`: Market (existing — add PA announcement reference and optional market-edge branch)
- `s_2`: Gruub (existing)
- `s_3` + `s_3a`: Zara + resistance option (existing + new)
- `s_4`–`s_10`: Harko territory (existing + new Harko meeting branch)
- All paths converge to either `h_1` (north shafts) or `h_5` (crawlway, via Harko's south tunnels connecting to the maintenance levels)

---

### Act 2 — h_ (The Hab Ring / Maintenance)
**Tone:** Tightening. Darkness pressing in. The station's history surfacing. Something wrong in the lower levels.

**Passage budget:**
```
Migrated passages:   14   (h_1 through h_14)
Named new passages:   7   (h_new_freq, h_new_second_chance + outcomes, h_new_vibro_knife, h_new_terminal, h_new_stalker_win)
Fill passages:       29   (flooded section, dead scavenger, extra crawler, shaft collapse, connective tissue)
─────────────────────────
Act minimum:         50
```

**Spine (minimum path):**
`h_1` → `h_5` → `h_6` or `h_9` → bulkhead → `h_14` or `h_12`/`h_13` → Act 3

**Existing passages retained:** `h_1` through `h_14` (see migration map)

**New passages to write (50 minimum total):**

#### h_new_freq — Voss gives his comm frequency
New passage inserted after `h_3` (accept Voss), before `h_5`.
- A quiet beat as you descend together. Voss checks his signal scrambler, mentions that if you get separated he needs a way to find you. He gives you a comm frequency — seven digits scratched on a scrap of foil, old Imperial field protocol. Sets `has_voss_freq`.
- This passage should feel like natural character work. The frequency is almost an aside. He says: "If we get split up — use that. Short burst, encrypted. Don't broadcast."
- One choice: "Continue into the shafts" → `h_5`.

#### h_new_second_chance — Voss in trouble (met_voss but not voss_allied)
New passage reachable from a new branch in Act 2's maintenance corridors.
- Requires `met_voss` + NOT `voss_allied`.
- You find Voss cornered by two of Harko's enforcers — they've caught a squatter in their territory and are collecting. He has his weapon drawn but is outnumbered.
- Choices:
  - Intervene (fight or intimidate the enforcers) → Voss is freed. "You came back." Sets `voss_allied` + `has_voss_freq` (he gives it immediately, grateful). Continue.
  - Walk past — not your problem → continue alone.
- This is the last chance to pick up Voss. After this passage, `voss_allied` cannot be set.

#### h_new_vibro_knife — shortcut through the iris
New passage in the maintenance shaft network.
- A sealed ventilation iris — a circular mechanical valve, seized with corrosion — blocks a shorter route to the cargo bay level. 
- Requires `vibro_knife` (starting item — always available): cut through the oxidised locking ring. The blade was built for this. Takes two minutes and costs effort but saves ten minutes of crawling. `add_stamina: -1`.
- Alternative: go around (no cost, but no shortcut).
- Both routes converge at `h_9` (Cargo Bay 12).

#### h_new_terminal — station history
New optional passage in the maintenance corridors near the cargo bays.
- A still-powered terminal in a wall junction. Station Authority records — partial duty logs from five years ago, just before the garrison pulled out. Entries from a warrant officer who found something in the lower research labs. "The artefact in Lab 7 is not inert. Recommend immediate lockdown and Bureau notification." Last entry: "Bureau notification sent. Bureau response: ignore it."
- No mechanical effect. Sets scene for Act 3 Precursor content. One choice: continue.

#### h_new_shaft_expanded (~10-15 passages)
Expanded exploration of the maintenance shaft network between `h_5` and the bulkhead. Currently the path is very linear. New branches:
- A flooded section requiring a detour (atmospheric, minor stamina cost)
- A second duct crawler encounter (optional — player can avoid it)
- Discovery of a dead scavenger — no items, but their notes indicate someone else was looking for the compass recently (and didn't make it)
- A shaft collapse that forces a choice between two routes to the cargo bays

All branches reconnect before the bulkhead.

**Key beats:**
- `h_1`: Shaft entrance / boot prints (existing)
- `h_2`: Meet Voss (existing)
- `h_3`: Accept Voss (existing) → immediately to `h_new_freq`
- `h_new_freq`: Comm frequency exchange (new)
- `h_4`: Decline Voss (existing)
- `h_new_second_chance`: Last chance for Voss (new, requires `met_voss` + NOT `voss_allied`)
- `h_5`: Crawlway branches (existing)
- `h_6`–`h_8`: Service Corridor 7-Alpha, duct crawler, bulkhead (existing)
- `h_9`–`h_11`: Cargo Bay 12, mutant stalker, container loot (existing)
- `h_12`–`h_14`: Bulkhead bypass routes (existing)
- Exit: all paths converge into `e_1`

---

### Act 3 — e_ (Engineering / Lower Decks)
**Tone:** Alien. Ancient. The compass is real and it knows you're here.

**Passage budget:**
```
Migrated passages:   18   (e_1 through e_18)
Named new passages:   5   (e_new_data_chip, e_new_compass_vision, e_new_compass_fragment, e_new_signal, e_new_signal_sent)
Fill passages:       42   (expanded lower deck exploration, Precursor sub-chambers, additional Imperial encounters, atmosphere)
─────────────────────────
Act minimum:         65
```

**Spine (minimum path):**
`e_1` → `e_3` or `e_10` → `e_12` or `e_13` → `e_new_signal` or direct to Act 4

**Existing passages retained:** `e_1` through `e_18` (see migration map)

**New passages to write (65 minimum total):**

#### e_new_data_chip — the chip is recognised
New passage in Research Lab 7, before the compass is taken.
- Inserted as an optional beat after `e_10` (enter the lab) and before `e_11`/`e_12`/`e_13`.
- Requires `data_chip` in inventory (always present — player starts with it).
- As you approach the pedestal, the Precursor chamber responds to the data chip in your pocket. The chip was not just a map — it was a key, encoded by the Qeth archaeologists who found this place. It pulses with the same silver light as the compass. The chamber inscription becomes partially legible: coordinates, star patterns, a destination.
- `remove_items: ["data_chip"]` — the chip melds into the pedestal reader and dissolves.
- This passage connects: if you then take the compass cleanly (`e_12`), the compass's vision (`e_new_compass_vision`) is richer because of this interaction.
- One choice: continue to the compass.

#### e_new_compass_vision — attunement
New passage, reachable only after `e_12` (clean retrieval — `clean_retrieval` is set).
- The compass is in your hands. No alarm. The silver veins pulse slowly, almost breathing.
- And then it shows you something. Not a word, not an image — a feeling of location. A star. A dead system three jumps from here, outside Imperial charts. A signal still broadcasting from a Precursor installation that has been transmitting for ten thousand years and waiting for someone to answer.
- If `data_chip` was used (i.e. `remove_items` on `data_chip` has fired): the coordinates lock in with precision. You know exactly where to go.
- Sets `compass_attuned`.
- One choice: "Pocket the compass and move" → `e_14` (escape begins).

#### e_new_compass_fragment — partial vision (alarm path)
New passage, reachable after `e_13` (alarm triggered — rough grab).
- Much shorter. The compass flares and goes dim, overwhelmed by the alarm. You feel a ghost of something — a direction, a distance — but it's gone before it resolves. It was trying to show you something.
- Does NOT set `compass_attuned`. Atmospherically hints at what a cleaner retrieval might have yielded.
- One choice: "Run" → `e_14`.

#### e_new_signal — the signal choice
New passage. Inserted after `e_18` (voss_diversion). This is structurally critical — wire it exactly as specified.

Passage text: Voss disappeared around a corner and you heard gunfire, drawing the soldiers away. The route ahead is clear. You have maybe three minutes before they realise the distraction is one man and come back for you.

In your pocket is a comm unit. In your head is a seven-digit frequency.

Choices:
```
{ "text": "Signal Voss — send him the rendezvous point",
  "goto": "e_new_signal_sent",
  "requires_flag": "has_voss_freq" }

{ "text": "Run — trust him to find his own way out",
  "goto": "b_1" }
```

**`e_new_signal_sent`:** Short passage. You key in the frequency and transmit a single burst — cargo bay 12, floor hatch, ten minutes. The comm clicks. No reply. Either he heard it or he didn't.
Sets `voss_signalled`.
One choice: "Move" → `b_1`.

**Key beats:**
- `e_1`: Lower decks fork (existing — Imperial comms heard)
- `e_2`–`e_9`: Imperial encounters, sensor sabotage, EMP, fight (existing)
- `e_10`: Research Lab 7 entry (existing)
- `e_new_data_chip`: Chip recognition (new, in lab)
- `e_11`–`e_12`: Trap check + clean retrieval (existing)
- `e_new_compass_vision`: Attunement (new, after clean retrieval)
- `e_13`: Rough grab / alarm (existing)
- `e_new_compass_fragment`: Partial vision (new, after alarm grab)
- `e_14`–`e_18`: Escape from lab, Voss diversion (existing)
- `e_new_signal` + `e_new_signal_sent`: Signal choice (new, after diversion)

---

### Act 4 — b_ (The Bridge / Final Confrontation)
**Tone:** Consequence. Every decision lands. The bill comes due.

**Passage budget:**
```
Migrated passages:   11   (b_1 through b_9, end_survivor, end_lone_wolf)
Named new passages:  13   (b_new_pa, b_new_harko_exit, b_new_patrol, b_new_compass_reveal, b_voss_gate, b_new_voss_path1/2, b_new_voss_extract, b_new_voss_rescued, b_new_stim_pack, death_extraction)
Ending gate chain:    5   (end_gate_1 through end_gate_3b)
New endings:          4   (end_legend, end_resistance_give/keep, end_pyrrhic)
Fill passages:       17   (Malachar confrontation variants, escape route branches, atmosphere)
─────────────────────────
Act minimum:         50
```

**Spine (minimum path):**
`b_1` → `b_2` → fight or negotiate → escape → ending

**Existing passages retained:** `b_1` through `b_9`, `end_lone_wolf` (was `23a`)

**New passages to write (50 minimum total):**

#### b_new_pa — Malachar docks
New passage inserted at the top of Act 4, before or during `b_1`.
- As you emerge into Cargo Bay 12, the station PA crackles. Automated docking confirmation: "Imperial corvette *Relentless* — docking bay seven — clearance granted." Then Malachar's voice, calm and broadcast station-wide: "This is Inquisitor Malachar of the Imperial Bureau of Antiquities. This station is now under Imperial jurisdiction. All persons in possession of artefacts of Precursor origin are ordered to surrender immediately. Non-compliance will be treated as sedition."
- He's here. Time is up.
- One choice: "Keep moving" → continue to `b_1` content.

#### b_new_patrol — alarm makes escape harder
If `alarm_triggered`: a new branch in Cargo Bay 12 adds an Imperial patrol blocking the direct route to the exit. Player must fight, sneak (luck test), or use `harko_deal` to reroute.

#### b_new_harko_exit — Harko's smuggling tunnel
New passage, requires `harko_deal`.
- Available as an alternative exit from Cargo Bay 12, bypassing the main docking ring entirely.
- Harko's man is waiting at a specific container stack — a nod to the earlier deal. A narrow tunnel runs behind the station's outer skin, connecting to a private docking collar. The Sable Moth is three minutes away.
- This route avoids the Malachar confrontation entirely IF `alarm_triggered` is set. If NOT `alarm_triggered` (quiet run), Malachar finds you anyway at your ship — confrontation is unavoidable regardless.
- Mechanical effect: saves 1–2 stamina from not fighting through the patrol. Sets up cleaner escape.

#### b_new_voss_path1 — Voss finds the gap (sensors sabotaged)
New passage, requires `voss_signalled` + `sensors_sabotaged`.
- Malachar's men are scanning the wrong section. There's a gap in the cordon. Voss, who knows Imperial patrol patterns from three years in the guard, finds it.
- He appears at the cargo bay floor hatch, breathing hard but intact. "Signal worked. Sensors had them chasing ghosts in sector nine."
- Sets `voss_survived`.
- One choice: "To the ship — together" → `b_9`.

#### b_new_voss_path2 — Voss is pinned (signalled but no sabotage)
New passage, requires `voss_signalled` + NOT `sensors_sabotaged`.
- Voss got the signal. But the cordon is tight. You can hear him through the comm — two corridors over, taking fire, pinned behind cover.
- Choices:
  ```
  { "text": "Fight through to him",
    "goto": "b_new_voss_extract" }
  { "text": "Tell him to find another way — keep moving",
    "goto": "b_2" }
  ```

**`b_new_voss_extract`:** Combat passage — Imperial enforcer standing between you and Voss.
- `combat: { enemy: "imperial_enforcer", win_goto: "b_new_voss_rescued", flee_goto: "death_extraction", flee_allowed: false }`

**`b_new_voss_rescued`:** You broke through. Voss is on his feet, one arm bloodied but functional. "Didn't think you'd come back." Sets `voss_survived`. One choice: "To the ship" → `b_9`.

**`death_extraction`:** New death passage. You tried to reach him and the cordon closed around you both. The ending Malachar's men write.

#### b_2 extension — Malachar dialogue variants
The existing Malachar confrontation passage needs dialogue additions based on flags:
- If `emp_used`: Malachar mentions his advance team went dark. "You used an EMP. Resourceful. Messy." He is not surprised, but he is noting it.
- If `fought_imperials`: "You killed two of my soldiers in the lower decks. I want you to know I noticed." His tone is the same — cold — but he's clocked you as a real threat.
- If `compass_attuned`: New choice available: "Tell him what the compass showed you." → New passage `b_new_compass_reveal`: You describe the coordinates. Malachar goes very still. He has been hunting Precursor sites for thirty years and he has never found a live transmission. The pause before he speaks is the longest of the encounter. This shifts the negotiation — he wants the information, not just the artefact. Opens a new non-combat resolution branch leading to `end_pyrrhic` (he lets you go but keeps the compass coordinates — a deal, of sorts) or `b_5`/`b_6` if the player refuses to deal.

#### b_new_stim_pack — stim-pack scene
New passage, triggered if player's stamina is low (design note: place this as a choice option available when entering a combat passage at low stamina, requires `stim_pack` in inventory).
- You pull the stim-pack and hit the injector into your neck. The nano-healers flood your system in a cold wave. The pain recedes. You are not healed — you are suspended. But you are functional.
- `remove_items: ["stim_pack"]`, `add_stamina: 4`.
- One choice: "Fight" → continue to combat.

#### Ending passages

**`end_legend`** — requires `clean_retrieval` + `compass_attuned` + `voss_survived`
Voss finds you in the cockpit as the FTL drive spools up. You show him the coordinates in the compass — the star three jumps out, the transmission that has been broadcasting for ten millennia. He is quiet for a long time. Then: "That's not a treasure. That's a map to something that was waiting for us." You engage the drive. Stars stretch. The compass pulses, warm, certain, pointing the way. This is what you came for. This is more than you expected.

**`end_resistance`** — requires `voss_survived` + `resistance_contact` (check in order: end_legend first)
Checked after end_legend. Voss, aboard and alive, recognises the name Zara gave you. He makes a call on his encrypted comm. Three hours out from New Babylon, a ship drops out of FTL alongside you — old hull, no markings. They want the compass. Not to sell it. To use it. To put Precursor technology into hands that won't burn worlds with it. Voss looks at you: "Your call." The choice is yours. This ending has two final branches: hand it over (joining the cause) or decline (keep the compass, part as allies). Both are victories. Both are earned.

**`end_survivor`** — requires `voss_survived`, not `clean_retrieval`/`compass_attuned` (end_legend took priority if those are set)
The existing `23` passage content, updated to `end_survivor`. Voss is alive. The compass is yours. You made it. The stars burn.

**`end_lone_wolf`** — requires compass in inventory, NOT `voss_allied`
The existing `23a` passage content, unchanged. Solo. Sufficient.

**`end_pyrrhic`** — requires `alarm_triggered` + NOT `voss_survived`
You escaped. You are alive. But the station is behind you, lit up with Imperial activity, and the person who ran the diversion that saved your life isn't on your ship. The compass pulses in your hand — warm, alive, pointing somewhere. You will follow it. But the cost of this run will stay with you.

---

## New Enemies

No new enemy types required. The existing set covers Act 4 needs. Confirm before Opus writes that these IDs are available: `security_drone`, `imperial_soldier`, `mutant_stalker`, `imperial_enforcer`, `inquisitor_malachar`, `malachar_weakened`, `duct_crawler`.

---

## New Items

No new items required. All narrative payoffs use existing items.

---

## Prose Style Notes for Opus

- Second person, present tense. "You push through the crowd." Not "You pushed."
- Short paragraphs. White space. The original adventure's voice is spare and precise — no florid description.
- Science fiction but grounded. The station is decaying and functional, not sleek. Empire is bureaucratic and brutal, not gothic.
- Voss speaks in clipped sentences. Military habit. He's not cold — he has a conscience — but he doesn't waste words.
- Malachar speaks with the patience of someone who has never needed to hurry. He is not theatrical. He is efficient.
- Harko is pragmatic and surprisingly reasonable. He is not a cartoon villain. He has been running this operation for fifteen years and he is good at it.
- The compass is ancient and alien. When it does something, describe it in physical sensation — warmth, pressure, a sound below hearing — not magical glowing effects.

---

## Validation Requirement (for Opus, after each act)

After writing each act, run the passage validator with the act's start ID and the known external passage IDs (death passages + passages from other acts that are referenced). Fix all errors before submitting the draft.

`start_passage` for each act:
- Act 1: `s_1`
- Act 2: `h_1`
- Act 3: `e_1`
- Act 4: `b_1`

Known external passage IDs (cross-act gotos that are valid):
- From Act 1 to Act 2: `h_1`, `h_5`
- From Act 2 to Act 3: `e_1`
- From Act 3 to Act 4: `b_1`
- Death passages (always valid): `death_cornered`, `death_malachar`, `death_empty`, `death_station`, `death_extraction`
- Endings (always valid): `end_legend`, `end_resistance`, `end_survivor`, `end_lone_wolf`, `end_pyrrhic`

---

## Pre-Writing Checklist

- [x] Every flag has at least one "Checked at" entry
- [x] Every ending has a unique, achievable flag combination
- [x] Every item has a narrative use beyond stats
- [x] Best ending (`end_legend`) requires 3 flags — feels earned
- [x] Fallback path exists: player who misses everything reaches `end_lone_wolf` or a death ending
- [x] `start_passage: "s_1"` must be added to adventure JSON before Act 1 merge
- [x] Voss thread wired: `has_voss_freq` → `voss_signalled` → `voss_survived` → ending gates
