# StoryForge - Implementation Plan

## Context
Build a Fighting Fantasy-style gamebook engine inspired by Ian Livingstone's books. Data-driven design where adventures are defined in JSON and the engine renders them as interactive web gamebooks. All game state lives client-side — the server is just an HTTP file server.

## File Structure
```
StoryForge/
  server.py                          # HTTP server (~80 lines)
  index.html                         # Single-file client (CSS + JS)
  adventures/
    the_warlocks_cave.json           # Sample mini-adventure
  Dockerfile
  .gitignore
  CLAUDE.md
```

## Adventure JSON Format
Each adventure is a JSON file with:
- **Metadata**: title, author, version, introduction
- **Character config**: base stats + dice (Skill 6+1d6, Stamina 12+2d6, Luck 6+1d6)
- **Items dict**: keyed by ID, with name, type, skill_bonus, description
- **Enemies dict**: keyed by ID, with name, skill, stamina
- **Passages dict**: keyed by string ID ("1", "2", etc.), each with:
  - `text` — narrative
  - `choices` — array of {text, goto, requires_item?, requires_flag?, requires_no_flag?}
  - `combat` — {enemy, win_goto, flee_goto?, flee_allowed?, flee_stamina_cost?}
  - `test_luck` — {lucky_text, lucky_goto, unlucky_text, unlucky_goto, stamina costs}
  - `add_items`, `remove_items`, `set_flags`, `clear_flags` — passage arrival effects
  - `add_stamina`, `add_skill`, `add_luck` — stat modifications
  - `ending`, `ending_type` — marks victory/defeat endings

## Server (server.py)
Minimal HTTP server matching orb-arena's style:
- `GET /` — serves index.html
- `GET /api/adventures` — lists available adventures (id, title, author)
- `GET /api/adventures/<id>` — serves full adventure JSON
- `ThreadingHTTPServer` on port 8080

## Client (index.html)
Dark parchment theme with CSS custom properties. Three screens:

1. **Adventure Select** — fetch list from API, pick an adventure
2. **Character Creation** — dice roll animation for Skill/Stamina/Luck, show starting gear
3. **Game Screen** — passage text panel + sidebar (stats bars, inventory, provisions)

### Game State (all client-side)
```javascript
gameState = {
    adventure, currentPassage,
    skill: {current, max}, stamina: {current, max}, luck: {current, max},
    items: [], flags: Set(), provisions: 0,
    combat: null, log: []
}
```

### Core Mechanics
- **Passage navigation**: apply arrival effects, check death, render choices filtered by conditions
- **Combat**: 2d6 + skill comparison each round, 2 stamina damage to loser, optional "Test Your Luck" to modify damage
- **Test Your Luck**: roll 2d6 <= current luck = lucky, luck decreases by 1 regardless
- **Provisions**: restore 4 stamina (outside combat only), up to max
- **Death**: stamina <= 0 triggers death screen with "Try Again"

## Sample Adventure: "The Warlock's Cave"
5 passages exercising all mechanics:
- Passage 1: Cave entrance — left/right tunnel + hidden lantern search
- Passage 2: Goblin combat (Skill 5, Stamina 5), flee allowed
- Passage 3: Pit trap — Test Your Luck
- Passage 4: Hidden alcove (requires lantern) — find magic sword (+2 skill)
- Passage 5: Locked door — requires silver_key from goblin, victory ending

## Build Phases

### Phase 1: Skeleton
- server.py with HTTP handler
- index.html with themed CSS, three screens, screen switching
- Minimal JSON adventure (2 passages)
- Wire up: list adventures → load → render passages → navigate choices

### Phase 2: Character & Stats
- Character creation with dice roll animation
- gameState with stat tracking
- Stat bars in sidebar
- Passage arrival effects (add_stamina, set_flags, etc.)
- Conditional choices (requires_item/flag)
- Death check

### Phase 3: Combat
- Combat UI (enemy stats, attack button, combat log)
- attackRound() — 2d6 + skill comparison
- Test Your Luck in combat (modify damage)
- Flee mechanic
- Item skill bonuses

### Phase 4: Inventory & Provisions
- Inventory panel in sidebar
- Item pickup/removal on passage arrival
- Eat Provisions button
- Item-gated choice visibility

### Phase 5: Luck Tests & Polish
- Standalone Test Your Luck passages
- Ending screens (victory/defeat + Play Again)
- Dice animation, passage transitions
- Mobile responsive layout
- Expand sample adventure to full 5 passages

### Phase 6: Packaging
- Dockerfile, .gitignore, CLAUDE.md

## Verification
- Start server, load adventure select screen
- Roll character, verify stats within expected ranges
- Play through sample adventure hitting all mechanics:
  - Navigate choices, find hidden lantern path
  - Fight goblin, test luck in combat, flee and retry
  - Hit pit trap luck test
  - Pick up magic sword, verify skill bonus in combat
  - Use provisions to heal
  - Reach victory ending with silver key
  - Die and use Try Again
- Test on mobile/tablet (touch-friendly buttons, responsive layout)
