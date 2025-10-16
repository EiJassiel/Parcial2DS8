import random
from datetime import datetime
from entities.device import Device
from alerts.alert import Alert


class Camera(Device):
    def __init__(self, device_id, location: str = None, params: dict = None):
        super().__init__(device_id, device_type="camera", location=location, params=params)

    def generate_alerts(self, sim_time: datetime = None, seed: int = None):
        rng = random.Random(seed)
        catalog = self.params.get('errors') or [
            {'desc': 'Persona detectada en área restringida', 'params': {'detected': True, 'type': 'person', 'zone': 'restricted'}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Objeto sospechoso detectado', 'params': {'detected': True, 'type': 'object'}, 'prob_real': 0.8, 'confidence': 0.7},
            {'desc': 'Múltiples personas detectadas', 'params': {'detected': True, 'count': rng.randint(2,5)}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Cámara parcialmente obstruida', 'params': {'obstruction': True}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Cambio brusco de iluminación', 'params': {'light_change': True}, 'prob_real': 0.3, 'confidence': 0.4},
            {'desc': 'Movimiento en horario restringido', 'params': {'detected': True, 'time': 'restricted'}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Imagen borrosa detectada', 'params': {'quality': 'low'}, 'prob_real': 0.4, 'confidence': 0.5},
        ]

        entry = rng.choice(catalog)
        if 'is_real' in entry:
            is_real = bool(entry['is_real'])
        else:
            is_real = rng.random() < float(entry.get('prob_real', 0.5))

        params = dict(entry.get('params', {}))
        params['desc'] = entry.get('desc', '')
        confidence = entry.get('confidence', 0.4)
        a = Alert.create(self.device_id, self.device_type, 'camera', params=params, location=self.location, is_real=is_real, confidence=confidence)
        return [a]