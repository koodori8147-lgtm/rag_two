from dataclasses import dataclass
from statistics import mean


@dataclass
class SensorReading:
    machine_id: str
    temperature: float
    vibration: float
    pressure: float


class MachineMonitor:
    def __init__(self, temp_limit=75.0, vibration_limit=5.0):
        self.temp_limit = temp_limit
        self.vibration_limit = vibration_limit
        self.history = []

    def add_reading(self, reading: SensorReading):
        self.history.append(reading)

    def check_status(self, reading: SensorReading):
        if (
            reading.temperature >= self.temp_limit
            and reading.vibration >= self.vibration_limit
        ):
            return "critical"
        if reading.temperature >= self.temp_limit:
            return "temperature_warning"
        if reading.vibration >= self.vibration_limit:
            return "vibration_warning"
        return "normal"

    def average_temperature(self):
        if not self.history:
            return None
        return mean(item.temperature for item in self.history)


def parse_sensor_row(row: dict) -> SensorReading:
    return SensorReading(
        machine_id=row["machine_id"],
        temperature=float(row["temperature"]),
        vibration=float(row["vibration"]),
        pressure=float(row["pressure"]),
    )


def create_alert_message(reading: SensorReading, status: str) -> str:
    return (
        f"machine={reading.machine_id}, "
        f"temperature={reading.temperature}, "
        f"vibration={reading.vibration}, "
        f"status={status}"
    )


def run_demo():
    raw_rows = [
        {"machine_id": "A-01", "temperature": 54.2, "vibration": 2.1, "pressure": 1.01},
        {"machine_id": "A-02", "temperature": 79.4, "vibration": 3.0, "pressure": 1.03},
        {"machine_id": "A-03", "temperature": 82.1, "vibration": 6.4, "pressure": 1.04},
    ]

    monitor = MachineMonitor()

    for row in raw_rows:
        reading = parse_sensor_row(row)
        monitor.add_reading(reading)
        status = monitor.check_status(reading)
        print(create_alert_message(reading, status))

    print("average_temperature:", monitor.average_temperature())


if __name__ == "__main__":
    run_demo()
