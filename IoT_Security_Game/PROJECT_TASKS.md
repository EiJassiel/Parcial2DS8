
Este documento adapta el plan del juego a la rúbrica entregada y reduce el alcance para un equipo de 4 integrantes en un proyecto de clase.

## Requisitos clave (rúbrica)
1. Usar Programación Orientada a Objetos y buenas prácticas.
2. Red formada por varios dispositivos conectados: sensores (movement, temp, energy, rfid, noise), cámaras y otros dispositivos básicos.
3. En cada turno se generan alertas (reales o falsas) en los dispositivos. Las alertas pueden incluir metadatos (timestamp, hora simulada, valor del sensor) para ayudar a identificar si son reales.
4. El jugador actúa como administrador TI y decide qué alertas atender.
5. Sistema de puntuación (rúbrica):
   - Puntos iniciales: 15
   - Alerta real atendida: +2
   - Alerta falsa atendida: -1
   - Alerta real NO atendida: -2
   - Alerta falsa NO atendida: 0
6. Condiciones de juego:
   - Duración: 5 rondas (turnos).
   - Victoria: terminar con >= 15 puntos.
   - Derrota: terminar con < 15 puntos.

## Objetivo del mini-proyecto
Entregar una versión funcional y simple del juego que cumpla exactamente la rúbrica: generación de alertas, toma de decisiones por parte del jugador, cálculo de puntaje y mensaje final de victoria/derrota.

## Reparto de trabajo (4 integrantes)
Se prioriza funcionalidad mínima y pruebas básicas.

### Integrante A — Lógica del juego (core)
- Implementar: `core/game.py`, `core/turn.py`, `core/score.py`.
- Responsabilidad: flujo de juego, control de rondas, integración del generador de alertas, aplicación de reglas de puntuación.
- Entregable mínimo: juego que ejecute 5 rondas y devuelva mensaje final.

### Integrante B — Entidades y sensores
- Implementar: `entities/device.py`, `entities/player.py`, `entities/sensors/*`.
- Responsabilidad: modelado de dispositivos, estructura de Alert (metadatos), funciones para simular lecturas.
- Entregable mínimo: un set de dispositivos con métodos que permitan generar alertas con metadatos.

### Integrante C — Generador de alertas y simulaciones
- Implementar: `alerts/alert.py`, `alerts/alert_generator.py`.
- Responsabilidad: generación por turno de alertas reales/falsas, parámetros (probabilidades, semilla para reproducibilidad).
- Entregable mínimo: función que devuelva lista de alertas por turno para todos los dispositivos.

### Integrante D — Interfaz y utilidades
- Implementar: `ui/hud.py`, `ui/input_handler.py`, `utils/time_utils.py`, `utils/random_utils.py`.
- Responsabilidad: entrada simple del usuario (texto o Pygame mínimo), mostrar puntaje/rondas, utilidades.
- Entregable mínimo: pantalla o texto por consola que permita seleccionar alertas a atender.

## Criterios de aceptación (mapeados a la rúbrica)
- Código orientado a objetos y modular.
- Juego ejecutable que simule 5 rondas y aplique las reglas de puntuación.
- Salida final con mensaje de victoria o derrota y puntuación final.
- Reproducibilidad: opción de pasar semilla para el generador de alertas (opcional pero recomendado).

## Checklist rápida
- [ ] `core/`: 5 rondas funcionando
- [ ] `alerts/`: generador por turno
- [ ] `entities/`: dispositivos y sensores básicos
- [ ] `ui/` o consola: seleccionar alertas a atender
- [ ] Documentación mínima (este archivo actualizado)

---