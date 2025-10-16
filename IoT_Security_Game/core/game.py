from datetime import datetime
from alerts.alert_generator import generate_all_alerts
from alerts.alert import Alert


class Game:
    """Controla el flujo del juego: rondas, puntaje y decisiones.

    API principal:
    - start(): inicializa y genera primera ronda
    - record_decision(alert_id, attend: bool)
    - submit_round(): aplica scoring, avanza la ronda
    - get_current_alerts(): devuelve lista de Alert de la ronda actual
    - is_over(): True si ya se completaron todas las rondas
    - result(): dict con score y message
    """

    def __init__(self, devices, rounds: int = 5, seed: int = None, initial_score: int = 15):
        self.devices = devices
        self.rounds = rounds
        self.seed = seed or 0
        self.initial_score = initial_score

        self.current_round = 0
        self.score = initial_score
        self.ended = False

        # alerts for current round
        self.current_alerts = []
        # decisions: alert_id -> bool (True = attend)
        self.decisions = {}

    def start(self):
        self.current_round = 1
        self.score = self.initial_score
        self.ended = False
        self._generate_round()

    def _generate_round(self):
        s = None if self.seed is None else (self.seed + self.current_round)
        now = datetime.utcnow()
        # Use the existing generator to get candidate alerts, then ensure exactly
        # one alert per device by selecting the highest-confidence alert per device
        candidates = generate_all_alerts(self.devices, sim_time=now, seed=s)

        by_device = {d.device_id: [] for d in self.devices}
        for a in candidates:
            if a.device_id in by_device:
                by_device[a.device_id].append(a)

        selected = []
        for d in self.devices:
            dev_id = d.device_id
            items = by_device.get(dev_id, [])
            if items:
                # pick alert with highest confidence
                items.sort(key=lambda x: x.confidence, reverse=True)
                selected.append(items[0])
            else:
                # create a default false alert so every device shows one alert
                selected.append(
                    Alert.create(dev_id, d.device_type, getattr(d, 'sensor_type', d.device_type), params={}, location=d.location, is_real=False, confidence=0.05)
                )

        # keep order matching self.devices
        self.current_alerts = selected
        self.decisions = {}

    def get_current_alerts(self):
        return list(self.current_alerts)

    def record_decision(self, alert_id: str, attend: bool):
        self.decisions[alert_id] = bool(attend)

    def submit_round(self):
        # Apply scoring rules
        for a in self.current_alerts:
            attend = self.decisions.get(a.alert_id, False)
            if a.is_real and attend:
                self.score += 2
            elif (not a.is_real) and attend:
                self.score -= 1
            elif a.is_real and (not attend):
                self.score -= 2
            # false and not attend -> 0

        # Advance or end
        if self.current_round >= self.rounds:
            self.ended = True
        else:
            self.current_round += 1
            self._generate_round()

    def is_over(self):
        return self.ended

    def result(self):
        msg = "Victoria" if self.score >= self.initial_score else "Derrota"
        return {"score": self.score, "message": msg}

