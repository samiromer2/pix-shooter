from __future__ import annotations

import pygame
from pathlib import Path


def draw_dim(surface: pygame.Surface, alpha: int = 160) -> None:
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, max(0, min(255, alpha))))
    surface.blit(overlay, (0, 0))


def draw_center_text(surface: pygame.Surface, lines: list[str]) -> None:
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 64)
        font_sub = ft.Font(None, 28)
    except Exception:
        font_title = None
        font_sub = None
    w, h = surface.get_size()

    y = h // 2 - 40
    if font_title is None or font_sub is None:
        # If no font, just draw separators so UI still works visually
        pygame.draw.rect(surface, (80, 80, 80), (w // 2 - 150, h // 2 - 70, 300, 4))
        pygame.draw.rect(surface, (80, 80, 80), (w // 2 - 150, h // 2 + 70, 300, 4))
        return
    if lines:
        title_surf, _ = font_title.render(lines[0], (255, 255, 255))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, y))
        y += 60
    for line in lines[1:]:
        sub_surf, _ = font_sub.render(line, (220, 220, 220))
        surface.blit(sub_surf, (w // 2 - sub_surf.get_width() // 2, y))
        y += 34


def _draw_button(surface: pygame.Surface, rect: pygame.Rect, text: str, hovered: bool) -> None:
    base = (60, 60, 60)
    hover = (90, 90, 90)
    border = (200, 200, 200)
    fill = hover if hovered else base
    pygame.draw.rect(surface, fill, rect, border_radius=6)
    pygame.draw.rect(surface, border, rect, width=2, border_radius=6)
    # Draw a simple icon instead of text to avoid font dependencies
    fg = (240, 240, 240)
    cx, cy = rect.centerx, rect.centery
    label = text.lower()
    if label.startswith("start") or label.startswith("resume"):
        # Play icon
        points = [(cx - 12, cy - 14), (cx - 12, cy + 14), (cx + 14, cy)]
        pygame.draw.polygon(surface, fg, points)
    elif label.startswith("quit to start") or label.startswith("quit"):
        # X icon
        pygame.draw.line(surface, fg, (cx - 12, cy - 12), (cx + 12, cy + 12), 3)
        pygame.draw.line(surface, fg, (cx + 12, cy - 12), (cx - 12, cy + 12), 3)
    else:
        pygame.draw.line(surface, fg, (rect.left + 10, cy), (rect.right - 10, cy), 2)


def draw_start_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> dict[str, pygame.Rect]:
    # Optional background image
    bg_path = Path("assets/sprites/menu_bg.png")
    if bg_path.exists():
        try:
            img = pygame.image.load(str(bg_path)).convert()
            img = pygame.transform.scale(img, surface.get_size())
            surface.blit(img, (0, 0))
        except Exception:
            draw_dim(surface, 140)
    else:
        draw_dim(surface, 140)
    draw_center_text(surface, [
        "Pix Shooter",
        "Press Enter to Start",
        "F to Shoot, Arrows/A/D to Move, Space to Jump, R to Reload",
        "Esc/P to Pause",
    ])
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    btn_w, btn_h = 200, 44
    start_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 80, btn_w, btn_h)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 80 + 56, btn_w, btn_h)
    buttons["start"] = start_rect
    buttons["quit"] = quit_rect
    mp = mouse_pos or (-1, -1)
    _draw_button(surface, start_rect, "Start", start_rect.collidepoint(mp))
    _draw_button(surface, quit_rect, "Quit", quit_rect.collidepoint(mp))
    return buttons


def draw_pause_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> dict[str, pygame.Rect]:
    draw_dim(surface, 180)
    draw_center_text(surface, [
        "Paused",
        "Press Esc/P to Resume",
        "Press Q to Quit to Start",
    ])
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    btn_w, btn_h = 220, 44
    resume_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 40, btn_w, btn_h)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 40 + 56, btn_w, btn_h)
    buttons["resume"] = resume_rect
    buttons["quit_to_start"] = quit_rect
    mp = mouse_pos or (-1, -1)
    _draw_button(surface, resume_rect, "Resume", resume_rect.collidepoint(mp))
    _draw_button(surface, quit_rect, "Quit to Start", quit_rect.collidepoint(mp))
    return buttons


def draw_animated_background(surface: pygame.Surface, tick_ms: int) -> None:
    # Simple animated diagonal lines background
    w, h = surface.get_size()
    # subtle gradient fill
    base = pygame.Color(25, 25, 30)
    surface.fill(base)

    # moving lines
    color = pygame.Color(40, 40, 60)
    spacing = 40
    offset = (tick_ms // 20) % spacing
    for x in range(-h, w + h, spacing):
        start = (x + offset, 0)
        end = (x - h + offset, h)
        pygame.draw.line(surface, color, start, end, 2)

