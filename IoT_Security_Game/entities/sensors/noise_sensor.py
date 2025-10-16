import random
from datetime import datetime
from entities.device import Device
from alerts.alert import Alert


class NoiseSensor(Device):
    def __init__(self, device_id, location: str = None, params: dict = None):
        super().__init__(device_id, device_type="noise_sensor", location=location, params=params)
    def generate_alerts(self, sim_time: datetime = None, seed: int = None):
        rng = random.Random(seed)
        catalog = self.params.get('errors') or [
            {'desc': 'Nivel de ruido ambiental', 'params': {'db': 45}, 'prob_real': 0.1, 'confidence': 0.2},
            {'desc': 'Ruido crítico detectado', 'params': {'db': 95}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Ruido alto sostenido', 'params': {'db': 85, 'duration': '30s'}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Patrón de ruido sospechoso', 'params': {'db': 75, 'pattern': 'irregular'}, 'prob_real': 0.8, 'confidence': 0.7},
            {'desc': 'Pico breve de ruido', 'params': {'db': 70, 'duration': '2s'}, 'prob_real': 0.6, 'confidence': 0.5},
            {'desc': 'Ruido mecánico detectado', 'params': {'db': 65, 'type': 'mechanical'}, 'prob_real': 0.7, 'confidence': 0.6},
        ]

        entry = rng.choice(catalog)
        if 'is_real' in entry:
            is_real = bool(entry['is_real'])
        else:
            is_real = rng.random() < float(entry.get('prob_real', 0.5))

        params = dict(entry.get('params', {}))
        params['desc'] = entry.get('desc', '')
        confidence = entry.get('confidence', 0.3)
        a = Alert.create(self.device_id, self.device_type, 'noise', params=params, location=self.location, is_real=is_real, confidence=confidence)
        return [a]
        
