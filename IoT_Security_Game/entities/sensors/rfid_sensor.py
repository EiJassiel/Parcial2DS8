# rfid_sensor.py
# Subclase para sensor RFID
# Implementación pendiente
# rfid_sensor.py
import random
from datetime import datetime
from entities.device import Device
from alerts.alert import Alert


class RFIDSensor(Device):
    def __init__(self, device_id, location: str = None, params: dict = None):
        super().__init__(device_id, device_type="rfid_sensor", location=location, params=params)
    def generate_alerts(self, sim_time: datetime = None, seed: int = None):
        rng = random.Random(seed)
        catalog = self.params.get('errors') or [
            {'desc': 'Tag autorizado detectado', 'params': {'tag_id': f"TAG-{rng.randint(1000,9999)}"}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Tag no autorizado', 'params': {'tag_id': f"UNK-{rng.randint(1000,9999)}"}, 'prob_real': 0.9, 'confidence': 0.9},
            {'desc': 'Lectura fallida de tag', 'params': {'tag_id': None}, 'prob_real': 0.1, 'confidence': 0.2},
            {'desc': 'Múltiples tags detectados', 'params': {'tag_count': rng.randint(2,5)}, 'prob_real': 0.7, 'confidence': 0.6},
            {'desc': 'Tag expirado detectado', 'params': {'tag_id': f"EXP-{rng.randint(1000,9999)}"}, 'prob_real': 0.8, 'confidence': 0.7},
        ]

        entry = rng.choice(catalog)
        if 'is_real' in entry:
            is_real = bool(entry['is_real'])
        else:
            is_real = rng.random() < float(entry.get('prob_real', 0.5))

        params = dict(entry.get('params', {}))
        params['desc'] = entry.get('desc', '')
        confidence = entry.get('confidence', 0.3)
        a = Alert.create(self.device_id, self.device_type, 'rfid', params=params, location=self.location, is_real=is_real, confidence=confidence)
        return [a]
