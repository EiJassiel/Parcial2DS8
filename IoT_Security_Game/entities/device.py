"""Clase base Device y contrato para sensores"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Device(ABC):
    def __init__(self, device_id: str, device_type: str, location: str = None, params: dict = None):
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
        self.params = params or {}

    def __repr__(self):
        return f"<{self.device_type} id={self.device_id} loc={self.location}>"

    @abstractmethod
    def generate_alerts(self, sim_time: datetime = None, seed: int = None) -> List[object]:
        """Genera 0..N alertas para este dispositivo en el turno sim_time.

        Retorna lista de Alert (u objetos compatibles con Alert.to_dict()).
        """
        raise NotImplementedError()
