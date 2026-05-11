"""Screenshot helper.

Saves the current pygame display to ``assets/screenshots/`` with a timestamped
filename. Bound to F12 in ``main.py`` so it works in every game state.
"""

from __future__ import annotations

import os
from datetime import datetime

import pygame


SCREENSHOT_DIR = os.path.join("assets", "screenshots")


def save_screenshot(surface: pygame.Surface, state: str = "") -> str | None:
    """Write ``surface`` to disk as a PNG. Returns the path, or None on failure.

    The filename embeds the current game ``state`` (e.g. "playing", "shop") so
    bulk captures are easy to triage afterwards.
    """
    try:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        suffix = f"-{state}" if state else ""
        path = os.path.join(SCREENSHOT_DIR, f"screenshot-{stamp}{suffix}.png")
        pygame.image.save(surface, path)
        return path
    except (pygame.error, OSError) as exc:
        # Surfacing to stdout is intentional: screenshots are a dev/showcase
        # tool, not a gameplay-critical path, so failures shouldn't crash.
        print(f"[screenshot] failed to save: {exc}")
        return None
