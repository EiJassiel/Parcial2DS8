import random
from datetime import datetime
from entities.device import Device
from alerts.alert import Alert


class TempSensor(Device):
    def __init__(self, device_id, location: str = None, params: dict = None):
        super().__init__(device_id, device_type="temp_sensor", location=location, params=params)
    def generate_alerts(self, sim_time: datetime = None, seed: int = None):
        rng = random.Random(seed)
        catalog = self.params.get('errors') or [
            {'desc': 'Temperatura normal operativa', 'params': {'temperature_c': 22.0}, 'prob_real': 0.1, 'confidence': 0.2},
            {'desc': 'Temperatura crítica alta', 'params': {'temperature_c': 35.5}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Temperatura alta', 'params': {'temperature_c': 28.5}, 'prob_real': 0.8, 'confidence': 0.7},
            {'desc': 'Temperatura baja', 'params': {'temperature_c': 16.0}, 'prob_real': 0.7, 'confidence': 0.6},
            {'desc': 'Temperatura crítica baja', 'params': {'temperature_c': 5.0}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Fluctuación rápida temp', 'params': {'temperature_c': 25.0, 'rate': 5.0}, 'prob_real': 0.8, 'confidence': 0.7},
        ]

        entry = rng.choice(catalog)
        if 'is_real' in entry:
            is_real = bool(entry['is_real'])
        else:
            is_real = rng.random() < float(entry.get('prob_real', 0.5))

        params = dict(entry.get('params', {}))
        params['desc'] = entry.get('desc', '')
        confidence = entry.get('confidence', 0.3)
        a = Alert.create(self.device_id, self.device_type, 'temperature', params=params, location=self.location, is_real=is_real, confidence=confidence)
        return [a]
