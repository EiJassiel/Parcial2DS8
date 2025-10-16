from settings import (
    Display, SCREEN_WIDTH, SCREEN_HEIGHT, DEVICE_LOCATIONS
)
from entities.sensors import (
    MotionSensor, TempSensor, EnergySensor,
    RFIDSensor, NoiseSensor, Camera
)

def create_game_devices():
    """Crea y retorna la lista de dispositivos IoT para el juego."""
    return [
        MotionSensor("motion-1", location=DEVICE_LOCATIONS['motion']),
        TempSensor("temp-1", location=DEVICE_LOCATIONS['temp']),
        EnergySensor("energy-1", location=DEVICE_LOCATIONS['energy']),
        RFIDSensor("rfid-1", location=DEVICE_LOCATIONS['rfid']),
        NoiseSensor("noise-1", location=DEVICE_LOCATIONS['noise']),
        Camera("cam-1", location=DEVICE_LOCATIONS['camera']),
    ]

def main():
    """Función principal que inicia el juego."""
    devices = create_game_devices()
    display = Display(SCREEN_WIDTH, SCREEN_HEIGHT, devices)
    display.run()

if __name__ == "__main__":
    main()
