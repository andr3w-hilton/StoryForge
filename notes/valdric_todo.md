# The Crypt of Count Valdric — State & TODO

## Current State

- **Passages:** 43 | **Version:** 1.0
- **Victory endings:** 1 (`26`) — no variation regardless of player choices
- **Death endings:** 3 (`death_riddle`, `death_wraith`, `death_flee_valdric`)
- **Combats:** 6 | **Luck tests:** 2

**Summary:** Weakest adventure in the collection. Characters Sera (ghost girl ally) and Aldric (tragic ghost count) are sketched in but deliver zero mechanical payoff. 9 flags fire into nothing.

---

## Flag Audit

| Flag | Status | Notes |
|------|--------|-------|
| `aldric_warned_candle` | ✓ ok | |
| `has_candle_already` | ✓ ok | |
| `met_sera` | ✗ orphaned | Set but never checked |
| `helped_sera` | ✗ orphaned | Set but never checked |
| `sera_allied` | ✗ orphaned | Set but never checked |
| `met_aldric` | ✗ orphaned | Set but never checked |
| `aldric_warned_wraith` | ✗ orphaned | Set but never checked |
| `saw_vision` | ✗ orphaned | Set but never checked |
| `read_priest_note` | ✗ orphaned | Set but never checked |
| `candle_used` | ✗ orphaned | Set but never checked |
| `wraith_destroyed` | ✗ orphaned | Set but never checked |

---

## TODO

### Spec
- [ ] Write `adventures/the_crypt_of_count_valdric_spec.md`
- [ ] Define 8–10 flags — wire all current orphans or cut them
- [ ] Design 4–6 endings: `end_sealed` (basic), `end_freed` (Aldric at peace), `end_sera_stays` (Sera remains by choice), `end_cursed` (player takes the curse), plus death variants
- [ ] Map out Sera arc — she should matter mechanically, not just atmospherically
- [ ] Map out wraith_destroyed payoff — should gate an alternate approach to Valdric

### Expansion (~200 passages across 3 acts)
- [ ] Re-prefix existing passages to `v_` (Act 1)
- [ ] Add `"start_passage": "v_1"` to adventure JSON
- [ ] Act 2 (`c_`) — deep crypt: Sera's full backstory, Aldric confrontation, the pact revealed (~80 new passages)
- [ ] Act 3 (`k_`) — the Sealing Chamber: flag-gated finale, 4–6 divergent endings (~50 new passages)
- [ ] Spin up Opus for each act draft (see EXPANSION_GUIDE.md for prompt template)

### Polish
- [ ] All 9 orphaned flags gate something meaningful, or are removed
- [ ] Sera has real agency — at minimum one ending where her alliance changes the outcome
- [ ] Differentiate victory endings — Aldric-at-peace vs. crypt-sealed-but-cursed at minimum
- [ ] Flag audit panel shows all flags ✓ ok
