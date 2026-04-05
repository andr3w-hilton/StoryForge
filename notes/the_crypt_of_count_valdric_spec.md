# The Crypt of Count Valdric — Expansion Spec

## Target structure

```
Target: 43 passages (existing) → ~200 passages
Acts: 3 acts + 5 endings
```

| Act | Prefix | Status | Passages | Description |
|-----|--------|--------|----------|-------------|
| Act 1: Village + Upper Crypt | `v_` | Done (re-prefixed) | v_1–v_14 | Village approach, Sera meeting, upper crypt, chapel, Aldric |
| Act 2: Lower Crypt | `c_` | Partial — c_1–c_11 exist, c_20+ new | ~35 new | Deeper lower crypt, Aldric's second appearance, pact revelation, Sera's Act 2 role |
| Act 3: The Sealing Chamber | `k_` | New | ~50 new | Sealing ritual, 5 divergent endings |

**start_passage:** `v_1` (already set)

---

## Passage ID migration map (complete)

| Old ID | New ID | Act |
|--------|--------|-----|
| 1–14 | v_1–v_14 | Act 1 |
| 15, 15a, 15b, 15c | c_1, c_1a, c_1b, c_1c | Act 2 |
| 16–20 | c_2–c_6 | Act 2 |
| 21–25 | c_7–c_11 | Act 2 |
| 26 | end_sealed | Act 3 |
| death_riddle, death_wraith, death_flee_valdric | unchanged | — |

---

## Master flag table

| Flag | Set at | Checked at | What it unlocks |
|------|--------|------------|-----------------|
| `met_sera` | v_2 | c_35 | Sera recognises you in Act 2 |
| `sera_allied` | v_3a | c_35, c_36 | Sera follows into lower crypt |
| `helped_sera` | c_1a, c_1b | c_35, k_finale, end_pact_broken | Sera survives into Act 3 |
| `met_aldric` | v_11 | c_21, c_22 | Unlocks Aldric's second appearance with full pact revelation |
| `aldric_warned_candle` | v_11a | v_11b (already wired) | already ✓ ok |
| `aldric_warned_wraith` | v_11b | c_30 | Stealth/awareness option in inner halls |
| `read_priest_note` | v_9 | c_22 | Unlocks deeper lore from Aldric (he knew the priest) |
| `saw_vision` | v_18 | k_ritual | Vision guides the sealing ritual |
| `candle_used` | c_9 | k_finale, end_freed, end_pact_broken | Ritual fire for pact-breaking |
| `wraith_destroyed` | c_5b | c_30 | Inner halls cleared — gating choice |
| `knows_the_pact` | c_22 or c_40 | k_pact_ritual, end_freed, end_pact_broken | Player understands Valdric's pact |
| `sera_knows_truth` | c_37 | k_finale, end_sera_stays | Sera knows the history, stays by choice |

**2 new flags:** `knows_the_pact`, `sera_knows_truth`

---

## Ending condition matrix

| ID | Label | Required flags | Notes |
|----|-------|----------------|-------|
| `end_sealed` | The Tomb Resealed | None — fallback path | Basic victory, curse lifts slowly, Aldric stays trapped |
| `end_freed` | The Ghosts Released | `met_aldric` + `knows_the_pact` + `candle_used` | Aldric and all trapped souls freed, full healing |
| `end_cursed` | The New Warden | NOT `candle_used` (beat Valdric raw) | Player slowly takes on the curse, becomes new crypt guardian |
| `end_sera_stays` | Her Choice | `sera_allied` + `helped_sera` + `sera_knows_truth` | Sera chooses to remain as warden, player leaves free |
| `end_pact_broken` | The Pact Broken | `sera_allied` + `helped_sera` + `knows_the_pact` + `candle_used` + `wraith_destroyed` | Best ending: pact fully broken, all freed, Ashford healed permanently |
| `death_ring_claim` | Claimed | NOT `knows_the_pact`, NOT `candle_used` + luck test fail | Ring overwhelms the player during sealing — Act 3 death |
| `death_valdric_surges` | The Count Returns | NOT `knows_the_pact` + NOT `met_aldric` + luck test fail | Valdric's spirit surges back during incomplete ritual — Act 3 death |

**Rules for ending gates in k_:**
- Check flags in order from most-requiring to least — best match wins
- `end_sealed` is the unconditional fallback — always reachable
- `end_pact_broken` is the "good ending" in Fighting Fantasy tradition — requires 5 flags
- Both Act 3 death endings are gated behind luck tests — uninformed players face real risk in the ritual room, informed players have a safe path

---

## Item narrative payoff table

| Item | Existing use | New narrative moment |
|------|-------------|---------------------|
| `sword` | Starting weapon | `c_30`: Valdric's aura blunts iron — plain sword breaks on the vault approach; only silver or consecrated weapons hold |
| `torch` | Entry flavour | `c_20`: north archway is unlit; torchlight reveals inscription invisible in darkness |
| `silver_dagger` | Fight wraith | Already has narrative moment ✓ |
| `holy_water` | Destroy wraith | Already has narrative moment ✓ |
| `blessed_candle` | Weaken Valdric | Already has narrative moment ✓ |
| `iron_key` | Open iron door | Already has narrative moment ✓ |
| `healing_herbs` | Given to Sera | Already has narrative moment ✓ |
| `signet_ring` | Grabbed and sealed in one passage | `k_ritual`: sealing/breaking the ring is its own 3-passage scene — the ring resists, fights back, must be mastered |

---

## Act 1 — Summary (existing, v_)

Already written. 23 passages (v_1–v_14, with sub-passages).

**Spine:** v_1 (road/campfire) → v_3 (crypt entrance) → v_4/v_5 (ghoul or spider) → v_6/v_5a (burial hall or skeleton chamber) → v_8/v_9 (chapel, iron key, priest note) → v_11 (Aldric) → v_13 (lower crypt staircase)

**Key flag beats:**
- v_2: sets `met_sera`
- v_3a: sets `sera_allied`
- v_9: sets `read_priest_note`; gives `iron_key`
- v_11: sets `met_aldric`
- v_11a: sets `aldric_warned_candle`
- v_11b: sets `aldric_warned_wraith`
- v_18: sets `saw_vision`

**Exits to Act 2:** v_13 → c_1 (Sera wounded in treasury) or v_14 (iron key shortcut) → v_10 → c_1 area

---

## Act 2 — Structure (c_)

### Existing passages (c_1 through c_11)

**c_1** — Sera wounded in treasury (if `met_sera` or `sera_allied`, she recognises you)
- c_1a: Give healing herbs → sets `helped_sera`
- c_1b: Share provisions → sets `helped_sera`
- c_1c: Leave her → no flag

**c_2** — Pillared corridor, skeleton warrior combat → c_3

**c_3** — Circular chamber (3 existing exits):
- c_4: Vision room → sets `saw_vision` → c_3
- c_5: Wraith encounter → c_5a (silver dagger combat → c_7) or c_5b (holy water → sets `wraith_destroyed` → c_7)
- c_6: Fungus passage luck test → c_7
- **NEW 4th exit:** "Explore the north archway" → **c_20** (new Act 2 content)

**c_7** — Vault approach corridor ("all paths converge here…")
- Currently: one choice → c_8
- **After expansion:** add flag-gated choice for Sera joining if `sera_allied` + `helped_sera`; can also arrive via c_45

**c_8** — Vault entrance / Valdric confrontation
**c_9** — Candle combat (count_valdric_weakened) → c_11; sets `candle_used`
**c_10** — No-candle combat (count_valdric) → c_11
**c_11** — Valdric defeated, signet ring found → currently goes to end_sealed

> **After expansion:** c_11 leads to **k_1** (Act 3: Sealing Chamber) instead of end_sealed.
> The existing `end_sealed` passage becomes one of the k_ endings.

---

### New Act 2 passages (c_20 through c_50)

**Entry:** c_3 (add 4th choice → c_20)

#### c_20 — North archway
*The north archway is unlit — deeper than the other passages. Torchlight (or no light) reveals a carved inscription above the arch: "BENEATH THE SEAL LIES THE WORD THAT MADE IT."*

- If player has `torch`: inscription is legible, they understand its significance (no mechanical effect yet, payoff in k_)
- Choices: proceed through archway → c_21 | return to circular chamber → c_3

#### c_21 — The inner antechamber
*A high-vaulted chamber, cold and absolutely silent. Two features: a stone lectern holding a sealed iron casket, and a sarcophagus with "ALDRIC, COURT HISTORIAN" carved on its lid — the sarcophagus from v_11, but accessed from below.*

- If `met_aldric`: Aldric's ghost appears here — he followed you down (→ c_22 dialogue)
- If NOT `met_aldric`: Only the iron casket is accessible (→ c_40 document route)
- Choices: Speak to Aldric [requires_flag: met_aldric] → c_22 | Examine the iron casket → c_40 | Return → c_20

#### c_22 — Aldric's revelation
*Aldric appears in his second and final form — more present, more urgent. He's been watching you since v_11. He knows you're close to the vault.*

*If `read_priest_note`: "You found Brother Cavel's note. He was the last one who tried. He knew the truth — he wrote it down somewhere. Did you read it?" → deeper branch → c_23*

*Core revelation regardless:*
- Valdric did not become a necromancer through talent alone. He made a pact with the Lady of Bones — undeath in exchange for service. When the people sealed him, it broke the pact's terms. The Lady cursed him further — he cannot die a second death while the ring exists, and the ring cannot be destroyed while he lives. A loop. The original sealing only paused it.
- Simply resealing the ring again will pause it again — another century, maybe. But the pact will eventually erode the seal.
- **To break the pact:** the ring must be used to reseal the tomb with the blessed candle's fire as witness — not as a weapon against Valdric, but as a ritual component in the sealing chamber.

*Sets `knows_the_pact`*

- Choices: Ask about the sealing ritual → c_25 | Ask about the Lady of Bones → c_24 | Ask about the priest [requires_flag: read_priest_note] → c_23 | Thank him and head for the vault → c_45

#### c_23 — The priest's connection [requires read_priest_note]
*Brother Cavel. Aldric knew him — he came fifty years after the original sealing to re-examine the wards. He did discover the truth of the pact. He wrote it in his journal, which he dropped in the chapel — likely the note you found. But Cavel was too afraid to act on what he knew, and Valdric's rising paralysed him.*
*Aldric: "He died knowing what needed doing and unable to do it. Don't make the same choice."*

- Returns to c_22 dialogue options (choice: ask about ritual → c_25 | head for vault → c_45)

#### c_24 — The Lady of Bones [optional lore]
*The Lady is not evil in the way Valdric is evil. She is a power of endings — death as a natural force. Valdric tried to cheat her terms, and she allowed the sealing because it amused her. She has been waiting for someone to break the loop properly. Aldric believes she will not interfere if you attempt the full ritual.*
*This is reassuring — but only if you plan to break the pact rather than just reseal it.*

- Returns to c_22 options

#### c_25 — The sealing ritual explained
*Aldric explains the ritual in the sealing chamber (which is deeper than the vault, below the sarcophagus). The ring must be placed on the sealing stone. The blessed candle's fire, if still burning, can be used to re-invoke the original binding words. But the candle must have been lit in Valdric's presence — it must carry his acknowledgement of defeat.*
*"The candle does not merely weaken him. It bears witness. Lit in his presence, it records his second death. That testimony, carried to the sealing chamber, is what the ritual needs."*

*This confirms `candle_used` as the ritual gate — and makes the player understand why it matters.*

- Returns to c_22 → c_45

#### c_30 — Inner halls [after c_5a/c_5b if wraith_destroyed or silver dagger used]

> **Wire-in note:** After the wraith encounter in c_5/c_5a/c_5b, the player arrives at c_7 (vault approach). c_30 is not on the main spine — it's an alternative to c_20 for players who didn't take the north archway. c_30 can be reached from c_7 via a choice: "Explore the passage to the west before entering the vault."

*A narrow passage runs west from the vault corridor. If the wraith is gone (`wraith_destroyed`), it leads easily to a small reliquary. If the wraith is not destroyed, the presence is still felt — oppressive cold, hostile — but crossable at cost.*

- If `wraith_destroyed`: passage is clear → c_31 (reliquary)
- If NOT `wraith_destroyed`: must push through cold (2 STAMINA cost) → c_31

#### c_31 — The reliquary
*A small room with three stone niches. Two are empty. The third contains a leather-bound journal — Brother Cavel's full journal, not just the torn note from the altar. Reading it confirms the pact's existence and the ritual requirements.*

*If `knows_the_pact` already set: journal confirms what Aldric told you — adds a +1 LUCK bonus (reassurance).*
*If NOT `knows_the_pact`: reading the journal sets `knows_the_pact` — this is the alternate route to the flag for players who skipped the north archway.*

- Choice: continue → c_45

#### c_35 — Sera appears [if sera_allied]
*As you approach the vault corridor, you hear footsteps behind you. Sera. She's pale and moving slowly but she followed. "I'm not dying in a treasury," she says. "Tell me what we're walking into."*

*If `helped_sera`: she's steadier, more capable. She has her boot knife.*
*If NOT `helped_sera` but `sera_allied`: she followed but is weaker, leaning on the wall.*

- Choices: Tell her everything you know → c_36 | Tell her to wait here → c_7

#### c_36 — Sera hears the truth
*You tell her what Aldric said (or what the journal said, or just the facts as you know them). Sera listens without interrupting.*
*"A pact with a death goddess. Right." She's quiet for a moment. "The guild that hired me — they knew. They wanted the evidence of the pact, not just the ring. Proof that Valdric bargained with divine forces. That's worth more than any jewel." She looks at you. "I'm not taking it to them. Not after this."*

*Sets `sera_knows_truth`.*

- Choice: "Come with me" → c_37 | "This isn't your fight" → c_7

#### c_37 — Sera commits
*Sera straightens, testing her weight. "I'll hold the door while you do whatever ritual you're planning. If anything else comes out of that vault, I'll slow it down. Can't promise more than that."*
*A pause. "Whatever happens in there — you did well. The herbs helped."* [only if helped_sera]

- Choice: Enter the vault together → c_7 (with Sera alongside)

#### c_40 — The iron casket [if NOT met_aldric]
*The casket is sealed with a simple latch, no lock. Inside: a folded document on yellowed parchment, pressed flat by the weight of the casket's lid. The writing is old but legible — a contract. Two signatories: Valdric's serpent seal, and below it, a mark that hurts to look at directly.*
*Reading it takes effort. The words resist comprehension, as though the document itself doesn't want to be read.*

- Luck test: Lucky → read it fully → c_41 | Unlucky → partial reading, still usable → c_41

#### c_41 — The pact document
*The pact's terms: Valdric receives dominion over the dead within his lands. The Lady receives his service as a warden between life and death — his death energy, indefinitely. When the people sealed him, they unknowingly broke the terms by preventing his service. The Lady's response was the loop: he cannot die while the ring exists; the ring cannot be destroyed while he lives. She expects someone to eventually figure it out and break it properly.*
*Sets `knows_the_pact`.*

- Choice: Return to the circular chamber → c_3 (to continue to vault)

#### c_45 — Convergence passage
*A short corridor connecting the north archway area back to the main vault approach. Arrives at c_7.*
- One choice: "Head for the vault" → c_7

---

### Key edits to existing passages after Act 2 Opus draft is merged

1. **c_3**: Add 4th choice `{ "text": "Explore the north archway", "goto": "c_20" }`
2. **c_7**: Add choice `{ "text": "Check the western passage before entering", "goto": "c_30" }` and add Sera joining text if `sera_allied` (can be handled by c_35 → c_37 → c_7 route)
3. **c_11**: Change `"goto": "end_sealed"` to `"goto": "k_1"` — Valdric's defeat leads to Act 3, not straight to the ending

---

## Act 3 — The Sealing Chamber (k_)

### Entry: k_1
Player has the signet ring. Valdric is defeated. The vault is quiet.

The sealing chamber is not in the vault — it's beneath it. A trapdoor behind the dais leads to a lower level: a circular stone room with a single altar (the sealing stone) and walls carved with the original binding glyphs.

### Spine

**k_1** — The trapdoor behind the dais. The ring pulses in the player's hand — it knows where it wants to go.
**k_2** — The sealing chamber itself. The sealing stone. The options available depend on flags.
**k_3 / k_4 / k_5** — The ritual passages (one per path through the sealing)
**Endings** — 5 endings, each its own passage

### Flag evaluation order in k_2 (most specific → least specific)

```
end_pact_broken:    sera_allied + helped_sera + knows_the_pact + candle_used + wraith_destroyed
end_sera_stays:     sera_allied + helped_sera + sera_knows_truth
end_freed:          met_aldric + knows_the_pact + candle_used
death_ring_claim:   NOT knows_the_pact + NOT candle_used → luck test → death on fail
death_valdric_surge NOT knows_the_pact + NOT met_aldric → luck test → death on fail
end_cursed:         NOT candle_used (beat Valdric raw, survived the ritual)
end_sealed:         fallback — any player who reaches k_2
```

Implemented as layered choices with requires_flag / requires_no_flag conditions.

**Death mechanic in k_2:** Players who place the ring without knowing the pact and without the candle's testimony face a luck test. Lucky → end_cursed (they survive, but cursed). Unlucky → death_ring_claim (the ring's binding magic inverts and claims them). Players who also never met Aldric (and thus have the least context) face death_valdric_surge instead — Valdric's residual will surges back through the ring.

### k_1 — Below the vault
*The trapdoor's hinges are smooth — well-maintained despite the crypt's decay. As if someone expected this to be used.*
*The sealing chamber below is circular, perhaps twenty feet across. The walls are carved with glyphs that glow faintly when the ring comes near — recognition. In the centre, a stone altar with a shallow depression exactly the shape of the signet ring.*
*This is where it ends.*

Choices route based on flags — all lead to k_2 variants or directly to endings.

### Ending passages

#### end_sealed — The Tomb Resealed
*You place the ring in the depression. The glyphs flare white. The vault above seals with a grinding finality. The cold begins to lift.*
*Aldric's voice, faint: "It will hold. For a time."*
*You climb back through the crypt. The corruption is fading but slow — weeks, not days, before Ashford fully recovers. The curse will return in another century if no one comes back.*
*Maren meets you at the edge of Ashford. "It is done?" "It is done — for now."*

ending: true, ending_type: "victory"

#### end_freed — The Ghosts Released
*You place the ring with the candle's light still fresh on your hands. The binding glyphs recognise the candle's testimony and respond — not just sealing the ring, but reading its history. Every soul Valdric trapped in the loop flares bright and then is still.*
*Aldric appears one final time, fully present — not a ghost's echo but something almost alive. "Free," he says. Simply that. Then he is gone.*
*The sealing holds. The trapped souls are released. Ashford recovers within days, not weeks. The crops grow before you reach the village.*

ending: true, ending_type: "victory"

#### end_cursed — The New Warden
*You place the ring but it resists — because you are carrying Valdric's unresolved pact. You fought him without the ritual fire. You are, technically, the next in the loop.*
*The ring seals. But it seals to you. Not on your finger — you are not undead — but in your pack, in your blood, in the ache behind your eyes when the moon rises.*
*Ashford recovers. You are celebrated. You don't tell Maren what you can feel beginning.*
*You are the crypt's new warden. You don't know it yet. But the Lady of Bones does.*

ending: true, ending_type: "victory" (dark — player survives, village saved, but at cost)

#### end_sera_stays — Her Choice
*Sera stands beside you as the ring seals. She helped. The ritual recognises it.*
*Afterwards, she doesn't follow you up the steps.*
*"Someone should watch this place," she says. "The guild will send another collector eventually. And the next person who comes might not know what they're walking into."*
*She's not trapped. She chooses. There is a difference.*
*You climb out alone. In Ashford, Maren asks where your companion is. "Still in there," you say. "By choice." Maren nods as though she understands.*

ending: true, ending_type: "victory"

#### end_pact_broken — The Pact Broken
*Five conditions converge. The wraith's absence has cleared the path of interference. Sera is here. The candle's testimony is fresh. You know the pact's terms. The ring goes into the depression.*
*The glyphs don't flare — they sing. A deep resonance that is not sound so much as rightness. The pact document (if you found it) crumbles to ash in your pack.*
*Aldric is freed. All the trapped souls are freed. The Lady of Bones gets what she was owed — not service, but completion. A closed account.*
*Sera survives. The crypt becomes just stone and silence. Ashford heals fully, immediately. The dead forest on the road puts out new leaves before you reach the treeline.*
*Maren sees you coming and starts to cry before you even speak.*

ending: true, ending_type: "victory"

#### death_ring_claim — Claimed
*You place the ring. For a moment nothing happens — then everything happens at once. The binding glyphs do not recognise the candle's testimony because there is none. The ring's magic has no witness for Valdric's second death. It reads the only life in the room: yours.*
*The sealing works. The tomb is sealed. But the ring does not stay in the depression — it rolls to the edge, falls, and comes to rest against your boot. You pick it up without meaning to.*
*Your hand closes around it and does not open again.*
*In a century, a new count will rule this crypt. The village will call them something other than Valdric. But the pact will recognise the shape.*

ending: true, ending_type: "death"

#### death_valdric_surges — The Count Returns
*You place the ring in the depression without understanding what you're completing. The ritual begins but the pact's loop has no resolution — Valdric's second death was never properly witnessed, and the sealing stone cannot accept an unwitnessed death.*
*The glyphs flare the wrong colour. Cold. Then colder. Then the sound from above — the vault, sealed moments ago — and the vault doors opening.*
*Something is coming down the steps. Deliberate. Patient.*
*The Count is not defeated. He was resting.*

ending: true, ending_type: "death"

---

## Prose style notes

- Second person, present tense ("You push open the door…")
- Gothic horror tone — cold, precise, never overwrought
- Valdric's voice: the sound of a coffin lid sliding shut — measured, contemptuous
- Aldric's voice: scholarly, exhausted, grateful — he's been waiting a long time
- Sera's voice: flat, practical, dry — she's a professional and she's scared but won't show it
- Paragraph breaks via `\n\n` in text strings
- No purple prose — the horror is in the details, not the adjectives

---

## Validation notes

After each Opus draft:
1. Run the passage validator (BFS from start passage)
2. Check for duplicate choice labels
3. Verify all new flags are in the master flag table or removed
4. Verify enemy IDs match: `skeleton_warrior`, `crypt_ghoul`, `tomb_spider`, `wraith`, `count_valdric_weakened`, `count_valdric`
5. No `requires_no_item` usage
6. All new passages reachable from their entry point
