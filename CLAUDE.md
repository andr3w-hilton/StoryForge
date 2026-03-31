# StoryForge

A data-driven Fighting Fantasy-style gamebook engine. Adventures are defined in JSON files; the engine renders them as interactive web gamebooks. Inspired by Ian Livingstone's Fighting Fantasy series.

## Architecture

```
server.py                    # HTTP server, adventure list + JSON API (~90 lines)
index.html                   # Single-file client — all CSS, HTML, JS (~650 lines)
adventures/                  # Adventure JSON files (drop in to add new stories)
  the_warlocks_cave.json     # Sample adventure exercising all mechanics
Dockerfile                   # Python 3.11-slim, port 8080
```

**Server:** Pure HTTP, no WebSockets. `ThreadingHTTPServer` on port 8080.
**Client:** Vanilla JS, no frameworks, no build tools. All game state lives in the browser.
**Adventures:** Fully data-driven JSON. New adventures require no code changes.

## Running

```bash
python3 server.py
# Open http://localhost:8080
```

## API Endpoints

| Endpoint | Response |
|---|---|
| `GET /` | Serves `index.html` |
| `GET /api/adventures` | List of `{ id, title, author, introduction }` |
| `GET /api/adventures/<id>` | Full adventure JSON |

## Adventure JSON Schema

Each file in `adventures/` defines a complete adventure:

```json
{
    "title": "...",
    "author": "...",
    "version": "1.0",
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
        "magic_sword": { "name": "Enchanted Sword", "type": "weapon", "skill_bonus": 2 },
        "provisions": { "name": "Provisions", "type": "consumable", "stamina_restore": 4 }
    },

    "enemies": {
        "goblin": { "name": "Goblin Scout", "skill": 5, "stamina": 5 }
    },

    "passages": { ... }
}
```

### Passage Fields

```json
"1": {
    "text": "Narrative text shown to player. Supports \\n for paragraphs.",

    "choices": [
        { "text": "Button label", "goto": "2" },
        { "text": "Secret door (requires lantern)", "goto": "3", "requires_item": "lantern" },
        { "text": "If flag set",    "goto": "4", "requires_flag": "met_wizard" },
        { "text": "If flag not set","goto": "5", "requires_no_flag": "door_locked" }
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
1. **select** — adventure list fetched from `/api/adventures`
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

## Adding a New Adventure

1. Create `adventures/my_adventure.json` following the schema above
2. Drop the file in — the server picks it up automatically on next request
3. Start at passage `"1"` (engine always begins there)
4. Must have at least one `"ending": true` passage

## Theme / Style

Dark parchment aesthetic — CSS custom properties in `:root`:
- `--parchment` / `--parchment-hi` — background surfaces
- `--ink` / `--ink-dim` — text colours
- `--gold` / `--gold-hi` — headings, gold accents
- `--red-hi` — combat, danger
- `--green-hi` — positive outcomes
- `--blue-hi` — player/skill colour

Fonts: **IM Fell English** (serif, passage text + headings), **Share Tech Mono** (UI elements).
