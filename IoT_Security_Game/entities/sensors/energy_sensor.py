# energy_sensor.py
import random
from datetime import datetime
from entities.device import Device
from alerts.alert import Alert


class EnergySensor(Device):
    def __init__(self, device_id, location: str = None, params: dict = None):
        super().__init__(device_id, device_type="energy_sensor", location=location, params=params)
    def generate_alerts(self, sim_time: datetime = None, seed: int = None):
        rng = random.Random(seed)
        catalog = self.params.get('errors') or [
            {'desc': 'Consumo en rango normal', 'params': {'power_w': 120.0}, 'prob_real': 0.1, 'confidence': 0.2},
            {'desc': 'Sobrecarga crítica', 'params': {'power_w': 850.0}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Pico de consumo alto', 'params': {'power_w': 450.0}, 'prob_real': 0.8, 'confidence': 0.7},
            {'desc': 'Consumo fuera de horario', 'params': {'power_w': 280.0, 'time': 'after_hours'}, 'prob_real': 0.9, 'confidence': 0.8},
            {'desc': 'Caída de energía detectada', 'params': {'power_w': 0.0}, 'prob_real': 0.95, 'confidence': 0.9},
            {'desc': 'Consumo anormalmente bajo', 'params': {'power_w': 30.0}, 'prob_real': 0.7, 'confidence': 0.6},
            {'desc': 'Fluctuación de energía', 'params': {'power_w': 200.0, 'variation': '±50W'}, 'prob_real': 0.8, 'confidence': 0.7},
        ]

        entry = rng.choice(catalog)
        if 'is_real' in entry:
            is_real = bool(entry['is_real'])
        else:
            is_real = rng.random() < float(entry.get('prob_real', 0.5))

        params = dict(entry.get('params', {}))
        params['desc'] = entry.get('desc', '')
        confidence = entry.get('confidence', 0.3)
        a = Alert.create(self.device_id, self.device_type, 'energy', params=params, location=self.location, is_real=is_real, confidence=confidence)
        return [a]
