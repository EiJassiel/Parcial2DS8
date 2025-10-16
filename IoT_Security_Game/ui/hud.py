# hud.py
from typing import Optional


class HUD:
    """Small HUD helper for drawing score, round and game-over overlay."""

    @staticmethod
    def draw_score_and_round(screen, footer_rect, score: int, current: int, total: int, font):
        score_txt = font.render(f"Puntuación: {score}", True, (255, 255, 255))
        round_txt = font.render(f"Ronda: {current}/{total}", True, (255, 255, 255))
        screen.blit(score_txt, (footer_rect.left + 10, footer_rect.top + 8))
        screen.blit(round_txt, (footer_rect.left + 160, footer_rect.top + 8))

    @staticmethod
    def draw_game_over(screen, width: int, height: int, message: str, font_large, font_small=None):
        overlay = screen.subsurface((0, 0, width, height)).copy()
        # semi-transparent dark overlay
        import pygame

        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        big = font_large
        txt = big.render(message, True, (255, 255, 255))
        r = txt.get_rect(center=(width // 2, height // 2))
        screen.blit(txt, r)

