import random
from datetime import datetime
from entities.device import Device
from alerts.alert import Alert


class MotionSensor(Device):
    def __init__(self, device_id, location: str = None, params: dict = None):
        super().__init__(device_id, device_type="motion_sensor", location=location, params=params)
    def generate_alerts(self, sim_time: datetime = None, seed: int = None):
        rng = random.Random(seed)
        catalog = self.params.get('errors') or [
            {'desc': 'Movimiento rápido detectado', 'params': {'motion': True, 'velocity': 'high'}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Movimiento lento detectado', 'params': {'motion': True, 'velocity': 'low'}, 'prob_real': 0.7, 'confidence': 0.6},
            {'desc': 'Múltiples objetos en movimiento', 'params': {'motion': True, 'objects': rng.randint(2,4)}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Movimiento en zona restringida', 'params': {'motion': True, 'zone': 'restricted'}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Movimiento leve detectado', 'params': {'motion': True, 'distance_m': 2.1}, 'prob_real': 0.5, 'confidence': 0.4},
            {'desc': 'Falsa alarma - reflejo', 'params': {'motion': False, 'cause': 'reflection'}, 'prob_real': 0.1, 'confidence': 0.2},
        ]

        entry = rng.choice(catalog)
        if 'is_real' in entry:
            is_real = bool(entry['is_real'])
        elif 'prob_real' in entry:
            is_real = rng.random() < float(entry['prob_real'])
        else:
            is_real = bool(entry.get('params', {}).get('motion', False))

        params = dict(entry.get('params', {}))
        params['desc'] = entry.get('desc', '')
        confidence = entry.get('confidence', 0.3)

        a = Alert.create(self.device_id, self.device_type, 'motion', params=params, location=self.location, is_real=is_real, confidence=confidence)
        return [a]
