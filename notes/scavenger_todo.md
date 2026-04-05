# The Scavenger of New Babylon Station — State & TODO

## Current State

- **Passages:** 57 | **Version:** 1.0
- **Victory endings:** 2 (`23` escape with Voss, `23a` solo escape)
- **Death endings:** 4 (`death_cornered`, `death_malachar`, `death_empty`, `death_station`)
- **Combats:** 7 | **Luck tests:** 3

**Summary:** More developed than Valdric — Voss alliance, plasma pistol, and Zara's info are all gated correctly. But 8 flags fire into nothing. A stealth/loud consequence axis was clearly planned (`clean_retrieval` vs `alarm_triggered`) but never built. The data chip MacGuffin is never resolved.

---

## Flag Audit

| Flag | Status | Notes |
|------|--------|-------|
| `has_plasma_pistol` | ✓ ok | |
| `voss_allied` | ✓ ok | |
| `zara_info` | ✓ ok | |
| `alarm_triggered` | ✗ orphaned | Half of the stealth axis — never checked |
| `clean_retrieval` | ✗ orphaned | Half of the stealth axis — never checked |
| `emp_used` | ✗ orphaned | Set but never checked |
| `fought_imperials` | ✗ orphaned | Heat level flag — never checked |
| `met_voss` | ✗ orphaned | Set but never checked |
| `sensors_sabotaged` | ✗ orphaned | Set but never checked |
| `spotted_imperials` | ✗ orphaned | Heat level flag — never checked |
| `voss_diversion` | ✗ orphaned | Should unlock a unique escape route |

---

## TODO

### Spec
- [ ] Write `adventures/the_scavenger_of_new_babylon_station_spec.md`
- [ ] Define 10+ flags — wire all current orphans or cut them
- [ ] Design 5–6 endings driven by: what's on the chip, whether the station survives, Voss fate, Imperial heat level
- [ ] Resolve the data chip mystery — what's on it, and let player choices about it drive ending variations
- [ ] Map out the stealth/loud consequence axis — `clean_retrieval` vs `alarm_triggered` should feel meaningfully different by Act 3
- [ ] Wire `voss_diversion` to a unique escape route

### Expansion (~220 passages across 3 acts)
- [ ] Re-prefix existing passages to `n_` (Act 1)
- [ ] Add `"start_passage": "n_1"` to adventure JSON
- [ ] Act 2 (`b_`) — escape complicated: third faction reveal (who hired you?), Malachar pursuit, chip revelation (~90 new passages)
- [ ] Act 3 (`s_`) — the extraction: Imperial blockade, Voss sacrifice/survival, 5–6 flag-gated endings (~60 new passages)
- [ ] Spin up Opus for each act draft (see EXPANSION_GUIDE.md for prompt template)

### Polish
- [ ] All 8 orphaned flags gate real consequences, or are removed
- [ ] Stealth vs. loud playthroughs feel meaningfully different by the ending
- [ ] Data chip contents revealed and narratively significant
- [ ] Flag audit panel shows all flags ✓ ok
