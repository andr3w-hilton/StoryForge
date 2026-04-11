#!/usr/bin/env python3
"""
Path Arrival Analyser for StoryForge adventures.

Detects passages reachable under multiple flag-state contexts, with a focus
on concrete narrative inconsistencies:

  Mode 1 (default)  — Re-entry detection: passages that set a flag and are
                       reachable when that flag is already set (replayed
                       "first meeting" content, re-triggered introductions).

  Mode 2 --uncertainty — Passages with the highest spread between minimum
                         and maximum flags set on arrival (most ambiguous
                         narrative context). Shows top N.

  Mode 3 --passage PID — Full context audit for one passage: every distinct
                         flag state under which it is reachable.

  Mode 4 --audit       — Full dump of all flag states for every passage.

  Mode 5 --flag FLAG   — All passages where FLAG is uncertain (reachable
                         both with and without it set).

Scaling:
    Adventures with many independent optional flags (e.g. open hub towns)
    produce a combinatorial explosion of (passage, flag-set) states. Two caps
    are available to keep the BFS tractable:

    --per-passage-cap N (default 200)
        Stop collecting new flag-states for a passage once N distinct arrival
        states have been seen for it. BFS continues into the rest of the graph,
        so every passage is reached; only the per-passage flag variety is
        sampled. This is the recommended guard for large adventures — it gives
        broad coverage with a bounded runtime.

    --max-states N (default 0 = unlimited)
        Hard stop on total visited (passage, flags) pairs. Acts as a safety
        net. With --per-passage-cap in effect this limit is rarely needed.

    Both caps produce partial results. Re-entry bugs are almost always caught
    even with low per-passage caps because the violation path is short (visit
    setter, loop back). Use --per-passage-cap 0 for a fully exact run on small
    adventures, or --passage / --flag for targeted deep-dives.

Usage:
    py analyse_paths.py --adventure black_flag_running
    py analyse_paths.py --adventure black_flag_running --uncertainty --top 30
    py analyse_paths.py --adventure black_flag_running --passage a_42
    py analyse_paths.py --adventure black_flag_running --flag met_harlow
    py analyse_paths.py --adventure black_flag_running --audit
    py analyse_paths.py --adventure tide_of_the_leviathan --per-passage-cap 0
"""

import json
import sys
import argparse
from collections import defaultdict, deque


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_adventure(name: str) -> dict:
    path = f'adventures/{name}.json'
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f'ERROR: Adventure file not found: {path}')
    except json.JSONDecodeError as e:
        sys.exit(f'ERROR: Invalid JSON in {path}: {e}')


# ---------------------------------------------------------------------------
# BFS state-space traversal
# ---------------------------------------------------------------------------

def apply_arrival_effects(passage: dict, flags: frozenset) -> frozenset:
    """Return flags AFTER this passage's set_flags / clear_flags have fired."""
    new_flags = set(flags)
    for f in passage.get('set_flags', []):
        new_flags.add(f)
    for f in passage.get('clear_flags', []):
        new_flags.discard(f)
    return frozenset(new_flags)


def get_successor_pids(passage: dict, flags_after: frozenset) -> list:
    """
    Passage IDs reachable from this passage given post-arrival flags.
    Respects requires_flag / requires_no_flag on choices.
    """
    successors = []

    for c in passage.get('choices', []):
        rf = c.get('requires_flag')
        rnf = c.get('requires_no_flag')
        rnfs = c.get('requires_no_flags', [])
        if rf and rf not in flags_after:
            continue
        if rnf and rnf in flags_after:
            continue
        if any(f in flags_after for f in rnfs):
            continue
        successors.append(c['goto'])

    combat = passage.get('combat', {})
    if combat.get('win_goto'):
        successors.append(combat['win_goto'])
    if combat.get('flee_allowed') and combat.get('flee_goto'):
        successors.append(combat['flee_goto'])

    tl = passage.get('test_luck', {})
    for field in ('lucky_goto', 'unlucky_goto'):
        pid = tl.get(field)
        if pid:
            successors.append(pid)

    return successors


def run_bfs(
    adventure: dict,
    max_states: int = 0,
    per_passage_cap: int = 0,
    uncapped_passages: set | None = None,
) -> tuple[dict, int, bool, int]:
    """
    BFS over (passage_id, frozenset_of_flags) states.

    Args:
        max_states        — hard stop on total visited states (0 = unlimited).
        per_passage_cap   — stop collecting new flag-states for a passage once
                            this many have been seen for it (0 = unlimited).
                            New visits to a capped passage are still marked
                            visited (draining queue duplicates) but their
                            successors are not enqueued, so the cap propagates
                            forward cleanly. BFS continues into the rest of the
                            graph, giving every passage a chance to be reached.
        uncapped_passages — set of passage IDs exempt from per_passage_cap
                            (used by --passage mode to get the full picture for
                            one specific passage without lifting the global cap).

    Returns:
        arrival_states    — passage_id -> set of frozensets (flags on arrival,
                            BEFORE this passage's own set_flags / clear_flags)
        total_states      — total (passage, flags) pairs visited
        global_capped     — True if max_states was hit before BFS completed
        n_passages_capped — number of passages that hit per_passage_cap
    """
    passages = adventure['passages']
    start = adventure.get('start_passage', '1')
    uncapped = uncapped_passages or set()

    arrival_states: dict[str, set] = defaultdict(set)
    visited: set = set()
    passages_capped: set = set()
    queue = deque()
    queue.append((start, frozenset()))

    while queue:
        if max_states and len(visited) >= max_states:
            return dict(arrival_states), len(visited), True, len(passages_capped)

        pid, flags = queue.popleft()
        state = (pid, flags)
        if state in visited:
            continue
        visited.add(state)

        if pid not in passages:
            continue  # broken goto — skip (existing validator catches these)

        # Per-passage cap: once we have enough flag-state variety for this
        # passage, stop expanding from it. It has still been "reached" for
        # coverage purposes; we just don't keep adding new flag permutations.
        if (per_passage_cap
                and pid not in uncapped
                and len(arrival_states[pid]) >= per_passage_cap):
            passages_capped.add(pid)
            continue

        arrival_states[pid].add(flags)

        p = passages[pid]
        if p.get('ending'):
            continue

        flags_after = apply_arrival_effects(p, flags)

        for succ_pid in get_successor_pids(p, flags_after):
            succ_state = (succ_pid, flags_after)
            if succ_state not in visited:
                queue.append((succ_pid, flags_after))

    return dict(arrival_states), len(visited), False, len(passages_capped)


# ---------------------------------------------------------------------------
# Mode 1: Re-entry detection
# ---------------------------------------------------------------------------

def report_reentry(adventure: dict, arrival_states: dict, total_states: int) -> None:
    """
    Find passages that SET a flag and are also reachable when that flag is
    already in the arrival flags. These passages replay their content in a
    context they were not written for.

    Two sub-classes:
      LOOP    — only this passage sets the flag; it is reached via a route
                that loops back through itself (or arrives via another setter
                of the same flag that is itself downstream).
      PARALLEL — multiple passages set the same flag (different routes to the
                same narrative outcome). If the flag is pre-set because a
                DIFFERENT setter was visited first, this is usually benign.
                Only worth checking if the texts of the parallel setters are
                not equivalent.
    """
    passages = adventure['passages']

    # Build flag -> list of passages that set it
    flag_setters: dict[str, list] = {}
    for pid, p in passages.items():
        for f in p.get('set_flags', []):
            flag_setters.setdefault(f, []).append(pid)

    print('RE-ENTRY DETECTION')
    print('=' * 64)
    print('Passages that set a flag and are reachable with that flag already set.')
    print()
    print('  LOOP     — only one setter; the flag is pre-set on arrival -> genuine re-entry bug.')
    print('  PARALLEL — multiple setters; flag may be pre-set by a sibling setter on a')
    print('             different branch. Review whether the two passages\' texts are')
    print('             equivalent; if not, one branch is replaying incorrect content.')
    print()

    hits = []
    for pid, p in passages.items():
        set_here = p.get('set_flags', [])
        if not set_here:
            continue
        states = arrival_states.get(pid, set())
        for f in set_here:
            pre_set = [fs for fs in states if f in fs]
            if pre_set:
                all_setters = flag_setters.get(f, [])
                kind = 'LOOP' if len(all_setters) == 1 else 'PARALLEL'
                siblings = [s for s in all_setters if s != pid]
                hits.append((kind, pid, f, pre_set, siblings))

    if not hits:
        print('CLEAN — No re-entry violations found.')
        return

    loops = [(k, p, f, ps, si) for k, p, f, ps, si in hits if k == 'LOOP']
    parallels = [(k, p, f, ps, si) for k, p, f, ps, si in hits if k == 'PARALLEL']

    print(f'{len(hits)} violation(s): {len(loops)} LOOP, {len(parallels)} PARALLEL\n')

    # LOOPs first — highest risk
    if loops:
        print('--- LOOP (genuine re-entry) ---\n')
        for _, pid, flag, pre_set_states, _ in sorted(loops):
            p = passages[pid]
            text = p.get('text', '')
            preview = text[:200].replace('\n', ' / ')
            if len(text) > 200:
                preview += '...'
            print(f'  [{pid}]  sets: {flag}')
            print(f'  Pre-set in {len(pre_set_states)} arrival state(s). '
                  f'(No other passage sets this flag — loop or missed gate.)')
            print(f'  Text: "{preview}"')
            print()

    if parallels:
        print('--- PARALLEL (multiple setters — review for text equivalence) ---\n')
        # Group by flag for readability
        by_flag: dict[str, list] = {}
        for _, pid, flag, pre_set_states, siblings in sorted(parallels):
            by_flag.setdefault(flag, []).append((pid, pre_set_states, siblings))

        for flag, entries in sorted(by_flag.items()):
            all_setters_for_flag = flag_setters.get(flag, [])
            print(f'  Flag: {flag}  (set at: {sorted(all_setters_for_flag)})')
            for pid, pre_set_states, siblings in entries:
                p = passages[pid]
                text = p.get('text', '')
                preview = text[:150].replace('\n', ' / ')
                if len(text) > 150:
                    preview += '...'
                print(f'    [{pid}]  pre-set in {len(pre_set_states)} state(s)  '
                      f'siblings: {siblings}')
                print(f'    Text: "{preview}"')
            print()


# ---------------------------------------------------------------------------
# Mode 2: Flag uncertainty spread
# ---------------------------------------------------------------------------

def report_uncertainty(adventure: dict, arrival_states: dict, total_states: int, top_n: int) -> None:
    """
    Rank passages by the spread between the minimum and maximum number of
    flags set on arrival. A high spread means the passage is reachable in
    wildly different narrative contexts — worth reviewing manually.
    """
    passages = adventure['passages']

    print('FLAG UNCERTAINTY SPREAD')
    print('=' * 64)
    print('Passages ranked by (max_flags_on_arrival - min_flags_on_arrival).')
    print('High spread = reachable in very different narrative contexts.')
    print()

    rows = []
    for pid, states in arrival_states.items():
        if not states:
            continue
        min_flags = min(len(fs) for fs in states)
        max_flags = max(len(fs) for fs in states)
        spread = max_flags - min_flags
        n_states = len(states)
        certain = frozenset.intersection(*states)
        possible = frozenset.union(*states)
        uncertain = possible - certain
        rows.append((pid, spread, min_flags, max_flags, n_states, uncertain))

    rows.sort(key=lambda r: (-r[1], -r[3], -r[4]))
    rows = rows[:top_n]

    if not rows:
        print('No passages found.')
        return

    print(f'Top {len(rows)} passages by flag spread:\n')
    for pid, spread, mn, mx, n_states, uncertain in rows:
        p = passages.get(pid, {})
        ptype = ('ending' if p.get('ending') else
                 'combat' if p.get('combat') else
                 'luck' if p.get('test_luck') else
                 'choices')
        print(f'  [{pid}]  spread={spread}  (min {mn} -> max {mx} flags)  '
              f'{n_states} state(s)  [{ptype}]')
        if uncertain:
            print(f'         Uncertain: {sorted(uncertain)}')
        print()


# ---------------------------------------------------------------------------
# Mode 3: Single passage context audit
# ---------------------------------------------------------------------------

def report_passage(adventure: dict, arrival_states: dict, pid: str) -> None:
    """Full context dump for one passage."""
    passages = adventure['passages']

    if pid not in passages:
        print(f'ERROR: Passage "{pid}" not found in adventure.')
        return

    states = arrival_states.get(pid, set())
    p = passages[pid]

    print(f'CONTEXT AUDIT — [{pid}]')
    print('=' * 64)

    text = p.get('text', '')
    preview = text[:400].replace('\n', ' / ')
    if len(text) > 400:
        preview += '...'
    print(f'Text: "{preview}"')
    print()

    if p.get('set_flags'):
        print(f'Sets flags: {p["set_flags"]}')
    if p.get('clear_flags'):
        print(f'Clears flags: {p["clear_flags"]}')

    # Uncertainty summary
    if states:
        certain = frozenset.intersection(*states)
        possible = frozenset.union(*states)
        uncertain = possible - certain

        print(f'\n{len(states)} distinct arrival state(s):')
        print(f'  Always set on arrival:  {sorted(certain) if certain else "(none)"}')
        print(f'  Uncertain (varies):     {sorted(uncertain) if uncertain else "(none)"}')
        print(f'  Min flags on arrival:   {min(len(fs) for fs in states)}')
        print(f'  Max flags on arrival:   {max(len(fs) for fs in states)}')

        # Check re-entry
        for f in p.get('set_flags', []):
            pre_set = [fs for fs in states if f in fs]
            if pre_set:
                print(f'\n  WARNING: Sets [{f}] but reachable with it already set '
                      f'({len(pre_set)} state(s)) — re-entry violation.')

        print('\nAll arrival states:')
        for i, fs in enumerate(sorted(states, key=lambda s: (len(s), sorted(s))), 1):
            print(f'  {i:3d}. {sorted(fs) if fs else "(no flags set)"}')
    else:
        print('\nNot reachable from start passage.')


# ---------------------------------------------------------------------------
# Mode 4: Full audit dump
# ---------------------------------------------------------------------------

def report_audit(adventure: dict, arrival_states: dict) -> None:
    passages = adventure['passages']
    print(f'FULL CONTEXT AUDIT — {adventure.get("title", "Unknown")}')
    print('=' * 64)
    print()
    for pid in sorted(passages.keys()):
        states = arrival_states.get(pid, set())
        if not states:
            print(f'[{pid}] — NOT REACHABLE')
            continue
        print(f'[{pid}] — {len(states)} state(s):')
        for fs in sorted(states, key=lambda s: (len(s), sorted(s))):
            print(f'  {sorted(fs) if fs else "(no flags)"}')
        print()


# ---------------------------------------------------------------------------
# Mode 5: Flag-specific uncertainty report
# ---------------------------------------------------------------------------

def report_flag(adventure: dict, arrival_states: dict, flag: str) -> None:
    """Show all passages where FLAG is uncertain (reachable both with and without)."""
    passages = adventure['passages']

    print(f'FLAG UNCERTAINTY — "{flag}"')
    print('=' * 64)

    # Who sets this flag?
    setters = [pid for pid, p in passages.items() if flag in p.get('set_flags', [])]
    checkers_rf = [(pid, c) for pid, p in passages.items()
                   for c in p.get('choices', []) if c.get('requires_flag') == flag]
    checkers_rnf = [(pid, c) for pid, p in passages.items()
                    for c in p.get('choices', []) if c.get('requires_no_flag') == flag]

    print(f'Set at: {setters}')
    print(f'Checked (requires_flag) at: {[pid for pid, _ in checkers_rf]}')
    print(f'Checked (requires_no_flag) at: {[pid for pid, _ in checkers_rnf]}')
    print()

    # Re-entry on setters
    for pid in setters:
        states = arrival_states.get(pid, set())
        pre_set = [fs for fs in states if flag in fs]
        if pre_set:
            print(f'  RE-ENTRY: [{pid}] sets [{flag}] and is reachable with it already set '
                  f'({len(pre_set)} arrival state(s))')
        else:
            print(f'  OK: [{pid}] sets [{flag}] and is never reached with it pre-set')
    print()

    # Passages where flag is uncertain
    uncertain_at = []
    for pid, states in arrival_states.items():
        if not states:
            continue
        possible = frozenset.union(*states)
        certain = frozenset.intersection(*states)
        if flag in possible and flag not in certain:
            uncertain_at.append((pid, len(states)))

    uncertain_at.sort(key=lambda x: -x[1])

    print(f'Passages where [{flag}] is uncertain ({len(uncertain_at)} total):')
    for pid, n in uncertain_at:
        p = passages.get(pid, {})
        gated = any(
            c.get('requires_flag') == flag or c.get('requires_no_flag') == flag
            for c in p.get('choices', [])
        )
        tag = ' [choices branch on this — OK]' if gated else ''
        print(f'  [{pid}]  {n} state(s){tag}')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Analyse arrival flag contexts for StoryForge adventure passages.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--adventure', required=True, metavar='NAME',
                        help='Adventure ID (filename without .json)')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--uncertainty', action='store_true',
                      help='Rank passages by flag-spread (most ambiguous first)')
    mode.add_argument('--passage', metavar='ID',
                      help='Full context audit for one passage')
    mode.add_argument('--audit', action='store_true',
                      help='Dump all flag states for every passage')
    mode.add_argument('--flag', metavar='FLAG',
                      help='Show all passages where FLAG is uncertain')

    parser.add_argument('--top', type=int, default=20, metavar='N',
                        help='Number of results to show in --uncertainty mode (default: 20)')
    parser.add_argument('--per-passage-cap', type=int, default=200, metavar='N',
                        help='Max distinct flag-states tracked per passage (default: 200; '
                             '0 = unlimited). Keeps BFS tractable on adventures with many '
                             'independent optional flags. Every passage is still reached; '
                             'only per-passage flag variety is sampled.')
    parser.add_argument('--max-states', type=int, default=0, metavar='N',
                        help='Hard stop on total visited (passage, flags) pairs '
                             '(default: 0 = unlimited). Safety net; rarely needed when '
                             '--per-passage-cap is active.')

    args = parser.parse_args()

    adventure = load_adventure(args.adventure)
    n_passages = len(adventure['passages'])
    title = adventure.get('title', args.adventure)

    # In --passage mode, lift the per-passage cap for the target so the audit
    # sees its complete flag picture.
    uncapped = {args.passage} if args.passage else set()

    print(f'Analysing "{title}"...', end=' ', flush=True)
    arrival_states, total_states, global_capped, n_capped = run_bfs(
        adventure,
        max_states=args.max_states,
        per_passage_cap=args.per_passage_cap,
        uncapped_passages=uncapped,
    )
    n_reached = len(arrival_states)

    # Build header suffix
    tags = []
    if global_capped:
        tags.append(f'GLOBAL CAP {args.max_states:,}')
    if n_capped:
        tags.append(f'{n_capped} passage(s) per-passage-capped')
    tag_str = '  [' + ', '.join(tags) + ']' if tags else ''
    print(f'done. ({total_states:,} states, {n_reached}/{n_passages} passages reached){tag_str}\n')

    if global_capped:
        print(f'  *** Global cap hit ({args.max_states:,} states) — results are partial. ***')
        print(f'  Lower --per-passage-cap or use --passage / --flag for targeted analysis.\n')
    elif n_capped and args.per_passage_cap:
        print(f'  Note: {n_capped}/{n_passages} passages were per-passage-capped at '
              f'{args.per_passage_cap} states. Flag variety at those passages is sampled,')
        print(f'  not exhaustive. Re-entry bugs are still reliably detected. Use')
        print(f'  --per-passage-cap 0 for a fully exact run (may be slow on large adventures).\n')

    if args.passage:
        report_passage(adventure, arrival_states, args.passage)
    elif args.audit:
        report_audit(adventure, arrival_states)
    elif args.uncertainty:
        report_uncertainty(adventure, arrival_states, total_states, args.top)
    elif args.flag:
        report_flag(adventure, arrival_states, args.flag)
    else:
        report_reentry(adventure, arrival_states, total_states)


if __name__ == '__main__':
    main()
