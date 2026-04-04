# StoryForge — TrimUI Native Port

A native SDL2 port of StoryForge for NextUI on TrimUI handheld devices.
Adventures remain fully data-driven JSON — only the rendering and input layer changes.

---

## Target Platform

| Property | Value |
|---|---|
| Firmware | NextUI (LoveRetro/NextUI) |
| Devices | TrimUI Smart Pro, TrimUI Brick |
| Platform ID | `tg5040` |
| SoC | Allwinner A133P |
| CPU | Quad-core Cortex-A53 (aarch64 / ARM64) |
| OS | Linux 4.9, glibc userspace |
| GPU | PowerVR GE8300 |
| Resolution | 1280×720 (Smart Pro) · 1024×768 (Brick) |
| Pixel format | RGB565 (16-bit) |
| Refresh rate | 60 Hz |

---

## .pak Format

A NextUI tool pak is just a **directory with a `.pak` extension** containing a `launch.sh` script.

```
Tools/tg5040/StoryForge.pak/
  launch.sh               # entry point, must be chmod +x
  storyforge.elf          # compiled ARM64 binary
  adventures/             # JSON adventure files (copied from main project)
    index.json
    the_crypt_of_count_valdric.json
    the_scavenger_of_new_babylon_station.json
    tide_of_the_leviathan.json
  fonts/
    IMFellEnglish-Regular.ttf
    ShareTechMono-Regular.ttf
  pak.json                # Pak Store metadata
```

**launch.sh:**
```sh
#!/bin/sh
cd $(dirname "$0")
./storyforge.elf
```

**Environment variables available at runtime:**
- `SDCARD_PATH` — `/mnt/SDCARD`
- `LOGS_PATH` — path for log output
- `DEVICE` — `smartpro` or `brick` (use this to switch resolution)
- `IS_NEXT` — `"yes"` (confirms NextUI environment)

---

## Tech Stack

| Component | Choice | Notes |
|---|---|---|
| Language | C (C99) | Matches the NextUI ecosystem; manageable for a text game |
| Display | SDL2 2.26.1 | Ships with TrimUI SDK |
| Text | SDL2_ttf | Ships with TrimUI SDK |
| JSON | cJSON | Single .c/.h drop-in |
| Build | Makefile | Simple two-target: desktop + ARM64 |
| Cross-compile | Docker | NextUI SDK Docker image |

---

## Development Strategy

Write and test on **desktop SDL2** first. Cross-compile for ARM64 only when milestones are stable.

```
PC (SDL2, fast iteration) ──► Cross-compile ──► Test on device
```

This means most development requires no TrimUI device.

---

## Project Structure (target)

```
StoryForge_TrimUI/
  PLAN.md                 # this file
  Makefile                # desktop + ARM64 build targets
  src/
    main.c                # entry point, screen routing
    engine.c / engine.h   # passage navigation, game state
    combat.c / combat.h   # Fighting Fantasy combat loop
    render.c / render.h   # SDL2 text + UI drawing
    input.c / input.h     # gamepad button mapping
    json_load.c / json_load.h  # adventure JSON parsing (wraps cJSON)
    cJSON.c / cJSON.h     # vendored JSON library
  assets/
    fonts/                # TTF fonts
  adventures/             # symlink or copy from parent project
  pak/
    launch.sh
    pak.json
```

---

## Game State (mirrors JS engine)

```c
typedef struct {
    Adventure *adventure;    // loaded adventure data
    char current_passage[64];
    int skill_current, skill_max;
    int stamina_current, stamina_max;
    int luck_current, luck_max;
    char items[MAX_ITEMS][64];
    int item_count;
    char flags[MAX_FLAGS][64];
    int flag_count;
    int provisions;
    CombatState *combat;     // NULL when not in combat
} GameState;
```

---

## Screen Flow

```
Adventure Select ──► Character Create ──► Game (passage loop)
                                              │
                                    ┌─────────┴──────────┐
                                  Choices             Combat
                                  Luck Test           Death screen
                                  Ending
```

---

## Input Mapping (TrimUI buttons → SDL2)

| Physical Button | SDL Gamepad | Action |
|---|---|---|
| D-pad Up/Down | DPAD_UP / DPAD_DOWN | Navigate choice list |
| A (confirm) | SDL_CONTROLLER_BUTTON_A | Select choice / confirm |
| B (back) | SDL_CONTROLLER_BUTTON_B | Back / cancel |
| Start | SDL_CONTROLLER_BUTTON_START | Pause / menu |
| Select | SDL_CONTROLLER_BUTTON_BACK | Use provisions |

---

## Milestones

### M1 — Toolchain + Hello World pak
- [ ] SDL2 window opens on desktop
- [ ] Cross-compiled `.elf` runs on device (or emulator)
- [ ] `.pak` folder structure correct, appears in NextUI Tools menu
- [ ] Displays a string of text on screen

### M2 — Text Rendering
- [ ] Load and render IM Fell English TTF via SDL2_ttf
- [ ] Word-wrap function for passage text (SDL_ttf does not wrap natively)
- [ ] Scrollable text if passage exceeds screen height
- [ ] Basic dark parchment background colour

### M3 — JSON Loading + Passage Navigation
- [ ] Parse adventure JSON with cJSON
- [ ] Load passages, choices, enemies, items
- [ ] Navigate between passages via button input
- [ ] Arrival effects: add_items, set_flags, add_stamina etc.

### M4 — Full Game Logic
- [ ] Inventory system
- [ ] Flag system (set_flags / clear_flags / requires_flag / requires_no_flag)
- [ ] Item requirements on choices
- [ ] Stat modifiers (add_skill, add_luck, add_stamina)
- [ ] Provisions (useProvisions outside combat)

### M5 — Combat Loop
- [ ] Full Fighting Fantasy combat (2d6 + SKILL comparison)
- [ ] Luck test in combat (modify pending damage)
- [ ] Flee mechanic (flee_allowed, flee_stamina_cost)
- [ ] Death screen on stamina ≤ 0

### M6 — Adventure Select Screen
- [ ] Parse index.json
- [ ] Display adventure list with title, author, genre tag
- [ ] Accent colour per adventure (SDL rectangle border)
- [ ] D-pad navigation + A to select

### M7 — Character Creation Screen
- [ ] Animated stat rolling (SKILL, STAMINA, LUCK)
- [ ] Starting items display
- [ ] Confirm to begin

### M8 — Polish + Pak Release
- [ ] Match dark parchment aesthetic
- [ ] Brick vs Smart Pro resolution switching via `DEVICE` env var
- [ ] pak.json metadata for Pak Store
- [ ] Adventure JSON files bundled
- [ ] Tested on real hardware

---

## Key Differences from Web Version

| Web | Native Port |
|---|---|
| HTML/CSS layout | Manual SDL2 rectangle + text drawing |
| Google Fonts via CDN | Bundled TTF files |
| Mouse/keyboard | D-pad + buttons only |
| Automatic text wrap | Custom word-wrap function needed |
| Sidebar always visible | May need to toggle sidebar (screen space) |
| Scrolling via browser | Manual scroll offset tracking |

---

## Open Questions

- **Developer platform:** Windows (WSL2) / Mac / Linux? (affects toolchain setup)
- **Language:** Stick with C, or evaluate Rust/Go? (both cross-compile to ARM64 trivially)
- **Fonts:** Can we bundle IM Fell English + Share Tech Mono? (both are OFL licensed — yes)
- **Screen layout:** Sidebar always shown, or toggle with a button?
- **Save state:** Should the port support save/resume? (not in web version currently)

---

## Resources

- NextUI repo: `github.com/LoveRetro/NextUI`
- NextUI PAKS.md: documents the pak format and toolchain
- TrimUI SDK: ships SDL2-2.26.1.GE8300 + SDL2_ttf + GLESv2
- cJSON: `github.com/DaveGamble/cJSON` (single file, MIT licensed)
- SDL2_ttf docs: `wiki.libsdl.org/SDL2_ttf`
- Existing pak examples: `minui-remote-terminal`, `nextui-video-player`, `minui-gallery`
