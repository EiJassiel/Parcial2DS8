from alerts.alert import Alert
from collections import defaultdict
from datetime import datetime, timedelta


def generate_all_alerts(devices, sim_time: datetime = None, seed: int = None):
    """Solicita a cada dispositivo sus alertas y aplica correlación simple.

    Retorna lista de Alert.
    """
    sim_time = sim_time or datetime.utcnow()
    alerts = []
    for i, dev in enumerate(devices):
        # create a per-device, per-round seed to increase variability
        base_seed = 0 if seed is None else int(seed)
        time_part = int(sim_time.timestamp()) if sim_time is not None else 0
        # combine device id, time and base seed deterministically
        s = (hash(dev.device_id) ^ time_part ^ base_seed) & 0xFFFFFFFF
        dev_alerts = dev.generate_alerts(sim_time=sim_time, seed=s)
        alerts.extend(dev_alerts)

    # correlación simple por location: agrupar
    groups = defaultdict(list)
    for a in alerts:
        loc = a.location or "__unknown__"
        groups[loc].append(a)

    # aplicar heurística de correlación en cada grupo
    for loc, group in groups.items():
        sensor_types = set(a.sensor_type for a in group)
        n = len(sensor_types)
        add = min(0.7, 0.25 * n)
        weights = {"camera": 0.6, "motion": 0.5, "rfid": 0.7, "temp": 0.4, "energy": 0.5, "noise": 0.3}
        for a in group:
            w = weights.get(a.sensor_type, 0.3)
            a.confidence = min(1.0, a.confidence + add * w)
        if n >= 2:
            for a in group:
                a.is_real = True

    return alerts
