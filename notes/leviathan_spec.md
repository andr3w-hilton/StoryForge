# TIDE OF THE LEVIATHAN — EXPANSION SPEC v2.0

**Target:** 64 passages → ~300 passages  
**Engine:** StoryForge data-driven JSON gamebook  
**Passage schema:** Standard (choices / combat / test_luck / ending), all engine fields available  
**Current version baseline:** `tide_of_the_leviathan.json` v1.0, 64 passages, 17 flags set, 8 checked

---

## 0. DESIGN PRINCIPLES

1. Every flag that is set must be checked somewhere meaningful. No silent tracking.
2. Every item must have at least one explicit narrative moment — a scene that calls the item out by name and changes what happens because of it.
3. The six endings are not score-gated. They are path-gated: the player earns each ending by making specific decisions, not by being lucky in combat.
4. The existing 64 passages are a skeleton. Most will be retained, expanded, or re-numbered. New passages fill the bones.
5. Act 1 is exploration and characterisation. Act 2 is dread and revelation. Act 3 is escalating confrontation. Act 4 is consequence.

---

## 1. PASSAGE NUMBERING SCHEME

All passage IDs use a prefix system. The engine accepts any string ID.

| Prefix | Act | Range (approx) |
|--------|-----|----------------|
| `s_` | Act 1 — Saltmere | `s_1` … `s_60` |
| `r_` | Act 2 — The Sunken Reaches | `r_1` … `r_70` |
| `t_` | Act 3 — The Drowned Temple | `t_1` … `t_100` |
| `l_` | Act 4 — The Leviathan & Aftermath | `l_1` … `l_70` |
| `end_` | Endings (not counted toward totals) | `end_binding`, `end_sacrifice`, `end_warrior`, `end_bargain`, `end_drowned`, `end_hollow` |
| `death_` | Mid-adventure death passages | `death_sea`, `death_reef`, `death_temple`, `death_drowned` |

**Migration note:** All existing numeric IDs (`"1"`, `"2a"`, etc.) must be remapped to the new scheme before the expansion is written. The mapping is documented in Section 6.

---

## 2. FLAG ARCHITECTURE

### 2.1 Master Flag Table

Ten heavy flags drive the six endings and major branch unlocks. Eight carry over from v1.0 (some renamed); two are new.

| Flag | Set At | Checked At | What It Unlocks |
|------|--------|------------|-----------------|
| `saw_symbol` | `s_4` (harbour wall) | `s_22` (harbourmaster gives extra info), `t_45` (recognise a second symbol in the temple), `l_10` (understand the ritual inscription) | Unlocks `knows_the_pact` path in Act 4; gives +1 LUCK at `s_22` |
| `helped_kael` | `s_3d` (fought thugs) | `r_5` (Kael dives into wreck with you), `l_35` (Kael arrives in time at the climax) | Kael survives and is present for The Binding ending |
| `kael_survived` | `r_33` (Kael emerges alive from wreck dive) | `l_35` (timing of Kael's arrival), `end_binding` (condition check) | Required for The Binding ending |
| `spared_first_mate` | `r_28` (flee from first mate) or `r_30` (back away without fighting) | `l_15` (first mate's ghost answers you), `l_40` (ghost can hold the seal) | Required for The Binding ending; opens ghost-assist mechanic in Act 4 |
| `defeated_first_mate` | `r_32` (win the combat) | `r_33` (receive drowned key and compass together), `t_5` (memory vision triggers), `l_20` (ghost is hostile, not helpful) | Closes off The Binding ending's ghost-assist path; opens The Warrior's Reckoning path |
| `altar_destroyed` | `t_65` (smash the altar) | `t_70` (Morrow's weakened stat block triggers), `l_5` (aspect is less powerful), `l_55` (ending gate check) | Enables The Warrior's Reckoning ending; the aspect uses the weaker `the_leviathan_aspect_weakened` enemy |
| `knows_the_pact` | `t_52` (find ancient inscription) — only reachable if `saw_symbol` is set | `l_25` (offer the old pact to the aspect), `l_30` (aspect hesitates before attacking) | Required for The Ancient Bargain ending |
| `compass_intact` | `r_33` or `r_28b` (obtained compass without combat) | `l_8` (compass guides you to the binding chamber), `l_42` (socket is revealed), `end_binding` and `end_sacrifice` checks | The compass must be in inventory AND this flag set for the sealing endings |
| `morrow_heard` | `t_44` (read the journal in Morrow's sanctum) | `t_52` (inscription passage unlocks from Morrow's words), `l_25` (pact offer is coherent) | Gate for The Ancient Bargain path — you cannot offer a pact you have not heard described |
| `ritual_delayed` | `t_20` (disrupt the ritual chant early) — requires `sea_glass_amulet` | `t_22` (Morrow starts the boss fight at reduced stamina: 8 instead of 12), `l_5` (aspect weakened flag stacks) | Stacks with `altar_destroyed` for the easiest Morrow fight; not required for any ending |

### 2.2 Flag Interaction Map

```
saw_symbol ─────────────────────────────────────── knows_the_pact ──── end_bargain
                                                         ↑
                                               morrow_heard (also needed)

helped_kael ──── kael_survived ──────────────────────────────────────── end_binding (required)
                                                         ↓
spared_first_mate ──────────────────────────────── ghost assists ─────── end_binding (required)
                                                         ↓
compass_intact ─────────────────────────────────── sealing mechanic ─── end_binding / end_sacrifice

defeated_first_mate ─── ghost hostile ──────── blocks ghost-assist ─── blocks end_binding
                    └── drowned_key obtained ──────────────────────────── opens locked door

altar_destroyed ─────────────────────────────── weakened aspect ─────── end_warrior (required)
ritual_delayed ────────────────────────────── stacks with above ──────── same

(No flags met for sealing) ──────────────────── aspect fought at full ── end_warrior or end_drowned
```

### 2.3 Orphan Flags Resolved

The following v1.0 flags were set but never checked. This expansion gives each a home:

| Old Flag | Resolution |
|----------|-----------|
| `saw_symbol` | Now gates `knows_the_pact` (see above) |
| `helped_kael` | Now gates `kael_survived` sub-flag |
| `spared_first_mate` | Now gates ghost-assist mechanic |
| `defeated_first_mate` | Now gates ghost-hostile branch and extra item reward |
| `knows_first_mate` | Absorbed: Pell's dialogue in `s_2a` now sets `knows_first_mate`; it is checked at `r_18` (recognise the first mate on sight = skip shock stamina penalty) |
| `knows_kael` | Checked at `s_3`: if set, the approach text is different and Kael trusts you one level faster |
| `knows_warehouse` | Checked at `s_6`: if NOT set, player must succeed at a luck test to find the skiff inside |
| `has_skiff` | Now used at `r_1`: Kael's skiff vs. stolen skiff affects which departure passage triggers |

---

## 3. ITEM AUDIT — ALL ITEMS WITH EXPLICIT NARRATIVE PAYOFFS

Every item must have at least one passage where having it changes the text and outcome, not just stats.

| Item ID | Name | Explicit Narrative Use(s) |
|---------|------|--------------------------|
| `cutlass` | Cutlass | `s_3a` (fight thugs); `r_30b` (fight first mate as fallback); replaced if `wave_cutlass` acquired |
| `wave_cutlass` | Wave-Etched Cutlass | `t_45`: the wave-pattern resonates with the temple inscription, revealing the hidden text (same effect as `saw_symbol` but via item). `l_30`: the blade does not shatter when striking the aspect's coral-bone form (plain cutlass shatters at `l_30`, costs -1 SKILL for the aspect combat) |
| `flintlock_pistol` | Flintlock Pistol | `t_15`: one-shot ambush on a Tide Wraith blocking the passage — destroys it outright, skipping the combat entirely. Expended after use (item removed). If not fired here, can be used at `t_60` as a one-shot distraction to shatter a cultist's concentration during the ritual circle, giving +2 LUCK for the Morrow fight |
| `navigator_compass` | Navigator's Compass | `r_15` (guides through reef channels without stamina penalty); `l_8` (reveals path to binding chamber); `l_42` (fits socket in binding seal). Must be in inventory for `end_binding` and `end_sacrifice`. Removed when placed in seal at `end_binding` |
| `tide_chart` | Tide Chart | `r_5`: sailing with chart → safe passage + Kael points out the Windborne. Without chart → `r_7a` (hull damage, -3 STAMINA). `t_1`: the chart's low-tide window marks when the lower temple floor is exposed — without it, the player must fight through an extra passage of flooded combat |
| `grappling_hook` | Grappling Hook | `r_10` (scale wreck's tilted hull without luck test); `t_30` (traverse a collapsed passage by hooking across a gap — skips a Drowned Cultist fight); `l_12` (escape the collapsing temple — without it, player must succeed at a luck test or lose 4 STAMINA) |
| `drowned_key` | Drowned Key | `t_3` (unlocks the armoury side chamber); `t_38` (unlocks Morrow's private sanctum, giving morrow_heard flag opportunity) |
| `rum` | Saltmere Dark Rum | `r_22` (consumable: 3 STAMINA). Also has a narrative use at `r_18`: offering the rum to the half-aware first mate causes a moment of recognition that sets `knows_first_mate_awake` (a sub-flag) — this affects the `spared_first_mate` path and makes the ghost more coherent in Act 4 |
| `sea_glass_amulet` | Sea-Glass Amulet | `t_20` (disrupt ritual chant, sets `ritual_delayed`); `t_52` (the amulet glows near the ancient inscription, readable text becomes visible — alternative path to `knows_the_pact` without needing `saw_symbol`); removed on use at `t_20` |
| `provisions` | Provisions | Standard consumable (+4 STAMINA). Narrative use: at `t_55` (the temple's final corridor), a trapped survivor of the crew offers to trade information for food — if you have provisions, they give you the location of Morrow's sanctum, which skips a searching passage |

### 3.1 New Items Needed

Three new items to support expanded paths:

| Item ID | Name | Type | Description | Narrative Use |
|---------|------|------|-------------|---------------|
| `kelp_rope` | Woven Kelp Rope | tool | "A length of rope braided from enchanted kelp, stripped from the temple walls. Stronger than hemp." | `t_30` alternative to grappling hook for the gap traverse; also used at `l_12` escape (lighter than iron, no luck test needed) |
| `morrow_journal` | Morrow's Journal | quest | "A waterproof-sealed journal taken from Morrow's sanctum. His handwriting grows increasingly inhuman toward the end." | Sets `morrow_heard` when read at `t_50`. Required for knowing the ancient pact. Also gives +1 SKILL (tactical knowledge of the temple layout) |
| `ancient_seal_fragment` | Ancient Seal Fragment | quest | "A cracked stone disc carved with an inverted spiral — the same mark as the binding pillar. One half of something." | Found at `t_52`. Fits into the binding pillar socket at `l_42` as an alternative to the compass — enables `end_sacrifice` path where the compass is NOT used |

---

## 4. ACT STRUCTURE

### ACT 1 — SALTMERE (~60 passages, IDs: s_1 to s_60)

**Tone:** Urgency beneath mundane harbour-town texture. The player is a stranger with one day to act.

**The Spine (mandatory path, shortest route):**
`s_1` → `s_3` → `s_3a` (or `s_3b`) → `s_3d` → `s_3e` → `s_7` (depart)

A player who fights the thugs, allies with Kael, and sets sail without exploring will reach Act 2 in ~8 passages. This is valid but leaves them under-equipped and missing key flags.

**Key Beats:**

- `s_1`: Harbour arrival. Three hooks visible: tavern, docks altercation, harbour wall symbol. (Unchanged from v1.0, re-ID'd)
- `s_4`: Harbour wall symbol. Sets `saw_symbol`. Expanded: the fisherwoman has more to say — she has seen the symbol on her husband's body. Player can ask about the symbol's age (it predates the cult), which hints at the ancient pact.
- `s_2a`: Old Pell. Sets `knows_first_mate`, `has_tide_chart`. Expanded: Pell has a second scene (`s_2d`) if player returns after helping Kael — he gives a warning about the first mate that sets up the `spared_first_mate` path.

**Major Branch 1 — The Tavern Depth Branch (~12 passages: s_2 to s_2h)**

This branch expands Pell and the tavern's other occupants into a proper information-gathering hub.

- `s_2`: Drowned Anchor entry
- `s_2a`: Old Pell — tide chart + first mate warning + skill bonus. Existing.
- `s_2b`: Buy rum. Existing.
- `s_2c`: Pell's boat advice + chandlery tip. Existing.
- `s_2d` (NEW): Return visit after Kael allied — Pell gives extra warning about the first mate. Requires `kael_allied`. Sets `pell_warned_you` (makes first mate recognition scene in Act 2 less shocking — no stamina penalty).
- `s_2e` (NEW): The barkeep Marta's side scene — mentions three fishermen who came back changed. Player learns the cult's symbol is a ward as much as a beacon. Sets `knows_symbol_danger`.
- `s_2f` (NEW): A drunk sailor reciting drowned-priest liturgy in his sleep. Luck test to wake him — if awoken, he describes the inside of the temple from memory. Sets `knows_temple_layout` (gives one extra choice at `t_1`).
- `s_2g` (NEW): The cellar door. Requires `saw_symbol` for the instinct to check. A second cult symbol under the stairs + waterproof satchel with `sea_glass_amulet` (alternate acquisition).
- `s_2h` (NEW): Departure from tavern hub.

**Major Branch 2 — Kael and the Docks (~10 passages: s_3 to s_3h)**

- `s_3`: Dock confrontation. Three options. Existing.
- `s_3a`: Fight thugs (combat: dock_thug). Existing.
- `s_3b`: Talk thugs down (luck test). Existing.
- `s_3c`: Watch, skiff stolen. Existing.
- `s_3d`: Win fight, Kael allied. Sets `helped_kael`, `kael_allied`. Existing.
- `s_3e`: Kael briefed, agrees to sail. Existing.
- `s_3f`: Skiff stolen — Kael points to warehouse. Existing.
- `s_3g` (NEW): If `knows_kael` set (from Pell): Kael greets player with slight recognition. Trusts you faster, no persuasion needed. Merges into `s_3e`.
- `s_3h` (NEW): Kael's backstory scene — only after `kael_allied`, before departure. Sets `kael_told_story`. Checked at `r_5`: if set, Kael dives into the wreck with you.

**Major Branch 3 — Harlan's Warehouse (~8 passages: s_6 to s_6h)**

- `s_6` through `s_6f`: Existing passages (re-ID'd).
- `s_6g` (NEW): Harlan himself appears if player is noisy. Combat (dock_thug upgraded: SKILL 7, STAMINA 8). Win: take receipts showing cult paid to delay boats. Sets `knows_harlan_paid` — gives reputation bonus + +1 LUCK at `s_22`.
- `s_6h` (NEW): Escape from warehouse with skiff. Bridge to `r_1`.

**Major Branch 4 — Chandlery and Harbour Dressing (~8 passages: s_5 to s_5f)**

- `s_5` through `s_5c`: Existing (re-ID'd).
- `s_5d` (NEW): Old chandler Silas — if player buys both items, he shares his son's tide-window calculation. Sets `knows_tide_window` (gives extra action at `t_1` before the tide turns).
- `s_5e` (NEW): Second visit to chandlery — Silas sells the `kelp_rope` (washed up, "don't ask me where it came from").
- `s_5f` (NEW): Departure from chandlery.

**Minor Hub — Harbourmaster (~5 passages: s_20 to s_24)**

- `s_20`: Harbourmaster's office. Refuses to talk openly.
- `s_21`: Persuasion — requires `has_tide_chart` (show evidence) or `knows_harlan_paid` (show receipts).
- `s_22`: If persuaded — admits cult observation for weeks. Alternate `navigator_compass` acquisition. Gives +1 LUCK if `saw_symbol` is set.
- `s_23`: Harbourmaster refuses.
- `s_24`: Bridge back to main hub.

**Act 1 Departure Gate (~3 passages: s_55 to s_57)**

- `s_55`: Pre-departure moment at dusk. Summary of what player has gathered.
- `s_56`: Kael's skiff or stolen skiff? Branch based on flags.
- `s_57`: Bridge to `r_1`. Tone passage — last lights of Saltmere disappear.

---

### ACT 2 — THE SUNKEN REACHES (~70 passages, IDs: r_1 to r_70)

**Tone:** Dread and wonder in equal measure. The supernatural becomes undeniable. The personal stakes arrive.

**The Spine (mandatory path):**
`r_1` → `r_5` or `r_7a` → `r_8` → `r_14` → `r_16` → `r_70` (temple entrance)

**Major Branch 1 — The Windborne Wreck (~20 passages: r_15 to r_35)**

The emotional heart of Act 2. Source of the `spared_first_mate` / `defeated_first_mate` split.

- `r_15`: Approach wreck. Compass guides if held.
- `r_16`: Hull exterior. Three-way split: upper deck, lower hatch, leave.
- `r_18`: Upper deck. Compass found. `has_compass` + `compass_intact` set. If `knows_first_mate` set, no stamina penalty when player hears thumping below.
- `r_20`: Lower hatch descent.
- `r_22`: First mate encounter. Three options: reach out, draw weapon, back away.
- `r_24` (NEW): Reach out path. Rum can be offered here — sets `knows_first_mate_awake`. Brief recognition before Leviathan's hold reasserts.
- `r_25` (NEW): Recognition collapses — first mate lunges. If rum was offered at `r_24`, -1 STAMINA to first mate (grief made it hesitate).
- `r_26`: Fight path. Combat: drowned_first_mate.
- `r_28`: Spare path (back away). Sets `spared_first_mate`. First mate speaks a clue about the drowned key.
- `r_28b` (NEW): Pick up compass from flooded hold on the way out. Sets `compass_intact`.
- `r_30`: Win fight. Sets `defeated_first_mate`. Items: compass + drowned key. +1 SKILL from hardened resolve.
- `r_32` (NEW): Post-fight reflection. Short. Gates `t_5` memory vision in Act 3.
- `r_33` (NEW): Kael dives scene. Only if `kael_told_story`. She finds provisions satchel. Sets `kael_survived`. Conversation sets `kael_knows`.
- `r_35`: Leave wreck. Bridge to `r_50`.

**Major Branch 2 — The Drowned Town (~15 passages: r_40 to r_55)**

New branch. Submerged settlement between wreck and temple.

- `r_40`: Option to dive down (requires grappling hook or kelp rope to anchor safely; otherwise luck test).
- `r_42`: Submerged street. Air pockets in doorways.
- `r_44`: Town hall — a binding altar-stone at its centre with the inverted spiral. If `saw_symbol` set, player connects the symbols — sets `knows_the_pact` early. Otherwise noted but not understood.
- `r_46`: Tide Wraith inhabits the town hall. Combat or flee.
- `r_48`: Town hall chest — contains `ancient_seal_fragment`.
- `r_50`: Surface. Continue to temple.
- `r_52` (NEW): Reef shark encounter. Two sharks. Grappling hook deters one — fight only the other.

**Major Branch 3 — The Outcrop Guards (~10 passages: r_60 to r_70)**

Expanded from v1.0's passage 14/15 cluster.

- `r_60`: Outcrop approach. Three guards (expanded from two). Three approach options.
- `r_62`: Direct challenge. Sequential combat: drowned_cultist x2.
- `r_64`: Grappling hook bypass.
- `r_65`: Underwater swim. Reef shark combat or luck test.
- `r_66` (NEW): Kael creates a distraction (only if `kael_survived`). No combat needed. Sets `kael_helped_distraction`.
- `r_68`: Loot fallen cultist — `sea_glass_amulet` (if not held) and `drowned_key` (if not held).
- `r_70`: Top of stairs. Chanting audible. Descend.

---

### ACT 3 — THE DROWNED TEMPLE (~100 passages, IDs: t_1 to t_100)

**Tone:** Claustrophobic, escalating. The cult has fouled something ancient. The player's choices from Acts 1-2 visibly matter here.

**The Spine (mandatory path):**
`t_1` → `t_5` → `t_10` → `t_20` (or `t_25`) → `t_40` → `t_60` → `t_70` (Morrow fight) → `t_80` → `t_90`

**Key Beats:**

- `t_1`: Stairway descent. Air trapped at ceiling. Bioluminescent glow. Left fork (locked door) vs. right fork (chanting). If `knows_tide_window` set, player has awareness of exact time pressure.
- `t_3`: Locked armoury door. Requires `drowned_key`. `wave_cutlass` and `sea_glass_amulet` available. Expanded from v1.0's `17`.
- `t_5` (NEW): Memory vision. Only triggers if `defeated_first_mate`. Short, no choices. First mate's face in a barnacle-covered porthole. Gone in a moment. Sets `had_vision` (text variation at `end_warrior`).
- `t_10`: The Great Cavern first sight. Re-ID'd from v1.0's `18`.
- `t_12` (NEW): Cavern overview — player observes before acting. Can spot the rear passage leading toward the binding chamber. Sets `saw_rear_passage`.

**Major Branch 1 — The Ritual Disruption (~15 passages: t_15 to t_28)**

- `t_15`: Tide Wraith in east colonnade. If `flintlock_pistol` held: one-shot option to destroy it outright, skipping combat. Pistol expended.
- `t_18`: Past the wraith, in position to disrupt before Morrow notices.
- `t_20`: Sea-glass amulet disruption. Sets `ritual_delayed`. Removes amulet. Leads to Morrow confrontation.
- `t_22`: `ritual_delayed` check — Morrow's STAMINA reduced to 8 for the fight.
- `t_25`: Sneak behind Morrow. Existing logic.
- `t_28`: Pre-emptive backstab. Morrow takes -2 STAMINA before fight.

**Major Branch 2 — Morrow's Sanctum (~12 passages: t_38 to t_52)**

New branch. Only accessible via `drowned_key` (second lock) or by following a retreating Morrow.

- `t_38`: Sanctum door. Requires `drowned_key` OR Morrow fled and left it ajar.
- `t_40`: Sanctum interior. Bookshelves, charts, writing desk.
- `t_42` (NEW): Morrow's journal on the desk. Taking it adds `morrow_journal` to inventory.
- `t_44` (NEW): Reading the journal. Luck test: lucky = read quickly; unlucky = interrupted by cultist patrol (-2 STAMINA from fight but finish reading). Sets `morrow_heard`.
- `t_46` (NEW): Journal revelations. No choices. Morrow was a maritime historian who found evidence the Leviathan was originally a binding-god — a coastal guardian twisted by a rival cult's inversion of its worship. The current cult is inverting something once holy.
- `t_48` (NEW): Locked chest (no item required). Inside: `ancient_seal_fragment` (if not found at `r_48`), plus a map giving `saw_rear_passage` if not already set.
- `t_50` (NEW): Leave sanctum. If `morrow_heard` now set, passage text acknowledges the shift.
- `t_52` (NEW): Ancient inscription chamber. Reachable from sanctum map OR if `saw_symbol` + `sea_glass_amulet` led here. If `saw_symbol` set: player reads enough to understand the binding. If `morrow_heard` set: full comprehension. Sets `knows_the_pact`.

**Major Branch 3 — The Drowned Crew (~10 passages: t_55 to t_65)**

New branch. Other Windborne crew members converted by the cult.

- `t_55`: Player recognises a former crewmate in drowned cultist's robes. Fight or try to reach them.
- `t_57`: Barely conscious crewmate reveals Morrow's weakness: his connection to the altar stone. Gives tactical advantage at `t_65`.
- `t_59` (NEW): Second crewmate, fully drowned. Combat unavoidable.
- `t_60`: Trapped survivor passage. Existing provisions-trade scene.
- `t_62` (NEW): Corridor to altar. Three cultists. Options: fight, pistol distraction (if not used at `t_15`), alternate route via gap (requires `grappling_hook` or `kelp_rope`).
- `t_65`: Altar chamber. Smash option. Sets `altar_destroyed`. Cultists collapse. Morrow staggers.

**The Morrow Fight (~8 passages: t_70 to t_78)**

- `t_70`: Pre-fight dialogue. If `morrow_heard` set, player can quote the journal — Morrow flinches. Extra choice appears.
- `t_72`: Combat. Base: high_priest_morrow (SKILL 9, STAMINA 12). Modifiers: `ritual_delayed` → STAMINA 8; `altar_destroyed` → STAMINA 10; both → STAMINA 8; backstab at `t_28` → -2 STAMINA at start.
- `t_74`: Morrow defeated. Dying words vary by flags:
  - `knows_the_pact`: "You found the old words. Then you know what must be done."
  - `morrow_heard` only: "The journal... you read it. Good. Don't destroy what was never evil."
  - Otherwise: "It's too late. Nothing stops the tide."
- `t_75` (NEW): If `morrow_heard` AND `knows_the_pact`: Morrow describes the exact words of the pact. Sets `knows_pact_words`.
- `t_76`: Morrow dies. Green fire dims but doesn't go out. The deep water begins to rise.
- `t_78`: The aspect surfaces for the first time. Act 3 ends. Bridge to Act 4.

**Act 3 Minor Passages (~35 remaining)**

- Cultist patrol combats (3–4 passages each, ~15 passages total): tide wraith, drowned cultist, reef shark in a flooded sub-passage.
- Atmospheric wonder passages (2–3 passages): no combat, no choices — the temple's alien beauty. Tone-setting.
- False door / trap passages (4–6 passages): luck test or item-check to avoid stamina damage.
- The flooded library (4 passages): optional lore, minor item (clay flask of rum).
- The bone pit (3 passages): bones of drowned sailors. Emotional beat varies by `defeated_first_mate` vs `spared_first_mate`.

---

### ACT 4 — THE LEVIATHAN & AFTERMATH (~70 passages, IDs: l_1 to l_70)

**Tone:** The reckoning. Every flag pays off. The player discovers what kind of story they have been telling.

**The Spine (mandatory path):**
`l_1` → `l_5` → `l_10` → `l_20` → ending gate passages → endings

**Key Beats:**

- `l_1`: The aspect rises. Enormous. Ancient. The cavern shakes.
- `l_5`: Player takes stock — what do they have? What flags are set? This is the ending-routing hub. Multiple choices presented based on flags.

**Path A — The Sealing (leads to end_binding or end_sacrifice)**

- `l_8`: Compass spins. Pattern recognition. Requires `compass_intact`. If `saw_rear_passage` set, path to binding chamber known immediately. Otherwise, luck test.
- `l_10`: Cavern inscriptions. If `saw_symbol` + `knows_the_pact`: full understanding. If `morrow_heard` only: partial understanding with effort. If neither: trust the compass blindly.
- `l_12`: Flight through narrow passage. Aspect cannot follow. If `grappling_hook` or `kelp_rope`: automatic success. Without: luck test, failure costs 4 STAMINA.
- `l_14`: The binding chamber. The pillar with its inverted spiral. The socket.
- `l_15`: The ghost moment. If `spared_first_mate`: first mate's ghost is here. If `knows_first_mate_awake` (rum offered): ghost speaks, confirms compass will work. If `spared_first_mate` only: ghost is silent but gestures. If `defeated_first_mate`: chamber is empty.
- `l_16`: Aspect reaches the passage entrance. Time running out.
- `l_18`: ENDING GATE — The Binding. Requires: `compass_intact` AND `spared_first_mate` AND `kael_survived`. If all met: choice to place compass → `end_binding`.
- `l_20`: If `compass_intact` but conditions for Binding unmet: seal can still be made but costs more. Routes to `end_sacrifice`.
- `l_22`: If `ancient_seal_fragment` held: can use fragment instead of compass. Seal is weaker (Leviathan stirs again in a generation, not a century) but compass preserved. Also routes to `end_sacrifice` with different text.

**Path B — The Ancient Bargain (leads to end_bargain)**

Only accessible if `knows_the_pact` AND `knows_pact_words` both set.

- `l_25`: Player stands before the aspect. Speaks the words of the old pact instead of running or fighting.
- `l_26`: The aspect pauses. Its dead-sailor face-cloud shifts.
- `l_28`: Luck test. Lucky: the bargain holds immediately. Unlucky: aspect demands proof — compass offered (removes it) or blood offering (-4 STAMINA).
- `l_30`: If `wave_cutlass` held: blade resonates with ancient power. Aspect recognises it as a relic of the old order. Eliminates luck test at `l_28`.
- `l_32`: The bargain is struck. Aspect retreats. Routes to `end_bargain`.

**Path C — The Warrior's Reckoning (leads to end_warrior)**

Active if `altar_destroyed` is set.

- `l_35`: Kael arrives (only if `kael_survived` AND `helped_kael`). She distracts the aspect — player gets one free round before combat.
- `l_38`: Weakened aspect combat. Uses `the_leviathan_aspect_weakened` (SKILL 9, STAMINA 10). Without `altar_destroyed`, standard aspect (SKILL 11, STAMINA 16).
- `l_40`: If `spared_first_mate`: ghost of first mate enters. The aspect hesitates when it sees the ghost — player gets one free attack.
- `l_42`: Aspect is not destroyed — driven back. Retreats to sleep. Routes to `end_warrior`.

**Path D — The Drowned / Hollow Shore**

- `l_50`: Player without flags, health, or equipment to reach any other path. Aspect closes off exits.
- `l_52`: Final luck test. Lucky: player escapes to surface — but arrives too late. Routes to `end_hollow`. Unlucky or no attempt: aspect takes the player. Routes to `end_drowned`.

---

## 5. ENDING CONDITION MATRIX

### Ending 1 — The Binding (`end_binding`)
**Label:** Best victory. The seal holds. The ghost finds rest.

**Required:** `compass_intact` + `spared_first_mate` + `kael_survived` + (`knows_the_pact` OR `compass_intact`)

**Gate passage:** `l_18`

**Text beat:** The compass slots into the pillar. The ghost of the first mate places their hand over yours, then dissolves upward like sea spray into sunlight. Kael is on the surface, waiting. The Leviathan sleeps. The coast is saved for a generation.

**Engine:** `remove_items: ["navigator_compass"]`, `ending_type: "victory"`

---

### Ending 2 — The Sacrifice (`end_sacrifice`)
**Label:** Bittersweet victory. The seal holds, but the compass is gone and the player is alone.

**Required:** `compass_intact` + NOT (`spared_first_mate` AND `kael_survived`)

**Gate passage:** `l_20` or `l_22`

**Text beat:** The binding holds. There is no ghost to share the moment. The player walks back to Saltmere alone. Does not stay long. The compass is sealed in the deep. There is nothing left here.

**Engine:** `remove_items: ["navigator_compass"]`, `add_luck: -1`, `ending_type: "victory"`

---

### Ending 3 — The Warrior's Reckoning (`end_warrior`)
**Label:** Pyrrhic victory. The Leviathan is dormant, not sealed. It will return.

**Required:** `altar_destroyed` + Morrow defeated + aspect fought at `l_38`

**Gate passage:** `l_42`

**Text beat:** The aspect retreats. The temple collapses. Player swims out through the dark. Kael drags them clear (if she survived). Saltmere intact. But the player knows — and only the player knows — it will return. The sea is patient.

**Engine:** `ending_type: "victory"` (victory text explicitly marked "For now.")

---

### Ending 4 — The Ancient Bargain (`end_bargain`)
**Label:** Secret/discovery ending. The Leviathan reinstated as guardian.

**Required:** `knows_the_pact` + `knows_pact_words` (+ optional: `wave_cutlass` removes luck test)

**Gate passage:** `l_32`

**Text beat:** The Leviathan's aspect stills. A sound — not waves crashing, but something beneath waves, the deep vibration of the ocean's oldest heartbeat. The pact is reinstated. The thing in the deep is not a god of destruction but a guardian that was betrayed. It goes back to sleep. The coast is safe — not because you destroyed something, but because you understood it.

**Engine:** `add_luck: 2`, `ending_type: "victory"`

---

### Ending 5 — The Drowned (`end_drowned`)
**Label:** Death ending. Taken by the deep.

**Condition:** Failed `l_52` luck test or chose to keep running

**Gate passage:** `l_55`

**Text beat:** The player's face joins the cloud of drowned sailors within the aspect's form. Saltmere is swallowed by the tide.

**Engine:** `ending_type: "death"`

---

### Ending 6 — The Hollow Shore (`end_hollow`)
**Label:** Failure ending. Survived, but too late.

**Condition:** Lucky escape from `l_52` without having stopped the ritual

**Gate passage:** `l_52` lucky branch

**Text beat:** The player surfaces. The aspect did not take them. But Saltmere's lights are gone. On the shore: no boats, no smoke, no sound. The harbour is empty. Every window dark. The nets still in the water. The tide took everyone in the night. The player walks the empty streets until dawn. There is no one left to tell.

**Engine:** `ending_type: "death"` (failure classified as death per engine convention)

---

## 6. PASSAGE MIGRATION MAP (v1.0 → v2.0 IDs)

| v1.0 ID | v2.0 ID | Notes |
|---------|---------|-------|
| `1` | `s_1` | Unchanged |
| `2` | `s_2` | Unchanged |
| `2a` | `s_2a` | Unchanged |
| `2b` | `s_2b` | Unchanged |
| `2c` | `s_2c` | Unchanged |
| `3` | `s_3` | Unchanged |
| `3a` | `s_3a` | Unchanged |
| `3b` | `s_3b` | Unchanged |
| `3c` | `s_3c` | Unchanged |
| `3d` | `s_3d` | Unchanged |
| `3e` | `s_3e` | Unchanged |
| `3f` | `s_3f` | Unchanged |
| `4` | `s_4` | Unchanged |
| `5` | `s_5` | Unchanged |
| `5a` | `s_5a` | Unchanged |
| `5b` | `s_5b` | Unchanged |
| `5c` | `s_5c` | Unchanged |
| `6` | `s_6` | Unchanged |
| `6a` | `s_6a` | Unchanged |
| `6b` | `s_6b` | Unchanged |
| `6c` | `s_6c` | Unchanged |
| `6d` | `s_6d` | Unchanged |
| `6e` | `s_6e` | Unchanged |
| `6f` | `s_6f` | Unchanged |
| `7` | `r_1` | Departure is now Act 2 |
| `7a` | `r_7a` | Chartless sail |
| `8` | `r_5` | Chart-guided sail to wreck |
| `9` | `r_9` | Reef swim after hull breach |
| `10` | `r_16` | Wreck exterior |
| `10a` | `r_18` | Upper deck, compass found |
| `10b` | `r_19` | Grappling hook from rigging |
| `11` | `r_20` | Hatch descent |
| `11a` | `r_24` | Reach out to first mate |
| `11b` | `r_28` | Back away, spare first mate |
| `12` | `r_26` | Fight first mate |
| `13` | `r_30` | First mate defeated |
| `14` | `r_60` | Outcrop approach |
| `14a` | `r_64` | Grappling hook bypass |
| `14b` | `r_65` | Underwater swim / shark |
| `14c` | `r_66b` | Post-shark, slip past guards |
| `15` | `r_62` | Challenge guards |
| `15a` | `r_68` | Guards defeated, loot |
| `16` | `t_1` | Stairway descent |
| `17` | `t_3` | Armoury side chamber |
| `17a` | `t_3a` | Sea-glass amulet taken |
| `17b` | `t_3b` | Clay flasks taken |
| `17c` | `t_3c` | Wave cutlass taken |
| `18` | `t_10` | Great Cavern first sight |
| `18a` | `t_25` | Sneak behind Morrow |
| `18b` | `t_27` | Behind altar, two choices |
| `19` | `t_30` | Direct charge |
| `20` | `t_20` | Sea-glass amulet disruption |
| `21` | `t_28` | Backstab Morrow |
| `22` | `t_65` | Smash the altar |
| `22a` | `t_68` | Fight weakened Morrow |
| `23` | `t_74` | Morrow defeated |
| `24` | `l_38` | Fight the aspect (full) |
| `25` | `l_8` | Compass guides to binding chamber |
| `25a` | `l_16` | Hesitation at the socket |
| `26` | *(merged into `end_warrior` path)* | |
| `victory_seal` | `end_binding` | Now two separate endings |
| `victory_fight` | `end_warrior` | |
| `death_drowned` | `end_drowned` | |
| `death_sea` | `death_sea` | Unchanged |

---

## 7. NEW ENEMY DEFINITIONS

Two new enemy definitions required in the JSON `"enemies"` block:

```json
"high_priest_morrow_weakened": {
    "name": "High Priest Morrow (Weakened)",
    "skill": 8,
    "stamina": 8
},
"the_leviathan_aspect_weakened": {
    "name": "The Leviathan (Weakened Aspect)",
    "skill": 9,
    "stamina": 10
}
```

The engine picks the enemy definition based on which ID is referenced in the passage's `combat` block. The writer assigns the weakened version by routing flag-checks to separate combat passages.

---

## 8. PASSAGE COUNT SUMMARY

| Act | Target | Spine | Branch Passages | Total |
|-----|--------|-------|-----------------|-------|
| Act 1 Saltmere | ~60 | 8 | 52 | ~60 |
| Act 2 Reaches | ~70 | 10 | 60 | ~70 |
| Act 3 Temple | ~100 | 12 | 88 | ~100 |
| Act 4 Leviathan | ~70 | 15 | 55 | ~70 |
| Endings | 6 | — | — | 6 |
| Death passages | 4 | — | — | 4 |
| **Total** | **~310** | | | **~310** |

The ~10 passage buffer above 300 accommodates bridge passages and atmospheric text nodes.

---

## 9. WRITER GUIDANCE NOTES

**Tone consistency:**
- Act 1 is almost entirely mundane. Salt, rope, poverty, violence. The supernatural is rumour and cold water.
- Act 2 is the mundane cracking. The drowned town is beautiful and wrong in equal measure. The first mate scene is the emotional spine of the entire adventure.
- Act 3 is pressure. Less wonder, more dread. The temple is not evil by design — it is ancient and indifferent. The cult has fouled something old.
- Act 4 is earned. Every line of dialogue should feel like it matters. The aspect should feel impossibly large but not invincible.

**Flag-setting discipline:**
- Every `set_flags` must have a corresponding downstream `requires_flag` or `requires_no_flag` check, or a documented check in an ending condition. No flag should be set without a use.
- Flags are set on arrival (via passage-level `set_flags`), not inside choices.

**Item discipline:**
- When an item is used narratively, the text should say why having it changes things. "You hook the grappling iron into the coral above and haul yourself across the gap" — not just a mechanical bypass.
- Consumables (rum, provisions) should be described, not silent.

**Engine constraints:**
- A passage has exactly one of: `choices`, `combat`, `test_luck`, or `ending`.
- `add_items`, `remove_items`, `set_flags`, `add_stamina`, `add_skill`, `add_luck` apply on arrival, before rendering.
- Conditional choices use `requires_item`, `requires_flag`, and `requires_no_flag` on individual choice objects.
- There is no `requires_no_item` field — use a `requires_no_flag` pattern with a tracking flag (e.g., `has_compass`) if you need to gate on item absence.

**Validation:** After writing each act, run the passage validator from `CLAUDE.md` against the full adventure file to catch broken gotos and unreachable passages before proceeding to the next act.
