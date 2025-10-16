import os
import sys
import pygame
from ui.hud import HUD
from core.game import Game

# Paths y configuración de importación
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(os.path.join(ROOT_DIR, "entities"))
    sys.path.append(os.path.join(ROOT_DIR, "entities", "sensors"))

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HEADER_HEIGHT = 120
FPS = 30

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_DARK = (30, 30, 30)
GRAY_MEDIUM = (40, 40, 45)
GRAY_LIGHT = (50, 50, 50)
BLUE_BUTTON = (80, 160, 255)
BLUE_HOVER = (30, 100, 200)
GREEN_BUTTON = (40, 200, 40)
GREEN_HOVER = (30, 150, 30)
RED_BUTTON = (200, 80, 80)
RED_HOVER = (150, 50, 50)
RED_BUTTON = (200, 80, 80)
RED_HOVER = (150, 50, 50)

# Fuentes
def init_fonts():
    pygame.font.init()
    return {
        'title': pygame.font.SysFont(None, 24),
        'normal': pygame.font.SysFont(None, 20),
        'small': pygame.font.SysFont(None, 18),
    }

# Assets
def get_asset_path(filename):
    return os.path.join(ROOT_DIR, "assets", "images", filename)

# Configuración de dispositivos
DEVICE_LOCATIONS = {
    'motion': 'Entrada',
    'temp': 'Sala de Servidores',
    'energy': 'Recepción',
    'rfid': 'Oficina',
    'noise': 'Taller',
    'camera': 'Estacionamiento'
}

# Clase Botón
class Button:
    def __init__(self, text, x, y, width, height, color_normal, color_hover, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.action = action
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse) else self.color_normal
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_render = self.font.render(self.text, True, WHITE)
        text_rect = text_render.get_rect(center=self.rect.center)
        screen.blit(text_render, text_rect)

    def click(self):
        if self.action:
            self.action()

# Clase Display para manejo de pantalla y lógica de juego
class Display:
    def __init__(self, width, height, devices):
        pygame.init()
        self.width = width
        self.height = height
        self.header_height = HEADER_HEIGHT

        self.header_rect = pygame.Rect(0, 0, width, self.header_height)
        self.body_rect = pygame.Rect(0, self.header_height, width, height - self.header_height)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("IoT Security Game")
        self.running = True
        self.juego_iniciado = False

        self.devices = devices
        self.game = None

        # Cargar imágenes
        header_path = get_asset_path("header.gif")
        self.header_image = pygame.image.load(header_path).convert() if os.path.exists(header_path) else None
        if self.header_image:
            self.header_image = pygame.transform.scale(self.header_image, (self.header_rect.width, self.header_rect.height))

        bg_path = get_asset_path("background.png")
        self.background = pygame.image.load(bg_path).convert() if os.path.exists(bg_path) else pygame.Surface((self.body_rect.width, self.body_rect.height))
        if self.background:
            self.background = pygame.transform.scale(self.background, (self.body_rect.width, self.body_rect.height))
        else:
            self.background.fill(GRAY_LIGHT)

        # Inicializar fuentes
        fonts = init_fonts()
        self.font_title = fonts['title']
        self.font_normal = fonts['normal']
        self.font_small = fonts['small']
        self.botones = []
        
        # Imagen de inicio y fade
        start_path = get_asset_path("ClickToStar.png")
        self.start_image = pygame.image.load(start_path).convert() if os.path.exists(start_path) else None
        if self.start_image:
            # Escalar la imagen solo para el área debajo del header
            body_height = height - self.header_height
            self.start_image = pygame.transform.scale(self.start_image, (width, body_height))
        self.fade_alpha = 255
        self.fading = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.botones = []

            if self.juego_iniciado:
                self.draw_header()
                self.draw_body()
                self.draw_footer()
            else:
                self.draw_start_screen()
            
            if self.fading:
                fade_surface = pygame.Surface((self.width, self.height))
                fade_surface.fill(BLACK)
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()

            if self.fading:
                self.fade_alpha += 15
                if self.fade_alpha >= 255:
                    self.fading = False
                    self.fade_alpha = 255
                    self.juego_iniciado = True
                    if self.game is None:
                        self.game = Game(self.devices)
                        self.game.start()
                        self.alerts = self.game.get_current_alerts()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.juego_iniciado and not self.fading:
                        self.fading = True
                        self.fade_alpha = 0
                    elif self.juego_iniciado:
                        for boton in list(self.botones):
                            if boton.rect.collidepoint(event.pos):
                                boton.click()

            clock.tick(FPS)

        pygame.quit()

    def draw_start_screen(self):
        # Dibuja el header primero
        self.draw_header()
        
        if self.start_image:
            # Dibujar la imagen de inicio justo debajo del header
            self.screen.blit(self.start_image, (0, self.header_height))
        else:
            # Fondo por defecto para el área de contenido
            pygame.draw.rect(self.screen, GRAY_DARK, 
                           (0, self.header_height, self.width, self.height - self.header_height))
            txt = self.font_title.render("Haz clic para comenzar", True, WHITE)
            # Centrar el texto en el área debajo del header
            txt_rect = txt.get_rect(center=(self.width // 2, 
                                          self.header_height + (self.height - self.header_height) // 2))
            self.screen.blit(txt, txt_rect)

    def draw_header(self):
        if self.header_image:
            self.screen.blit(self.header_image, self.header_rect.topleft)
        else:
            pygame.draw.rect(self.screen, GRAY_DARK, self.header_rect)
            txt = self.font_title.render("IoT Security Game", True, WHITE)
            self.screen.blit(txt, (20, 20))

    def draw_body(self):
        self.screen.blit(self.background, (0, self.header_height))
        if not self.juego_iniciado or self.game is None:
            return

        alerts = self.game.get_current_alerts()
        cols = 3
        card_w = (self.body_rect.width - 40) // cols
        card_h = 140
        for idx, alert in enumerate(alerts):
            row = idx // cols
            col = idx % cols
            x = 20 + col * (card_w + 10)
            y = self.header_height + 20 + row * (card_h + 10)
            card_rect = pygame.Rect(x, y, card_w, card_h)
            pygame.draw.rect(self.screen, GRAY_MEDIUM, card_rect, border_radius=8)

            title = self.font_title.render(f"{alert.device_type.replace('_', ' ').title()}", True, WHITE)
            self.screen.blit(title, (x + 10, y + 8))

            desc = self.font_normal.render(f"{alert.params.get('desc', '')}", True, (200, 200, 200))
            self.screen.blit(desc, (x + 10, y + 32))

            params_to_show = {k: v for k, v in alert.params.items() if k != 'desc' and v is not None}
            if params_to_show:
                params_text = ", ".join(f"{k}: {v}" for k, v in params_to_show.items())
                params = self.font_small.render(params_text, True, (160, 160, 160))
                self.screen.blit(params, (x + 10, y + 52))

            chosen = None
            if alert.alert_id in self.game.decisions:
                chosen = self.game.decisions[alert.alert_id]

            attend_color = BLUE_BUTTON if chosen is not True else GREEN_BUTTON
            ignore_color = GRAY_LIGHT if chosen is not False else RED_BUTTON

            btn_att = Button("Atender", x + card_w - 200, y + card_h - 36, 90, 28, attend_color, BLUE_HOVER, lambda a=alert: self._record_decision(a.alert_id, True))
            btn_ign = Button("Ignorar", x + card_w - 100, y + card_h - 36, 90, 28, ignore_color, RED_HOVER, lambda a=alert: self._record_decision(a.alert_id, False))
            btn_att.draw(self.screen)
            btn_ign.draw(self.screen)
            self.botones.append(btn_att)
            self.botones.append(btn_ign)

        ctrl_y = self.header_height + self.body_rect.height - 60
        pygame.draw.rect(self.screen, GRAY_DARK, (self.body_rect.left + 10, ctrl_y - 8, self.body_rect.width - 20, 56), border_radius=8)

        score_txt = self.font_title.render(f"Puntuacion: {self.game.score}", True, WHITE)
        round_txt = self.font_title.render(f"Ronda: {self.game.current_round}/{self.game.rounds}", True, WHITE)
        self.screen.blit(score_txt, (self.body_rect.left + 20, ctrl_y + 4))
        self.screen.blit(round_txt, (self.body_rect.left + 180, ctrl_y + 4))

        next_btn = Button("Siguiente Ronda", self.body_rect.right - 300, ctrl_y + 8, 180, 36, GREEN_BUTTON, GREEN_HOVER, self._next_round)
        next_btn.draw(self.screen)
        self.botones.append(next_btn)

        exit_btn = Button("Salir", self.body_rect.right - 100, ctrl_y + 8, 80, 36, RED_BUTTON, RED_HOVER, lambda: setattr(self, 'running', False))
        exit_btn.draw(self.screen)
        self.botones.append(exit_btn)
        
        if self.game.is_over():
            res = self.game.result()
            big = pygame.font.SysFont(None, 48)
            HUD.draw_game_over(self.screen, self.width, self.height, f"{res['message']} - Puntuacion final: {res['score']}", big)
            restart = Button("Reiniciar", (self.width // 2) - 90, (self.height // 2) + 50, 180, 40, RED_BUTTON, RED_HOVER, self._restart_game)
            restart.draw(self.screen)
            self.botones.append(restart)

    def draw_footer(self):
        return

    def _record_decision(self, alert_id: str, attend: bool):
        if self.game is None:
            return
        self.game.record_decision(alert_id, attend)
        print(f"Decision registrada: {alert_id} -> {attend}")

    def _next_round(self):
        if self.game is None:
            return
        self.game.submit_round()
        if not self.game.is_over():
            self.alerts = self.game.get_current_alerts()

    def _restart_game(self):
        self.juego_iniciado = False
        self.game = None
        self.alerts = []
        print("Juego reiniciado")
