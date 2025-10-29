from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Tuple

import pygame

import settings as S


TILE_SIZE = 30  # chosen to evenly divide 960x540 (32x18 grid)


class Level:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.solid_rects: List[pygame.Rect] = []
        self._build_cache()

    @staticmethod
    def from_csv(path: str | Path) -> "Level":
        rows: List[List[int]] = []
        with open(path, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                rows.append([int(cell) for cell in row])
        return Level(rows)

    def _build_cache(self) -> None:
        self.solid_rects.clear()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.solid_rects.append(rect)

    def draw(self, surface: pygame.Surface) -> None:
        # Simple visual: dark gray tiles
        color = (30, 30, 30)
        for rect in self.solid_rects:
            pygame.draw.rect(surface, color, rect)


