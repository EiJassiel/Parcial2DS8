from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class Alert:
    alert_id: str
    device_id: str
    device_type: str
    sensor_type: str
    timestamp: datetime
    params: dict
    location: str = None
    is_real: bool = False
    confidence: float = 0.1
    metadata: dict = None

    def to_dict(self):
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else str(self.timestamp)
        return d

    def summary(self) -> str:
        """Return a short human readable one-line summary for UI cards."""
        # Prefer sensor-specific short labels
        if isinstance(self.params, dict):
            if 'power_w' in self.params:
                return f"Power {self.params['power_w']}W"
            if 'temperature_c' in self.params:
                return f"Temp {self.params['temperature_c']}C"
            if 'db' in self.params:
                return f"Noise {self.params['db']}dB"
            if 'tag_id' in self.params:
                return f"Tag {self.params['tag_id'] or 'unknown'}"
            if 'detected' in self.params:
                return "Object detected" if self.params['detected'] else "No detection"
            if 'motion' in self.params:
                return "Motion" if self.params.get('motion') else "No motion"
        return str(self.params)

    @staticmethod
    def create(device_id, device_type, sensor_type, params=None, location=None, is_real=False, confidence=0.1, metadata=None):
        return Alert(
            alert_id=str(uuid.uuid4()),
            device_id=device_id,
            device_type=device_type,
            sensor_type=sensor_type,
            timestamp=datetime.utcnow(),
            params=params or {},
            location=location,
            is_real=is_real,
            confidence=confidence,
            metadata=metadata or {}
        )
