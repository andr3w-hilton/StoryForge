# StoryForge

A data-driven Fighting Fantasy-style gamebook engine. Adventures are defined in JSON files; the engine renders them as interactive web gamebooks. Inspired by Ian Livingstone's Fighting Fantasy series.

## Architecture

```
server.py                                        # HTTP server for local dev (~90 lines)
index.html                                       # Single-file client — all CSS, HTML, JS (~700 lines)
adventures/
  index.json                                     # Static manifest — adventure list for the select screen
  the_crypt_of_count_valdric.json
  the_scavenger_of_new_babylon_station.json
Dockerfile                                       # Python 3.11-slim, port 8080
```

**Server:** Pure HTTP, no WebSockets. `ThreadingHTTPServer` on port 8080. Used for local dev only.
**Client:** Vanilla JS, no frameworks, no build tools. All game state lives in the browser.
**Adventures:** Fully data-driven JSON. New adventures require no code changes — add JSON, update manifest.
**Hosting:** Deployable as a fully static site (GitHub Pages). No server required in production.

## Running (local dev only)

`server.py` is only needed for local development. In production the site is hosted statically on GitHub Pages — no server required.

```bash
python3 server.py
# Open http://localhost:8080
```

## Static File API

The client fetches two types of file directly — no server API needed in production:

| Fetch | File |
|---|---|
| Adventure list | `adventures/index.json` |
| Full adventure | `adventures/<id>.json` |

`server.py` still serves these paths for local dev. In production (GitHub Pages) the files are served statically.

### adventures/index.json

Manually maintained manifest. **Must be updated when adding a new adventure.** Each entry:

```json
{
    "id": "my_adventure",
    "title": "...",
    "author": "...",
    "introduction": "...",
    "accent_color": "#4a8ab5",
    "genre_tag": "SPACE OPERA",
    "theme_icon": "✦"
}
```

## Item Fields

| Field | Purpose |
|---|---|
| `skill_bonus` | Adds to attack roll in combat (highest in inventory wins, not stacked) |
| `damage_bonus` | Adds to base damage per hit (base 2, highest in inventory wins). Luck modifiers scale with base: lucky = base+1, unlucky = base−1 (min 1) |
| `stamina_restore` | Stamina restored when used as a consumable |

### Choice `style` field

Choices accept an optional `"style"` field that changes button appearance:

| Value | Appearance | Use for |
|---|---|---|
| *(omitted)* | Default parchment | Normal choices |
| `"danger"` | Dark red border, red hover | Flee, retreat, run choices |

## Adventure JSON Schema

Each file in `adventures/` defines a complete adventure:

```json
{
    "title": "...",
    "author": "...",
    "version": "1.0",
    "accent_color": "#5c7d5c",
    "genre_tag": "GOTHIC HORROR",
    "theme_icon": "☠",
    "introduction": "...",

    "character": {
        "skill_base": 6,   "skill_dice": 1,
        "stamina_base": 12, "stamina_dice": 2,
        "luck_base": 6,    "luck_dice": 1,
        "starting_items": ["sword", "lantern"],
        "starting_provisions": 4
    },

    "items": {
        "sword": { "name": "Sword", "type": "weapon", "skill_bonus": 0, "description": "..." },
        "magic_sword": { "name": "Enchanted Sword", "type": "weapon", "skill_bonus": 2, "damage_bonus": 1 },
        "provisions": { "name": "Provisions", "type": "consumable", "stamina_restore": 4 }
    },

    "enemies": {
        "goblin": { "name": "Goblin Scout", "skill": 5, "stamina": 5 }
    },

    "passages": { ... }
}
```

### Card Flourish Fields

Three optional fields drive the visual style of the adventure's card on the select screen:

| Field | Purpose | Example |
|---|---|---|
| `accent_color` | Left border colour + flourish tint | `"#4a8ab5"` |
| `genre_tag` | Uppercase label shown in flourish row | `"SPACE OPERA"` |
| `theme_icon` | Unicode character before the tag | `"✦"` |

Adventures without these fields fall back to the default gold border and no flourish row.

### Passage Fields

```json
"1": {
    "text": "Narrative text shown to player. Supports \\n for paragraphs.",

    "choices": [
        { "text": "Button label", "goto": "2" },
        { "text": "Secret door (requires lantern)", "goto": "3", "requires_item": "lantern" },
        { "text": "If flag set",    "goto": "4", "requires_flag": "met_wizard" },
        { "text": "If flag not set","goto": "5", "requires_no_flag": "door_locked" },
        { "text": "Run for your life", "goto": "6", "style": "danger" }
    ],

    "combat": {
        "enemy": "goblin",
        "win_goto": "10",
        "flee_goto": "1",
        "flee_allowed": true,
        "flee_stamina_cost": 2
    },

    "test_luck": {
        "lucky_text": "...", "lucky_goto": "10",
        "unlucky_text": "...", "unlucky_goto": "10",
        "lucky_stamina_cost": 0,
        "unlucky_stamina_cost": 3,
        "lucky_add_items": ["silver_key"],
        "unlucky_add_items": []
    },

    "add_items":    ["silver_key"],
    "remove_items": ["sword"],
    "set_flags":    ["defeated_goblin"],
    "clear_flags":  ["door_locked"],
    "add_stamina":  -2,
    "add_skill":    1,
    "add_luck":     -1,

    "ending": true,
    "ending_type": "victory"
}
```

**Rules:**
- Passage IDs are strings — `"1"`, `"2a"`, `"death_1"` all valid
- A passage can only have one of: `choices`, `combat`, `test_luck`, or `ending`
- Arrival effects (`add_items`, `set_flags`, etc.) always apply before rendering
- Items best `skill_bonus` applies in combat (not stacked — highest wins)

## Client Architecture

### Game State
```javascript
gameState = {
    adventure,          // loaded adventure JSON
    currentPassage,     // string ID
    skill:   { current, max },
    stamina: { current, max },
    luck:    { current, max },
    items:   [],        // item IDs in inventory
    flags:   Set(),     // story state flags
    provisions,
    combat:  null,      // active combat state or null
    inCombat: false
}
```

### Key Functions
| Function | Purpose |
|---|---|
| `navigateToPassage(id)` | Apply arrival effects, check death, render passage |
| `renderPassage(passage)` | Route to choices / combat / luck test / ending |
| `isChoiceAvailable(choice)` | Check requires_item / requires_flag conditions |
| `attackRound()` | Resolve one combat round (2d6 + skill comparison) |
| `testLuck()` | Roll 2d6 vs luck, decrement luck, return boolean |
| `testLuckInCombat()` | Modify pending combat damage via luck roll |
| `resolveLuckTest(luckDef)` | Handle standalone passage luck tests |
| `useProvisions()` | Restore stamina (outside combat only) |
| `updateSidebar()` | Refresh stat bars + inventory panel |
| `getEffectiveSkill()` | skill.current + best weapon skill_bonus |

### Three Screens
1. **select** — adventure list fetched from `adventures/index.json`
2. **create** — character rolling (animated), starting gear display
3. **game** — passage panel (left) + stats/inventory sidebar (right)

## Combat Mechanics (Fighting Fantasy rules)
1. Both sides roll 2d6 + their SKILL → **Attack Strength**
2. Higher Attack Strength deals **2 STAMINA** damage to the loser
3. Tie → no damage
4. After each round (before applying damage), player may **Test Your Luck**:
   - Player wounded enemy: Lucky = 3 dmg, Unlucky = 1 dmg
   - Enemy wounded player: Lucky = 1 dmg, Unlucky = 3 dmg
5. LUCK decreases by 1 on every luck test regardless of outcome
6. Enemy STAMINA ≤ 0 → victory → navigate to `win_goto`
7. Player STAMINA ≤ 0 → death screen

## Expanding or Writing Adventures

See `notes/EXPANSION_GUIDE.md` for the full process — spec writing, flag architecture, Opus prompting, merge steps, and the flag audit checklist. Read it at the start of any session that involves expanding an existing adventure or writing a new one from scratch.

## Adding a New Adventure

1. Create `adventures/my_adventure.json` following the schema above
2. Add an entry to `adventures/index.json` (the static manifest)
3. Start passage defaults to `"1"`. For adventures that use a prefixed ID scheme (e.g. `"s_1"`), add `"start_passage": "s_1"` at the top level of the adventure JSON.
4. Must have at least one `"ending": true` passage
5. Recommended: run the passage validator to check all gotos resolve and all passages are reachable

```bash
python3 -c "
import json
with open('adventures/my_adventure.json') as f:
    d = json.load(f)
passages = d['passages']
errors = []
visited = set()
queue = ['1']
while queue:
    cur = queue.pop()
    if cur in visited: continue
    visited.add(cur)
    pp = passages.get(cur, {})
    for c in pp.get('choices', []):
        if c['goto'] not in passages: errors.append(f'[{cur}] bad goto {c[\"goto\"]}')
        else: queue.append(c['goto'])
    for field in ['win_goto','flee_goto']:
        t = pp.get('combat', {}).get(field)
        if t:
            if t not in passages: errors.append(f'[{cur}] bad {field} {t}')
            else: queue.append(t)
    for field in ['lucky_goto','unlucky_goto']:
        t = pp.get('test_luck', {}).get(field)
        if t:
            if t not in passages: errors.append(f'[{cur}] bad {field} {t}')
            else: queue.append(t)
unreachable = set(passages.keys()) - visited
if unreachable: errors.append(f'Unreachable: {sorted(unreachable)}')
print('OK' if not errors else '\n'.join(errors))
"
```

## Theme / Style

Dark parchment aesthetic — CSS custom properties in `:root`:
- `--parchment` / `--parchment-hi` — background surfaces
- `--ink` / `--ink-dim` — text colours
- `--gold` / `--gold-hi` — headings, gold accents
- `--red-hi` — combat, danger
- `--green-hi` — positive outcomes
- `--blue-hi` — player/skill colour

Fonts: **IM Fell English** (serif, passage text + headings), **Share Tech Mono** (UI elements).

### Adventure Card Design

Each card on the select screen has:
- A **coloured left border** driven by `--card-accent` (set from `accent_color`), falling back to `--gold`
- A **flourish row** above the title: `<icon>  <GENRE TAG>` in Share Tech Mono, tinted with the accent colour, with a thin border around the tag word
- **1.75rem gap** between cards and **1.4rem 1.5rem** padding so each card reads as a distinct object

Adventures without `accent_color`/`genre_tag`/`theme_icon` render with gold border and no flourish row — fully backwards compatible.
