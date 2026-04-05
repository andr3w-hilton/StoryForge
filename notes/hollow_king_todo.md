# The Throne of the Hollow King — State & TODO

## Current State

- **Passages:** 76 | **Version:** 1.0
- **Victory endings:** 2 (`43` standard victory, `45` sacrifice ending)
- **Defeat endings:** 3 (`26` overwhelmed, `44` take the crown, `35b` flee)
- **Combats:** 12 | **Luck tests:** 6

**Summary:** Most polished of the three — zero orphaned flags after polish pass (2026-04). All 13 flags set and checked. Items are narratively used. The story is complete and works as-is. Expansion is optional, not necessary.

---

## Flag Audit (post polish pass)

All 13 flags clean: `cursed_blade`, `explored_chapel`, `has_antitoxin`, `has_candle`, `has_ring`, `holy_water_used`, `honour_broken`, `knows_crown_weakness`, `sat_banquet`, `too_late`, `vashka_convinced`, `vashka_shaken`, `vashka_wounded`

---

## What Could Be Better (if expanding)

- Vashka is the most interesting character but only appears in ~8 passages
- The village (Carragh's Foot) and Brida appear only at start/end — no real presence
- Both victory endings land similarly — "you won, the mountain is quiet"
- No ending where Vashka turns against the ritual and fights beside you
- Aldric's thousand-year backstory is told but not fully explored

---

## TODO (lower priority — story works as-is)

### Spec (if proceeding)
- [ ] Write `adventures/the_throne_of_the_hollow_king_spec.md`
- [ ] New flags: `vashka_allied`, `aldric_remembers`, `village_warned`, `knows_aldrics_name`
- [ ] Design 6th ending: `end_vashka_allied` — Vashka turns, fights alongside you
- [ ] Differentiate the two current victories more sharply

### Expansion (~200 passages across 3 acts, if proceeding)
- [ ] Re-prefix existing passages to `h_` (Act 1)
- [ ] Add `"start_passage": "h_1"` to adventure JSON
- [ ] Act 2 (`k_`) — deep halls + Vashka arc (~60 new passages)
- [ ] Act 3 (`r_`) — throne chamber: longer endgame with 6 differentiated endings (~50 new passages)
- [ ] Spin up Opus for each act draft (see EXPANSION_GUIDE.md for prompt template)

### Polish (if expanding)
- [ ] Give Vashka a proper arc — she deserves more than 8 passages
- [ ] Differentiate the two victory endings more sharply
- [ ] Bring Brida/village back into the endgame via `village_warned` epilogue text
- [ ] Flag audit panel shows all flags ✓ ok
