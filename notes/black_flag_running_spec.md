# Black Flag Running — Adventure Spec

**Author:** Andrew Hilton
**Genre:** HIGH SEAS
**Theme icon:** ⚓
**Accent colour:** `#8b6914` (weathered gold)
**Tone:** Black Sails — gritty, political, morally complex. No magic. Pirate slang over fantastical naming. Every faction has a legitimate position.

---

## Target Structure

```
Target: 0 passages → ~260 passages
Acts: 4 acts + endings + deaths
Passage ID scheme: a_ / n_ / s_ / r_ / end_ / death_
Start passage: a_1
```

---

## The Setup

You are the captain of **The Adamant**, a capable but unremarkable sloop with a crew who have sailed with you long enough to trust you — and long enough to watch you carefully. You are new to Nassau. Your reputation exists elsewhere. Here, you are an unknown quantity, and the factions of the Free Republic will measure you before they let you in.

You arrive to find Nassau holding its breath. **Commodore Ashford** of the Crown's Atlantic Fleet has positioned three warships at the mouth of the harbour. He is not bombarding — not yet. He is waiting for something. The blockade has been in place for eleven days.

The key to breaking it lies beneath the Shallows of Perdition, eight leagues south of Nassau — the wreck of the **San Cristóbal**, a Crown galleon that went down a decade ago carrying a war chest and a diplomatic pouch known as **the Red Correspondence**. The letters implicate Ashford himself in a fraudulent prize claim that cost two hundred sailors their lives. He cannot let them surface. Nassau's captains want the gold to fund a defence. You want both — and you want to know why **Captain Reyna Morrow**, Nassau's dominant voice, has been sitting on the San Cristóbal's location for three years without acting.

---

## Passage Numbering Scheme

| Prefix | Act | Setting |
|--------|-----|---------|
| `a_` | Act 1 | Nassau harbour and town — arrival, first contacts |
| `n_` | Act 2 | Nassau interior — politics, hunting the location, faction stakes |
| `s_` | Act 3 | The Shallows of Perdition — the wreck, recovery, pursuit |
| `r_` | Act 4 | Nassau under siege — rally, confrontation, endings branch |
| `end_` | Endings | Final resolution passages |
| `death_` | Deaths | Death passages |

---

## Character

```json
"character": {
    "skill_base": 6,   "skill_dice": 1,
    "stamina_base": 14, "stamina_dice": 2,
    "luck_base": 6,    "luck_dice": 1,
    "starting_items": ["cutlass", "flintlock", "captain_chart"],
    "starting_provisions": 4
}
```

---

## Items

| ID | Name | Type | Stats | Narrative purpose |
|----|------|------|-------|-------------------|
| `cutlass` | Cutlass | weapon | skill_bonus: 1 | Starting weapon, narrative use in Act 1 duel |
| `flintlock` | Flintlock Pistol | weapon | skill_bonus: 2 | Single decisive shot — narrative use in Act 4 to open or end a confrontation |
| `captain_chart` | Captain's Chart | key | — | Leads to the San Cristóbal. Required to enter the efficient recovery path in Act 3 |
| `red_correspondence` | The Red Correspondence | key | — | Letters implicating Ashford. Required for leverage ending and saviour ending |
| `war_chest` | Crown War Chest | key | — | The gold from the San Cristóbal. Required for bribe path and free captain ending |
| `dragons_breath` | Dragon's Breath | weapon | damage_bonus: 1 | Explosive charges recovered from the San Cristóbal's armoury. Narrative use in Act 4 naval confrontation |
| `morrow_seal` | Morrow's Seal | key | — | Morrow's formal endorsement of your captaincy. Required for best ending |
| `harbour_bond` | Harbour Bond | key | — | Merchant Council's signed backing. Required for council-funded defence in Act 4 |
| `provisions` | Provisions | consumable | stamina_restore: 4 | Standard |

---

## Enemies

| ID | Name | SKILL | STAMINA | Used in |
|----|------|-------|---------|---------|
| `naval_marine` | Crown Marine | 7 | 6 | Act 1 (dockside altercation), Act 4 boarding action |
| `naval_officer` | Naval Officer | 8 | 8 | Act 3 pursuit, Act 4 |
| `rival_crew` | Rival Pirate Crew | 6 | 6 | Act 2 ambush, Act 3 competing salvage |
| `morrow_enforcer` | Morrow's Enforcer | 7 | 7 | Act 2 (if player challenges Morrow too early) |
| `harbour_thug` | Harbour Thug | 5 | 5 | Act 1 optional encounter |
| `morrow` | Captain Reyna Morrow | 8 | 9 | Act 3 or 4 (only if fully rival path) |
| `ashford` | Commodore Ashford | 9 | 10 | Act 4 final confrontation (direct combat path only) |

---

## Master Flag Table

### Crew Loyalty — Build and Spend System

Crew loyalty is a resource built through early decisions and spent at high-stakes moments. It is not passive — the player must actively protect it or it erodes. Each spend either costs the flag or extracts a stamina/path penalty in lieu.

| Moment | Type | Mechanic |
|--------|------|---------|
| Act 1 crew introduction choices | Build → `crew_trusts_you` | Low-stakes early decisions about how you treat the crew |
| Act 2 night recon | Spend `crew_trusts_you` | With flag: recon succeeds cleanly. Without: luck test, stamina cost on failure |
| Act 2–3 threshold | Build → `crew_loyal` | Maintained by consistently backing the crew's interests. Set when `crew_trusts_you` holds through Act 2 |
| Act 3 the dive | Spend `crew_loyal` | With flag: crew dives willingly, full recovery possible. Without: forced dive, `crew_fractured` set, stamina penalty |
| Act 3 pursuit | Spend `crew_loyal` | With flag: crew fights smart. Without: `crew_fractured` set if not already |
| Act 4 final battle | Payoff or consequence | `crew_loyal` = effective. `crew_fractured` = weakened, `end_pyrrhic` more likely |

### Morrow's Secret — Three Response Paths

When `morrow_secret_known` is set, the player must choose how to handle the revelation. The response determines Morrow's final role and gates the ending tiers.

| Response | Flags set | Consequence |
|----------|-----------|-------------|
| Use as leverage — confront her privately | `morrow_cornered` | Morrow becomes a reluctant ally. She honours the deal but will not speak at the rally. Closes the true best ending. |
| Expose her to the Harbour Council | `council_backed` strengthened, `morrow_rival` forced | Destroys Morrow politically. Council fully backs you. Morrow is an enemy from this point. |
| Keep the secret — let her know you know, but won't use it | `morrow_committed` | The strongest Morrow path. She speaks at the rally unprompted and gives you her seal. Required for `end_saviour_true`. |
| Never discover the secret | No flag | Morrow remains neutral-to-ally depending on Act 1 choices — she never fully commits |

### Full Flag Table

| Flag | Set at | Checked at | What it unlocks |
|------|--------|------------|-----------------|
| `crew_trusts_you` | `a_` (crew introduction choices) | `n_` (night recon), builds toward `crew_loyal` | First loyalty tier; spend in Act 2 |
| `crew_loyal` | `n_` (maintained from `crew_trusts_you` through Act 2) | `s_` (willing dive), `s_` (pursuit), `r_` (battle effectiveness) | Core loyalty resource; spend in Acts 3–4 |
| `crew_fractured` | `s_` (forced dive or failed pursuit) | `r_` (weakened in final battle), `end_pyrrhic` more likely | Loyalty depleted — consequences in Act 4 |
| `morrow_ally` | `a_` (earn trust in Act 1) | `s_` (Morrow assists recovery), `r_` (Morrow at the rally) | Base ally path |
| `morrow_committed` | `n_` (keep Morrow's secret with compassion) | `r_` (Morrow speaks at rally unprompted, gives seal), `end_saviour_true` | Strongest Morrow path; required for true best ending |
| `morrow_cornered` | `n_` (use secret as leverage) | `r_` (Morrow is a reluctant ally — present but silent at rally) | Closes `end_saviour_true`; ally without full commitment |
| `morrow_rival` | `a_` or `n_` (challenge/undermine, or expose to Council) | `s_` (Morrow's crew contest the prize), `r_` (Morrow hostile) | Mutually exclusive with ally flags |
| `morrow_secret_known` | `n_` (investigate and discover her history with the San Cristóbal) | `n_` (response choice available), `s_` (wreck confrontation branch) | Unlocks the three-way response |
| `council_backed` | `n_` (Council formally backs you, or Morrow exposed to them) | `r_` (council funds defence), `end_saviour`, `end_saviour_true`, `end_free_captain` | Resources and ending gate |
| `council_burned` | `n_` (betray or ignore council) | `r_` (council refuses aid) | Closes council paths |
| `ashford_contact` | `n_` (player opens back-channel with Ashford) | `r_` (deal path available), `end_deal`, `end_betrayal` | Required for deal/betrayal endings |
| `knows_location` | `n_` (chart or intelligence acquired) | `s_` (efficient wreck entry) | Without it: blind search path, punishing |
| `red_correspondence_held` | `s_` (letters recovered from wreck) | `r_` (leverage against Ashford), `end_saviour`, `end_saviour_true`, `end_deal` | Public use = Ashford exposed; private = deal |
| `war_chest_held` | `s_` (gold recovered from wreck) | `r_` (bribe or fund defence), `end_free_captain` | Fund Nassau or take and run |
| `nassau_rallied` | `r_` (player unites Nassau's captains) | `end_saviour`, `end_saviour_true`, `end_free_captain`, `end_pyrrhic` | Required for all positive Nassau endings |
| `ashford_exposed` | `r_` (Red Correspondence used publicly) | `end_saviour`, `end_saviour_true` | Ashford withdraws to save himself |

---

## Ending Condition Matrix

| Ending ID | Label | Required flags | Type |
|-----------|-------|----------------|------|
| `end_saviour_true` | The Saviour of Nassau *(true best)* | `nassau_rallied` + `ashford_exposed` + `morrow_committed` + `council_backed` | victory |
| `end_saviour` | The Saviour of Nassau | `nassau_rallied` + `ashford_exposed` + (`morrow_ally` OR `morrow_cornered` OR `council_backed`) | victory |
| `end_free_captain` | The Free Captain | `nassau_rallied` + `war_chest_held` + NOT `ashford_contact` | victory |
| `end_deal` | The Uneasy Truce | `ashford_contact` + `red_correspondence_held` | victory |
| `end_betrayal` | The Reckoning | `ashford_contact` + NOT `nassau_rallied` | victory |
| `end_pyrrhic` | The Last Argument | `nassau_rallied` + `crew_fractured` (direct assault, Adamant lost) | victory |
| `death_betrayed` | Betrayed in Nassau | Wrong faction backed, no allies left | death |
| `death_ashford` | Taken by the Crown | Captured by Ashford's forces | death |
| `death_shallows` | Lost in the Shallows | Failed recovery at the San Cristóbal | death |

**True best ending note:** `end_saviour_true` requires the player to have discovered Morrow's secret AND chosen compassion over leverage — the hardest combination to achieve, rewarded with the most complete resolution. Players who use leverage get `end_saviour` instead, which is still a victory but Morrow is absent from Nassau's future.

**Fallback path:** A player who earns no flags and makes no alliances can still reach `end_deal` or a death ending — there is always a resolution available.

---

## Item Narrative Payoff Table

| Item | Narrative use (must occur in writing) |
|------|---------------------------------------|
| `cutlass` | Act 1: A dockside dispute that can be resolved by blade or words. The cutlass is named. |
| `flintlock` | Act 4: A single shot that opens or ends the final confrontation — the passage explicitly invokes the pistol. |
| `captain_chart` | Act 3: The chart is read aloud to the crew before the dive. Without it, the search is blind. |
| `red_correspondence` | Act 4: The letters are read or described — their content is shown, not just referenced. |
| `war_chest` | Act 4: The chest is physically present — offered, counted, or seized depending on path. |
| `dragons_breath` | Act 4: Used in the naval confrontation — explicit scene of deploying the charges. |
| `morrow_seal` | Act 4: Presented publicly during the rally — Morrow's endorsement turns the crowd. |
| `harbour_bond` | Act 4: The council's resources arrive at a specific passage when this item is held. |

---

## Act 1 — Arrival at Nassau (prefix: `a_`)

**Tone:** Atmosphere and establishment. Nassau breathes. It smells of tar, rot, and money. The blockade sits on the horizon like a threat no one wants to name first. Everyone is watching the new captain off the Adamant.

**Passage budget:**
```
Named new passages:   20
Fill passages:        35 minimum
─────────────────────
Act 1 minimum:        55
```

**Spine (mandatory path):**
`a_1` Arrive at Nassau harbour. The blockade ships are visible. A harbour pilot comes aboard.
→ `a_2` Dockside. First read of Nassau — who's in charge, what the mood is.
→ `a_3` The Broken Wheel tavern. First contact opportunity with Morrow's people or Harbour Council.
→ `a_` First faction choice: seek out Morrow, approach the Council, or ask around independently.
→ `a_` Learn about the San Cristóbal — the rumour exists before the detail.
→ Act 1 close: you know the blockade is tightening and the prize is real.

**Major branches:**

1. **The Morrow path** — Seek audience with Reyna Morrow. She tests you. You may earn `morrow_ally` here through a trust scene (help her with a problem, don't challenge her authority). Alternatively, a misstep sets `morrow_rival`. She holds the San Cristóbal location but won't confirm it yet.

2. **The Council path** — Approach the Harbour Council's representative. Merchants want numbers and assurances. Earn `council_backed` through a negotiation passage (no combat). The council knows the prize exists and knows Morrow won't use it.

3. **The independent path** — Ask around the harbour. Slower, less flagged, but surfaces `morrow_secret_known` earlier than the other paths if the player is persistent. A harbour thug encounter optional here.

4. **Crew passages** — 3–4 passages establishing the Adamant's crew and their mood. Choices here set `crew_trusts_you` if the player backs the crew's interests over personal convenience — specific moments: how you handle a crew complaint about provisions, whether you let a crewman go ashore when it costs you time, how you respond when Nassau's locals look down at your people. Small decisions that the crew notices. The flag is seeded quietly — the player should not feel they are filling a loyalty meter.

**Key beats:**
- `a_1`: The harbour entrance. The blockade ships are named — the *Crown's Justice*, *Fervent*, and *Resolve*. Three ships to Nassau's none.
- Dockside altercation: a Crown marine in civilian clothes is watching the Adamant. Confrontation optional. Combat uses `naval_marine`. Resolution here is a first test of the player's instincts.
- The Broken Wheel: central hub. Three NPCs present — a Morrow lieutenant, a Council factor, and an old sailor who knew the San Cristóbal's last captain. Only the sailor will talk freely.
- End of Act 1: the player knows the San Cristóbal is real, knows the location is hidden (Morrow has it or it's in the archive), and has made one significant faction contact.

---

## Act 2 — Nassau Politics (prefix: `n_`)

**Tone:** Pressure mounts. The blockade tightens. The factions reveal their real positions. Morrow's secret surfaces if the player digs. Ashford makes a private move.

**Passage budget:**
```
Named new passages:   25
Fill passages:        35 minimum
─────────────────────
Act 2 minimum:        60
```

**Spine:**
`n_1` Three days in Nassau. The blockade has moved closer. Morrow calls an open council.
→ The council is fractious — no one agrees on the San Cristóbal.
→ Player must acquire `knows_location` — through Morrow (ally path), a merchant archive (council path), or a bribed dockworker (independent path).
→ Optional: Ashford sends a private messenger. `ashford_contact` available here.
→ Optional: Investigation uncovers `morrow_secret_known`.
→ Act 2 close: player has the location and a fractured set of alliances. Time to sail.

**Major branches:**

1. **Morrow's secret** — Investigation passages reveal that Morrow was the first mate on a ship that found the San Cristóbal three years ago. She recovered one item — a partial copy of the Red Correspondence — and has been using it quietly, personally, to keep Ashford at bay. The full pouch is still on the wreck. She's been protecting herself, not Nassau. Sets `morrow_secret_known`. This is a revelation that can be used to leverage her (`morrow_ally` via different means) or confirm her as a rival.

2. **Ashford's offer** — A Crown messenger finds the player privately. Ashford will let the Adamant leave free and clear if the player brings him the Red Correspondence before anyone else can read it. Sets `ashford_contact`. This opens the deal and betrayal paths in Act 4.

3. **The ambush** — A rival crew (working for a Nassau captain who wants the prize for themselves) attacks the player. Combat with `rival_crew`. Outcome determines whether a secondary antagonist persists into Act 3.

4. **The archive** — A Council-path option: the Harbour Council's factor has an old naval survey that triangulates the San Cristóbal's position. Sets `knows_location` without Morrow's involvement. Also reveals the war chest's value in Crown gold — enough to fund Nassau's defence for a year.

5. **The secret revealed** — The revelation that Morrow recovered a partial copy of the Red Correspondence years ago and has been using it for personal protection rather than Nassau's defence. Discovery methods: bribed dockworker (independent path), a confrontation with Morrow (if `morrow_rival`), or a late-night search of harbour records (council path). Sets `morrow_secret_known`. Immediately followed by the response choice — three passages, one per path:
   - *"Use it."* → `morrow_cornered`. Morrow goes cold. She will help you — she has no choice — but she will never forgive it.
   - *"Tell the Council."* → `morrow_rival` forced, `council_backed` strengthened. Morrow is finished in Nassau politics. The Council owes you everything.
   - *"I won't use it."* → `morrow_committed`. A long beat. Morrow looks at you for a long time. Then: *"I'll be at the Shallows."* This is the moment the best ending becomes possible.

**Key beats:**
- The open council: Morrow speaks. She is measured, political, and clearly in control — but the player can read the cracks if `morrow_secret_known` is already set.
- The messenger scene: Ashford's offer is delivered in writing, hand-delivered at the Adamant's gangway. The player must decide immediately whether to send a reply.
- Morrow's secret revelation: the truth is she is protecting herself, not Nassau — and she knows it. The three-way response is the emotional centrepiece of Act 2. All three paths are written with weight. None of them are obviously correct.
- Act 2 close: the Adamant prepares to sail. Whoever the player has allied with sends something — a crewman, a resource, a warning. If `morrow_committed`, Morrow's ship is already gone from harbour when the Adamant departs. She left first.

---

## Act 3 — The Shallows of Perdition (prefix: `s_`)

**Tone:** Open water. Physical danger. The prize in reach. The Adamant's crew at full stretch. Other ships on the horizon. What the player finds in the wreck will decide everything.

**Passage budget:**
```
Named new passages:   30
Fill passages:        40 minimum
─────────────────────
Act 3 minimum:        70
```

**Spine:**
`s_1` The Adamant clears Nassau harbour at night, running without lights.
→ The passage south. Weather and navigation passages.
→ Find the San Cristóbal — requires `knows_location` for clean entry; blind search path available but punishing.
→ The dive and recovery. Crew loyalty tested. Two items available: `red_correspondence` and `war_chest`. Player may take both, or one, or be interrupted before they get a second.
→ Pursuit. Another ship appears — rival crew or naval patrol depending on flags.
→ Return to Nassau with whatever was recovered.

**Major branches:**

1. **The `knows_location` path** — Clean entry. The chart is read. `captain_chart` narrative moment here. The wreck is found in two passages. Crew morale is good.

2. **The blind search path** — Without `knows_location`, the search takes longer. Luck test involved. Crew takes a stamina hit from exhaustion. Risk of discovery by Ashford's patrol before recovery is complete.

3. **The dive** — The San Cristóbal is in 40 feet of water, partially intact. Crew must dive in shifts. If `crew_loyal`, they go willingly and the recovery is efficient. If NOT `crew_loyal`, there is hesitation — a passages-long negotiation or a penalty dive with injury risk.

4. **Morrow's arrival** — Morrow's ship appears at the wreck regardless of flags — but what happens depends entirely on the relationship built:
   - `morrow_committed`: She is already there. She dives with your crew. No confrontation — she has made her choice.
   - `morrow_ally` or `morrow_cornered`: She arrives and waits. A tense exchange. She will not interfere but she wants to know what you found.
   - `morrow_rival`: Her crew moves to take the prize. Confrontation: fight, negotiate, flee, or — if `morrow_secret_known` and not yet used — reveal it here as last-resort leverage (sets `morrow_cornered` late, partial benefit).
   - No Morrow flags set: She does not appear. The wreck is uncontested.

5. **The naval patrol** — If `ashford_contact` was set, Ashford's patrol is light — he is watching, not intercepting yet. If not, a heavier patrol threatens. Possible combat with `naval_officer` at sea.

6. **Dragon's Breath** — In the San Cristóbal's armoury there are sealed canisters of Dragon's Breath — ship-grade explosive charges, still sealed, still volatile. Taking them is risky. Not taking them closes one Act 4 option. Sets `dragons_breath` item if taken.

**Key beats:**
- The wreck itself: described in detail. She lies on her side. The Crown's crest is still visible on the stern. The cargo hold is accessible but the forward sections have collapsed.
- The war chest: heavy, stamina cost to move. Player can take it but it slows the Adamant on the return. Sets `war_chest_held`.
- The Red Correspondence: in a sealed brass tube in the captain's cabin. The player reads the first letter — Ashford's signature is on it, the date predates his commission, the content is briefly shown. Sets `red_correspondence_held`.
- Departure under fire: the return to Nassau should feel dangerous regardless of path. The blockade is tightening. The Adamant runs.

---

## Act 4 — The Reckoning (prefix: `r_`)

**Tone:** Consequence. Everything the player built now either holds or breaks. Nassau's fate is decided. The Adamant earns her name or loses it.

**Passage budget:**
```
Named new passages:   25
Fill passages:        40 minimum
─────────────────────
Act 4 minimum:        65
```

**Spine:**
`r_1` The Adamant returns to Nassau. Ashford's ships have closed the mouth of the harbour — three ships in line.
→ What did you bring back? The flags determine what paths are available.
→ Rally Nassau (or don't). `nassau_rallied` set here if the player succeeds.
→ Confront Ashford — via leverage, bribe, combat, or deal.
→ Endings branch.

**Major branches:**

1. **The Rally** — Player calls Nassau's captains together. `morrow_ally` means Morrow speaks for you. `council_backed` means the merchants back the defence financially. `morrow_seal` turns reluctant captains. Without allies, the rally fails — not every path requires it, but failure here closes `end_saviour` and `end_free_captain`.

2. **The Leverage path** — `red_correspondence_held`: player sends Ashford a private message with a copy of the first letter. He knows what is implied. He withdraws — not in defeat, but in self-preservation. Nassau is saved quietly. Sets `ashford_exposed` if done publicly. Leads to `end_saviour` (public) or `end_deal` (private with `ashford_contact`).

3. **The Bribe path** — `war_chest_held`: the gold is offered — either to Ashford directly (he takes it and leaves, privately) or used to fund a defence (ships provisioned, crew paid). The bribe path is efficient but unsatisfying. Leads to `end_free_captain` if Nassau is rallied and player sails after.

4. **The Direct Assault** — If the player has `nassau_rallied` and `dragons_breath` but neither prize, or chooses to fight regardless: Nassau's ships engage Ashford's fleet. Dragon's Breath used in a passage that must describe the charges explicitly. Heavy combat. Adamant may be lost. Leads to `end_pyrrhic`.

5. **The Betrayal** — If `ashford_contact` set and `nassau_rallied` not achieved: player can still take Ashford's original offer, handing over the Red Correspondence location or the pouch itself. Nassau falls. Player escapes. `end_betrayal`.

6. **Death passages** — `death_betrayed`: player is sold out by whichever faction they trusted least — ambushed before the rally. `death_ashford`: captured attempting to board or negotiate with Ashford's flagship. `death_shallows`: referenced here as an Act 3 death but also available if the player returns without recovering anything and has no allies.

**Key beats:**
- `r_1`: Nassau harbour at dawn. The three ships are in line. The Adamant slides in behind them, undetected — for now. The crew is watching the player.
- The rally passage: should feel like the best Black Sails speeches. Morrow or the Council speak if allied. Without them, the player speaks alone — luck test involved.
- Ashford confrontation: whether by letter, negotiation, or cannon. The Commodore should feel like a real antagonist — not a villain, a man protecting himself at enormous cost to others.
- The final choice (all positive endings): Nassau is saved. What do you do now? Stay and take Morrow's place, or sail. This choice is the last passage before the ending passages. It must feel earned.

---

## Endings

### `end_saviour_true` — The Saviour of Nassau *(true best ending)*
Nassau's captains stand on the fort walls and watch Ashford's ships withdraw. Morrow is beside you. She did not have to be — you gave her the choice, and she made it, and that is the difference between a republic that lasts and one that doesn't. The Red Correspondence is read aloud in the harbour square. Ashford's name is in every sentence. His ships are gone before the sun sets. Morrow steps back when it is over and looks at you with something that is not quite respect and not quite gratitude and says nothing at all. She doesn't need to. Nassau remembers who stood on the wall.
**ending_type:** victory

### `end_saviour` — The Saviour of Nassau
Nassau's captains stand on the fort walls and watch Ashford's ships withdraw. You exposed the Commodore before the whole harbour — the Red Correspondence read aloud by the Harbour Council's factor, witnessed by every captain who would later swear they heard it. Ashford had no choice. The republic survives. Morrow steps back. You step forward.
**ending_type:** victory

### `end_free_captain`— The Free Captain
The blockade breaks. Nassau cheers. You stood on the Adamant's deck and watched the Crown's ships turn south and knew you had done what you came here to do. The war chest is in your hold. The Adamant's crew are rich. Nassau is free — and it can be free without you.
**ending_type:** victory

### `end_deal` — The Uneasy Truce
Ashford got what he needed. Nassau got what it needed. Nobody is satisfied. The republic survives under the quiet weight of a deal that can never be spoken of publicly — Ashford withdraws, you keep the letters as insurance, and both parties know exactly how this ends if either one moves first. It is not justice. It is survival.
**ending_type:** victory

### `end_betrayal` — The Reckoning
The Adamant clears Nassau on a running tide. Behind you, Ashford's ships are moving into the harbour. You did not look back. The war chest is in your hold and the Red Correspondence is in Ashford's hands and Nassau is someone else's problem now. You tell yourself that is what the sea asks of you. By the time land disappears from the horizon, you almost believe it.
**ending_type:** victory *(player survives — Nassau does not)*

### `end_pyrrhic` — The Last Argument
The Adamant is gone. She burns at the mouth of Nassau harbour, Dragon's Breath still smoking in the water where she went down. Ashford's ships are withdrawing — three ships that came in a line and left in disorder. Nassau is free. Your crew swam ashore. You swam ashore. You sit on the fort wall with nothing but what you're wearing and watch the republic celebrate and decide that is enough. It nearly is.
**ending_type:** victory

### `death_betrayed` — Taken Before Dawn
You backed the wrong captain. That is all it was. Someone with more history and more loyalty than you ever had in this port made one move and the Adamant's crew was outnumbered before the sun came up. Nassau goes on. It does not go on for you.
**ending_type:** death

### `death_ashford` — Flag and Rope
Ashford's marines are thorough. His paperwork is meticulous. Your name will appear in the Crown's records as a pirate taken in lawful action on the waters of the Atlantic, sentenced and executed under articles of admiralty. Nassau will hear about it. Nassau will not come for you. The republic looks after itself first.
**ending_type:** death

### `death_shallows` — The San Cristóbal Keeps Her Own
The sea took her ten years ago. Today it takes you. The shallows hold the light differently down here — green and gold and very still. The Adamant is somewhere above the surface. Your crew will make for Nassau. Someone else will find the Red Correspondence eventually. You just won't be there to see it.
**ending_type:** death

---

## Introduction Text (for adventures/index.json and adventure JSON)

Nassau stinks of low tide and ambition. You smell it before you see the port — tar and fish and something underneath, a particular sweetness that means too many people living too close together without enough to lose.

The Adamant slips into harbour on the morning watch, and the first thing you see is not the fort or the market or the long row of ships stripped to their ribs — it is the three Crown warships sitting at the mouth of the bay, close enough that you can read their names. *Crown's Justice. Fervent. Resolve.* Three ships to Nassau's none. Commodore Ashford is patient. He has been here eleven days, your harbour pilot tells you. He has not fired a shot.

He is waiting for something.

You have come to Nassau for work. What you have arrived into is something larger — a free republic counting the hours until it stops being free, a sunken ship with secrets that could end a career or start a war, and four factions pulling in four directions with Nassau's future between them.

The Adamant's crew is watching you. The harbour is watching you. Somewhere above the waterline, the town is already deciding what kind of captain you are.

Your adventure begins on the deck of the Adamant, Nassau harbour, with the blockade on the horizon and the rest of it still ahead of you.

---

## Pre-Writing Checklist

- [x] Every flag in the master flag table has at least one "Checked at" entry
- [x] Every ending has a unique, achievable flag combination
- [x] Every item has a narrative use beyond stats
- [x] Best ending requires 4+ flags (nassau_rallied + ashford_exposed + morrow_committed + council_backed)
- [x] True best ending requires compassion over leverage — not achievable by pure optimisation
- [x] Fallback path exists — ashford_contact + any path reaches end_deal without requiring rally
- [ ] Adventure JSON skeleton created
- [ ] Act 1 written and merged
- [ ] Act 2 written and merged
- [ ] Act 3 written and merged
- [ ] Act 4 written and merged
- [ ] All endings reachable from start passage
- [ ] Flag audit clean
- [ ] start_passage: "a_1" set in adventure JSON
- [ ] index.json updated
