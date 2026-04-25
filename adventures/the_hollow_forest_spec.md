# The Hollow Forest — Adventure Spec

**Title:** The Hollow Forest
**Genre:** Wilderness Survival / Conspiracy Thriller
**Tone:** Naturalistic dread, epistemic unease, institutional menace. No magic, no fantasy. Influenced by VanderMeer's Southern Reach — dread through accumulated wrongness, not dramatic revelation.
**Scale:** 250–300 passages across 4 acts + endings

---

## Premise

Marek was a territorial warden and naturalist — a man with official access to the borderland forest on the empire's forgotten eastern margin. Three weeks ago he went in alone to document something wrong with the forest. His last message: *"I think I've found the cause."* Then nothing.

You go in after him.

The search-and-rescue framing is the surface of the adventure. The truth beneath it: the empire has been conducting a systematic territorial clearance operation, introducing a chemical defoliant into the upstream watershed to kill the forest slowly, destroy the livelihoods of the border communities who depend on it, and drive them out without open war. Marek found the evidence — soil samples, water readings, and the strategic documents that prove intent. The empire didn't silence him. They let him run, then sent a survey team in after him.

They let you in for the same reason. Every "helpful" thing you find in the forest — supply caches, trail markers, a professional survey team — serves the empire's need to monitor who knows what, and to ensure the right people never leave.

The player will not know this until Act 3. Everything before that is a survival adventure and a search.

---

## Tone Reference

**VanderMeer's method, stripped of the supernatural:**
- Ground descriptions in forensic naturalist accuracy. Name species. Get animal behaviour right. Then introduce one understated deviation — a hawk that doesn't flush, a deadfall pattern inconsistent with wind, a sound that stops too abruptly.
- The institutional menace is retroactive. The cache felt like luck. The trail markers felt like survival sense. The survey team felt like kindness. The reveal doesn't introduce new information — it recontextualises everything.
- Prose should favour smell, sound, and physical discomfort over visual description. The cold in wet boots. The smell of something wrong in still water. Silence where there should be birdsong.
- The narrator reports and catalogs. Emotional response is suppressed. What the player *sees* and what it *might mean* are kept separate.

---

## Target Structure

```
Target: 0 passages → 250–300 passages (new adventure, written from scratch)
Acts: 4 acts + endings
Start passage: "f_1"
```

---

## Passage ID Scheme

| Prefix | Act | Setting |
|--------|-----|---------|
| `f_` | Act 1 | The Forest Edge — first day, the margin of the known |
| `d_` | Act 2 | The Deep Forest — losing time, losing certainty |
| `h_` | Act 3 | The Heart — where Marek is, where the truth is |
| `end_` | Endings | Seven distinct resolutions |
| `death_` | Deaths | Two death endings |

---

## Character

```json
{
  "skill_base": 6,   "skill_dice": 1,
  "stamina_base": 14, "stamina_dice": 2,
  "luck_base": 6,    "luck_dice": 1,
  "starting_items": ["hunting_knife", "flint_steel", "waterskin", "forest_map"],
  "starting_provisions": 6
}
```

High stamina base because the adventure drains it through exposure, weather, and poor water rather than combat. Provisions are generous at start — survival management is the arc.

---

## Items

| ID | Name | Type | Stats | Description |
|----|------|------|-------|-------------|
| `hunting_knife` | Hunting Knife | weapon | skill_bonus: 1 | A long-bladed knife, good for skinning and for worse. |
| `flint_steel` | Flint & Steel | tool | — | Reliable fire-starter. Essential in the wet. |
| `waterskin` | Waterskin | tool | — | Carries water. What you fill it from matters. |
| `forest_map` | Forest Map | tool | — | An official survey map of the eastern margin. Parts of it are wrong. |
| `rope` | Rope | tool | — | Thirty feet of braided rope. Found in Marek's first camp. |
| `mentors_journal` | Marek's Journal | tool | — | Marek's field notes. Careful, methodical, increasingly disturbed. |
| `soil_samples` | Soil Samples | evidence | — | Vials of earth from the contamination sites. The compound is in them. |
| `imperial_documents` | Imperial Documents | evidence | — | Strategic papers. Proof of intent, not just method. |
| `provisions` | Provisions | consumable | stamina_restore: 4 | Hard rations. Running low is a slow emergency. |

**Item narrative payoff requirements:**

| Item | Minimum one narrative use |
|------|--------------------------|
| `hunting_knife` | `d_25`: Taking bark samples as evidence. Also usable in wolf encounter. |
| `flint_steel` | `f_18`: Fire is the difference between surviving the night and not. |
| `waterskin` | `d_22`: The water quality passage — what you're carrying matters. |
| `forest_map` | `f_10`: The map is wrong in a key place. First sign something is off. |
| `rope` | `d_12`: River crossing. Later: escape route from the agent camp. |
| `mentors_journal` | `h_15`: Key to earning Marek's trust. He recognises his own handwriting. |
| `soil_samples` | `h_60` / endings: Physical evidence that survives even if documents don't. |
| `imperial_documents` | Endings: Primary gate for `end_exposure` and `end_extracted`. |

---

## Enemies

| ID | Name | SKILL | STAMINA | Notes |
|----|------|-------|---------|-------|
| `wolf` | Wolf | 7 | 6 | Flee always available (flee_stamina_cost: 0 — running costs you nothing, the wolf gives up). Most encounters have a bypass via flag or luck test. |
| `wolf_pack` | Wolf Pack | 8 | 12 | Dangerous. Should feel like a crisis. Flee available but costly (flee_stamina_cost: 3). |
| `imperial_agent` | Imperial Agent | 8 | 9 | Human threat, Act 3 only. Professional, not monstrous. |
| `desperate_man` | Desperate Man | 5 | 6 | Another traveller, lost and hostile. Act 2. Can be talked down (choice gate) or fought. |

Combat should be rare and feel costly. The adventure is not a dungeon crawl. Most enemy encounters should have a non-combat resolution — stealth, avoidance, dialogue — gated on flags or luck tests.

---

## Master Flag Table

| Flag | Set at | Checked at | What it represents |
|------|--------|------------|-------------------|
| `has_fire` | f_18 (made fire) | f_20, f_28, d_5 (shelter quality gates) | Core survival — the night is survivable with fire |
| `clean_water_source` | f_32 or d_8 (found uncontaminated spring) | d_20, d_22, stamina gates throughout | Safe water source located |
| `followed_markers` | f_22 (followed imperial survey markers) | End matrix | Unwitting empire cooperation — minor |
| `used_cache` | d_48 (used imperial supply cache) | End matrix | Unwitting empire cooperation — minor |
| `trusted_survey_team` | d_58 or h_10 (cooperated with agents) | h_20, h_35, end matrix | Unwitting empire cooperation — major. Affects Marek's trust and escape options |
| `found_rope` | f_40 (Marek's first camp) | d_12, h_72 | Utility item gate |
| `found_mentors_notes` | d_38 (Marek's main camp) | h_15, h_20, end matrix | Knows the scope of what Marek found |
| `found_soil_samples` | d_44 (contamination site) | h_60, end matrix | Physical evidence of the compound |
| `knows_contamination` | d_50 (assembled the picture from notes + samples) | h_35, h_55, end matrix | Understands what is killing the forest |
| `found_documents` | h_48 (the hidden strategic papers) | end matrix | Proof of intent — the clearance operation |
| `knows_true_purpose` | h_55 (full picture: compound + documents + intent) | end matrix | Understands this is territorial clearance, not weapons testing |
| `marek_trusts_you` | h_25 (earned in the agent camp) | h_48, h_65, end matrix | He will work with you — sharing documents, coordinating escape |
| `warned_village` | h_68 (optional branch — sent warning to border community) | end_exposure only | The community is forewarned |

**Empire cooperation score:** Sum of `followed_markers` + `used_cache` + `trusted_survey_team` at endings (0–3). Determines epilogue tone even in survival endings.

**Flag design rules applied:**
- Every flag has at least one "Checked at" entry — no silent tracking
- Flags represent decisions and discoveries, not mechanical state
- The best ending requires 4 flags: `found_documents` + `marek_trusts_you` + `warned_village` + NOT `trusted_survey_team`
- A zero-flag player (trusted everything, found nothing) reaches `end_tool` or `end_survivor` — still a resolution

---

## Ending Condition Matrix

| Ending ID | Label | Required flags | Tone | ending_type |
|-----------|-------|---------------|------|-------------|
| `end_exposure` | The Truth Gets Out | `found_documents` + `marek_trusts_you` + `warned_village` + NOT `trusted_survey_team` | Best. You got Marek out, you got the proof out, the village knows. It will cost you both. | victory |
| `end_extracted` | Out With Marek | `marek_trusts_you` + `found_documents`, NOT `warned_village` | Pyrrhic. You saved him. The villages don't know yet. The documents are safe for now. | victory |
| `end_truth_only` | The Documents Survive | `found_documents` + NOT `marek_trusts_you` | Bitter. Marek didn't make it out. But the proof did. You carry it alone. | victory |
| `end_survivor` | Just Alive | No key flags — fallback for players who found nothing | You got out. The forest is still dying. You don't know why. | victory |
| `end_tool` | The Empire's Asset | `trusted_survey_team` + `used_cache` + `followed_markers` | The darkest non-death ending. You survived. You were useful. The survey team thanks you warmly. | victory |
| `death_forest` | Taken by the Forest | Failed survival — exposure, starvation, injury | The forest wins through attrition. | death |
| `death_agents` | Silenced | Caught by agents while carrying documents and/or with Marek's trust | They cannot let you leave with what you know. | death |

**Minimum ending set check:**
- ✓ 1 best victory (all key flags)
- ✓ 2 partial victories (extracted, truth_only)
- ✓ 1 survival fallback (survivor)
- ✓ 1 dark twist ending (tool)
- ✓ 2 death endings (forest, agents)

---

## Act 1 — The Forest Edge (f_)

**Tone:** Unease building. The forest looks wrong but you can't name why. Your first day in. The survival basics establish themselves as problems: shelter, water, navigation, the cold. Everything is functional, grounded. The wrongness is understated — one thing off at a time.

**Passage budget:**
```
Named passages:    25
Fill passages:     40 minimum  (weather texture, foraging branches, terrain navigation,
                                atmospheric side moments, survival dead-ends)
─────────────────────────────
Act minimum:       65
```

**The spine (mandatory path):**
f_1 → f_5 → f_10 → f_18 → f_28 → f_38 → f_48 → d_1

**Key beats — passage by passage:**

`f_1` — **The Entry**
You enter the forest at the margin road. Establish what the player knows: Marek's name, that he's been gone three weeks, that he was documenting something wrong with the eastern forest. Describe what you see immediately: the tree line is normal, then not. A particular quality of silence. The map in your hand. Second person, present tense throughout.
*Sets nothing. The opening.*

`f_5` — **First Navigation Choice**
The map shows two routes toward Marek's known operating area — the valley path (longer, sheltered, follows the river) or the ridge path (shorter, exposed, better sightlines). Neither is obviously correct. The map has a third feature marked that doesn't match the terrain in front of you.
*Choice: valley or ridge. Both are valid. The map discrepancy is noted but not explained.*

`f_10` — **The Map Is Wrong**
Whichever route, a landmark on the map is missing or wrong — a bridge that isn't there, a clearing that's now dense growth, a stream that runs the wrong direction. The player has to reckon with the map being unreliable.
*No flag. First epistemic crack — what can you trust?*

`f_15` — **Something Dead**
A large animal — a deer — dead beside the path. Wrong position (died lying down, not fallen). No obvious injury, no predation. Flies, but not many. Something about it is wrong in a way that takes a moment to identify: the ground around it is discoloured, a faint ring in the soil.
*No flag set. Pure atmosphere. Forensic, not dramatic.*

`f_18` — **Shelter — Making Fire**
Weather coming in — low cloud, dropping temperature, the smell of rain. Finding shelter before dark is a meaningful task. The flint & steel matters here: fire is the difference between a survivable night and a bad one. Luck test for shelter quality if no fire.
*Sets `has_fire` if flint used. `has_fire` gates f_20 (warm camp, stamina preserved) vs f_20_cold (rough night, add_stamina: -2).*

`f_22` — **The Markers**
On the path the next morning: small marks cut into trees at regular intervals. Too regular. The spacing is consistent — survey spacing, not trail blazing. They're leading somewhere. They could be Marek's. They're not Marek's style (he used cairns, not cuts).
*Choice: follow the markers or ignore them and navigate independently. Following sets `followed_markers`.*

`f_28` — **Marek's First Camp**
A camp site — weeks old. Marek's, clearly: the organisation of it, the particular way he laid a fire. He was here for several days. He moved on deliberately — nothing left behind that he'd have wanted. Except the rope, coiled and hung from a branch. Either he forgot it or he left it.
*`add_items: ["rope"]` on arrival. This is the first confirmation Marek was real and purposeful. Sets mood.*

`f_32` — **The Clean Spring (optional)**
A side branch off the main path — a spring, visibly cold and clear, fed from high ground rather than the valley. Different from the river water. An option to fill the waterskin from something untouched.
*Sets `clean_water_source`. Optional — requires choosing to leave the main path.*

`f_38` — **The Survey Team — First Contact**
Three people in practical clothing, good equipment, moving with professional confidence. They introduce themselves as an imperial survey team mapping the eastern margin. Friendly. They have better food, a drier camp, and information about the terrain ahead. They've seen sign of Marek — three days old, heading northeast.
*Choice: camp with them tonight (partial trust, social flag toward `trusted_survey_team`) or thank them and move on. No flag set yet — that comes in Act 2.*

`f_45` — **The Forest at the Margin's End**
The point where the managed edge of the forest becomes something older. The trees change character — larger, denser, less light. More dead ones. The wrongness accumulates here into something you could almost describe: the canopy is thinner than it should be at this scale of tree, because the trees are dying from the crown down.
*Atmospheric. The threshold passage. d_1 is through here.*

**Major branches in Act 1:**

*Branch A — Valley path vs ridge path (f_5)*
Both routes reach f_18 and f_22. The valley path has more foraging opportunity (provisions). The ridge path has better sightlines (an optional passage where you see the survey team before they see you, which lets you make a more informed choice at f_38).

*Branch B — Fire or no fire (f_18)*
`has_fire` / no flag. Affects stamina and gates a warm-camp passage where you notice something: the wood from a particular tree burns with a faint smell of something chemical.

*Branch C — Following the markers (f_22)*
Sets `followed_markers`. The markers lead to a small cache of supplies (this is the Act 1 cache — less obviously imperial than the Act 2 cache). A fork: use the supplies or leave them.

*Branch D — The clean spring (f_32)*
Optional detour, sets `clean_water_source`. Only reachable from the valley path branch.

*Branch E — Survey team trust (f_38)*
Camping with them doesn't set a flag yet — that's Act 2. But it establishes rapport that makes the Act 2 cooperation choices easier to drift into.

---

## Act 2 — The Deep Forest (d_)

**Tone:** The wrongness is no longer deniable. The ecology is visibly collapsing — dead zones, animals in wrong places, water that the nose rejects before the mind does. Marek's main camp and his notes change the adventure's register: this becomes an investigation as well as a survival. The survey team reappears. They knew where you were.

**Passage budget:**
```
Named passages:    30
Fill passages:     50 minimum  (ecological horror texture, wildlife encounters, foraging
                                failures, weather crises, terrain difficulty, dead-end
                                exploration of wrong-path areas)
─────────────────────────────
Act minimum:       80
```

**The spine:**
d_1 → d_12 → d_22 → d_35 → d_42 → d_50 → d_58 → h_1

**Key beats:**

`d_1` — **What the Trees Know**
The transition into the deep forest. Describe precisely: the canopy closes, the light changes quality. Specific wrongness — a stand of mature oak with the bark lifting away from the trunk in sheets, the exposed wood beneath pale and dry. The sound of the forest is wrong: too little. A woodpecker is working at a dead tree. Everything it finds is already gone.
*No flags. Pure VanderMeer baseline-then-deviation.*

`d_8` — **The River**
The main river. The map shows it as a reliable water source. Up close: the colour is slightly off — not dramatically, just not quite right. Depending on `clean_water_source`: if set, you know to be cautious; if not, this is the moment you notice and have to decide.
*Luck test for players without `clean_water_source`: drink and risk it (unlucky: add_stamina: -3, a slow nausea) or go thirsty (add_stamina: -1, manageable).*

`d_12` — **River Crossing**
A crossing point — the bridge on the map is gone, replaced by a debris dam. Crossable but requires the rope if the current is high (luck test). Without rope: harder crossing, higher risk.
*`requires_item: "rope"` for the safe route. Without: luck test, unlucky costs stamina.*

`d_20` — **The Desperate Man**
Another person in the forest — not a warden, not a surveyor. A charcoal-burner from one of the border communities, been in here four days, knows something is wrong and can't find his way out. He's frightened and not quite rational. Options: help him (costs provisions, sets up `warned_village` possibility — he knows the community), ignore him, or if he turns hostile, fight.
*The charcoal-burner is the connection to the border village. If helped, he gives information about the community upstream. This is the seed of `warned_village`.*

`d_25` — **The Bark Samples**
A stand of trees with distinctive discolouration at the roots — the compound concentrates here. Using the hunting knife to take samples produces the first physical evidence: the discolouration transfers to the cut surface, and the smell is faintly chemical. Wrong for rot, wrong for blight.
*Requires `hunting_knife`. Sets up `soil_samples` at d_44.*

`d_35` — **Marek's Main Camp**
He was here for at least two weeks. The organisation of it tells a story — systematic, methodical, increasingly anxious (the later notes are shorter, the handwriting tighter). The camp is intact. He left in a hurry, or was found.
*`add_items: ["mentors_journal"]` on arrival. Sets `found_mentors_notes`.*

`d_38` — **Reading the Journal**
The journal in full. Marek's voice: precise, unhurried at first, then not. He found the wrong-water pattern early. He traced it upstream. He took samples. He began to understand the distribution pattern wasn't natural — too even, too consistent with the watershed. His last entry names the compound by its mineral properties. His second-to-last entry: *"The survey team found my camp. They were polite. They offered to help me out. I said I needed more time."*
*Gate on `found_mentors_notes`. Detailed reading — Opus should write this as a long passage. Sets `knows_contamination` if read in full.*

`d_44` — **The Contamination Site**
Upstream of the main camp: a series of points along the river bank where the soil is visibly different — colour, texture, the absence of the usual riverside growth. With the knife, proper samples. Vials from Marek's camp to carry them in.
*`add_items: ["soil_samples"]`. Sets `found_soil_samples`. Requires visiting Marek's camp first.*

`d_48` — **The Cache**
Well-placed, well-stocked. Good food, dry fuel, a quality water flask. Imperial supply markings — present but not obvious unless you look, and looking requires either suspicion or the right knowledge. A normal player uses it gratefully. A suspicious player (has `knows_contamination` or `found_mentors_notes`) can spot the markings.
*Sets `used_cache` if used. The choice to examine vs use is meaningful here.*

`d_55` — **The Wolf**
A wolf on the path — thin, wrong territory for the season, displaced. It's not hunting. It's as lost as you are. Avoidance is possible (luck test or `has_fire` as a deterrent). Fighting is an option (costly). The wolf's displacement is ecological — its prey base has collapsed.
*Wolf encounter. Primary route is avoidance. Combat available but presented as a bad idea.*

`d_58` — **The Survey Team — Second Contact**
They appear again. They knew where you were — they name a campsite you didn't tell them about. The friendliness is unchanged. They have information about Marek: he's been found, he's safe, there's a camp ahead where he's resting. They offer to take you there.
*Major choice: go with them (sets `trusted_survey_team`, leads to h_1 via their route) or thank them and go independently (harder path to h_1, but no flag set). This is the most consequential trust decision.*

**Major branches in Act 2:**

*Branch A — Water decision (d_8)*
Contaminated river vs held thirst vs lucky find. Stamina management tension.

*Branch B — The desperate man (d_20)*
Help/ignore/fight. Helps sets up village connection. Key to `warned_village` later.

*Branch C — Reading the journal (d_38)*
Full reading vs partial. Full sets `knows_contamination`. Partial gives information but not the compound name — `knows_contamination` not set, reducing ending options.

*Branch D — The cache (d_48)*
Use vs examine. Sets `used_cache`. Players with `knows_contamination` have more reason to be suspicious.

*Branch E — Survey team trust (d_58)*
The most important binary in Act 2. Going with them is easier but sets `trusted_survey_team` and limits Act 3 options. Going alone is harder (stamina cost, luck test for navigation) but preserves agency.

---

## Act 3 — The Heart (h_)

**Tone:** Revelation and moral weight. The survival adventure becomes something harder. You find Marek, but not in the way you expected. The truth assembles itself. Every choice from the previous two acts carries forward into what's possible here.

**Passage budget:**
```
Named passages:    35
Fill passages:     45 minimum  (the agent camp's texture, Marek's constrained communication,
                                the forest around the camp, escape route exploration,
                                confrontation branches, aftermath passages)
─────────────────────────────
Act minimum:       80
```

**The spine:**
h_1 → h_10 → h_20 → h_35 → h_48 → h_60 → h_68 → h_72 → endings

**Key beats:**

`h_1` — **Voices Ahead**
You hear Marek's voice before you see the camp. Relief — genuine, physical relief — and then wrong. The cadence is off. He's answering questions, not speaking freely. The camp comes into view: good equipment, three agents including one clearly senior, and Marek sitting at a fire, wrapped in a blanket, looking smaller than you remember.
*The emotional beat of arrival. No flags set — pure atmosphere.*

`h_10` — **The Camp — Everything Fine**
The lead agent (name: Serrin — professional, unhurried, completely in control) welcomes you. Marek is here, recovering from a turned ankle, had been having trouble navigating. Lucky the survey team found him when they did. Tea is offered. The story is plausible.
*Choice: accept the hospitality (moves toward `trusted_survey_team` if not already set) or stay cautious.*

`h_20` — **Marek Gets a Moment**
A small window — fetching water, Serrin occupied with something else. Marek gets three sentences. What he says depends on what you're carrying:
- If `found_mentors_notes`: *"You read it. Good. The documents are under the hearthstone of the old forester's hut. Northeast, half a mile."*
- If NOT `found_mentors_notes`: *"Don't drink the tea. Don't trust Serrin. There are documents — I can't tell you where yet, not here."*
*Gate on `found_mentors_notes`. Critical passage — Marek's trust begins here. Whether he trusts you enough to say more requires checking `trusted_survey_team` — if set, he's more guarded.*

`h_25` — **Earning Marek's Trust**
If `trusted_survey_team` is NOT set: Marek finds a way to signal his real state — a look, a word out of Serrin's hearing. He's not free. He cooperates with them because the alternative was worse. He trusts you because you came alone and you're not theirs.
If `trusted_survey_team` IS set: Marek is uncertain. He can see you arrived with them. The trust passage is harder — requires a luck test or a specific item (`mentors_journal` — showing him his own notes proves you found the camp, not them).
*Sets `marek_trusts_you` if conditions met. This is the key relationship flag.*

`h_35` — **What Serrin Wants**
Serrin makes the offer explicit — privately, reasonably. You've all had a difficult few days. Marek is safe. The survey work is almost done. The simplest thing is to walk out together, file a missing-person closure, go home. He doesn't mention the documents. He doesn't need to.
*If `knows_contamination` is set: you understand what you're being asked to erase. If not: the offer seems reasonable and the choice is harder.*

`h_48` — **The Documents**
The forester's hut — northeast, half a mile, accessible only if `marek_trusts_you` is set (Marek told you) or if `found_soil_samples` is set (you traced the site pattern independently and the hut is at its centre). Inside, under the hearthstone: a leather document case. Imperial seal. Strategic papers — internal correspondence, operational timeline, deployment records. The compound identified by military designation. The objective stated plainly: *population clearance by resource denial.*
*`add_items: ["imperial_documents"]`. Sets `found_documents`. The moral weight of what you're holding.*

`h_55` — **The Full Picture**
Holding the documents, having the soil samples, knowing what Marek found: the picture is complete. This isn't a weapons test. It's a clearance operation. The forest dying is the plan working.
*Sets `knows_true_purpose` if `found_documents` + `found_soil_samples` + `knows_contamination` all set.*

`h_60` — **The Village**
Accessible if the charcoal-burner was helped at d_20 (he named his village) and if `knows_contamination` is set. A half-day's detour — the border community upstream. A choice: warn them (takes time, creates risk of Serrin noticing your absence) or don't.
*Sets `warned_village`. Costs stamina (add_stamina: -2). Only reachable via the d_20 help branch + `knows_contamination`.*

`h_65` — **Confrontation with Serrin (optional)**
If `knows_true_purpose` is set, a confrontation passage is available. Serrin drops the professional courtesy when cornered. He doesn't threaten — he explains. The empire's logic is coherent, delivered without malice: the border communities were always going to be absorbed; this is faster and quieter. If you have the documents, the confrontation becomes dangerous.
*Gate on `knows_true_purpose`. Without documents: he can afford to be calm. With documents: leads toward `death_agents` if mishandled.*

`h_72` — **The Escape**
Getting out: Marek, the evidence, through the forest. Multiple routes depending on what you have:
- With `rope`: the river crossing is manageable
- With `has_fire`: signal fire option (ambiguous — could be rescue, could be agents)
- With `trusted_survey_team` set: the agents' path is available but surveilled
- Without any of the above: the hard way, stamina-dependent luck tests

*This passage routes to the appropriate ending based on flags.*

**Major branches in Act 3:**

*Branch A — Trust at the camp (h_10–h_25)*
Accepting hospitality vs staying cautious. Converges on h_35 but `trusted_survey_team` state matters throughout.

*Branch B — Getting Marek's trust (h_25)*
Requires NOT `trusted_survey_team`, or requires `mentors_journal` item. Core relationship gate.

*Branch C — Finding the documents (h_48)*
Requires `marek_trusts_you` OR (`found_soil_samples` as independent navigation).

*Branch D — The village (h_60)*
Optional, costly, only available on the long flag path. Required for best ending.

*Branch E — Confrontation vs slipping away (h_65–h_72)*
Confrontation is dramatic, risky, only available with `knows_true_purpose`. Slipping away is safer but requires navigation tools.

---

## Endings (end_ / death_)

### end_exposure — The Truth Gets Out
**Required:** `found_documents` + `marek_trusts_you` + `warned_village` + NOT `trusted_survey_team`
You get out. Marek gets out. The documents get out. The village was warned before you left. What happens next is outside the scope of a warden and whoever came to find him — but the information exists now, in the right hands, and that's not nothing.
The epilogue names the cost: what Marek loses (his position, his access, probably more), what you lose, what it takes to make something like this known.
*ending_type: "victory"*

### end_extracted — Out With Marek
**Required:** `marek_trusts_you` + `found_documents`, NOT `warned_village`
Both of you out. The documents safe. The village doesn't know — you didn't have time, or you didn't know about them. The truth is contained in what you're carrying. What you do with it is the next story.
*ending_type: "victory"*

### end_truth_only — The Documents Survive
**Required:** `found_documents` + NOT `marek_trusts_you`
Marek is still back there. You don't know what happened to him after you left — whether Serrin's patience ran out, or whether Marek found another way. You have the documents. That's what he would have wanted. It doesn't feel like enough.
*ending_type: "victory"*

### end_survivor — Just Alive
**Required:** Fallback — no key flags
You came out of the forest. The forest is still dying. You don't know why. Marek is still missing. You tell people, and they listen in the way people listen when they don't know what to do with what they're hearing.
The epilogue notes: three months later, the forest is quieter still.
*ending_type: "victory"*

### end_tool — The Empire's Asset
**Required:** `trusted_survey_team` + `used_cache` + `followed_markers`
Serrin walks you out personally. You and Marek both. It was a difficult few days, he says. You did well. He means it — you were useful, in ways you don't entirely understand yet. The route you took, the camps you noted, the paths you tested: all of it documented.
The epilogue is the report you didn't write, but someone did.
*ending_type: "victory" — but the text reads as a defeat*

### death_forest — Taken by the Forest
**Required:** Failed survival
The forest wins through attrition. No monster, no villain. Exposure, a wrong step, a night without shelter, water that was wrong. The empire's operation continues. Marek is still there somewhere.
*ending_type: "death"*

### death_agents — Silenced
**Required:** Caught by agents while carrying `imperial_documents` without a safe escape route
Serrin remains professional about it. That's the worst thing.
*ending_type: "death"*

---

## Passage Count Requirement for Opus

Each act draft submitted to Opus must include the following count instruction:

> This act must contain at least [N] passages. After writing all named passages, count the keys in your "passages" object. If below [N], you are not finished — add more exploration branches, survival texture, atmospheric side passages, and connective tissue until the count is met. Do not submit until the count is met.

| Act | Minimum |
|-----|---------|
| Act 1 (f_) | 65 |
| Act 2 (d_) | 80 |
| Act 3 (h_) | 80 |
| Endings | 25 (7 endings with 3–4 passages each) |
| **Total minimum** | **250** |

Target 300 — fill passages are not padding, they are the texture that makes the world feel real.

---

## Pre-Writing Checklist

- [x] Every flag has at least one "Checked at" entry
- [x] Every ending has a unique, achievable flag combination
- [x] Every item has a narrative use beyond stats
- [x] Best ending requires 4 flags (feels earned)
- [x] Fallback path (no flags) reaches an ending (end_survivor)
- [x] `start_passage: "f_1"` must be added to the adventure JSON top level
- [ ] Adventure JSON skeleton created with character, items, enemies, start_passage
- [ ] Act 1 draft written and validated
- [ ] Act 2 draft written and validated
- [ ] Act 3 draft written and validated
- [ ] Endings written and validated
- [ ] Full BFS validator run from f_1
- [ ] Flag audit panel clean (all flags ✓ ok)
- [ ] Version set to 1.0 in adventure JSON

---

## Accent / Card Fields

```json
"accent_color": "#4a6741",
"genre_tag": "SURVIVAL",
"theme_icon": "⊕"
```

Dark forest green. The ⊕ icon suggests a survey/map marker — visually fits the imperial-survey theme without spoiling it.
