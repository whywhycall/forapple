# Replay Mode Spec

## Goal
Do **not** infer, transform, or auto-optimize user behavior.

The app should only:
1. Record user-defined actions
2. Normalize coordinates by screen size
3. Replay them exactly
4. Allow human interruption/cancel at any time

---

## Core Principle
**Copy only. Do not think.**

The app is not an AI planner.
It is a deterministic replay tool.

---

## Action Model
Each macro is a sequence of actions:

```json
[
  {"type": "tap", "x_ratio": 0.91, "y_ratio": 0.72},
  {"type": "wait", "seconds": 0.8},
  {"type": "swipe", "x1_ratio": 0.50, "y1_ratio": 0.78, "x2_ratio": 0.50, "y2_ratio": 0.28, "duration": 0.25},
  {"type": "wait", "seconds": 8.0}
]
```

---

## Rules
- No automatic variation
- No app-specific assumptions
- No automatic branching
- No AI-generated step changes
- Human handles exceptions/popups/cancel

---

## Required UI
- Add Tap
- Add Swipe
- Add Wait
- Delete Step
- Save Macro
- Load Macro
- Play
- Pause
- Stop
- Next Step
- Resume From Current Step

---

## Resolution Handling
Store coordinates as ratios:
- `x_ratio = x / screen_width`
- `y_ratio = y / screen_height`

Replay by converting back:
- `x = round(x_ratio * current_screen_width)`
- `y = round(y_ratio * current_screen_height)`

This keeps behavior consistent across iPhone 17 and iPad 10.

---

## Human-in-the-loop Model
Automation handles repetition only.
Human handles:
- unexpected screens
- popups
- cancel
- manual corrections
- optional extra actions

After intervention, replay may continue from the next step.
