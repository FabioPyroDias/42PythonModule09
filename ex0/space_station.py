from pydantic import BaseModel, Field, ValidationError
import datetime
from typing import Optional


class SpaceStationModel(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime.datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    ship = SpaceStationModel(
        station_id="ISS001",
        name="Internation Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.datetime.now(),
        is_operational=True)
    print("Valid station created:")
    print(f"ID: {ship.station_id}")
    print(f"Name: {ship.name}")
    print(f"Crew: {ship.crew_size} people")
    print(f"Power: {ship.power_level}%")
    print(f"Oxygen: {ship.oxygen_level}%")
    if ship.is_operational:
        print("Status: Operational")
    else:
        print("Status: Non-Operational")
    print()
    print("========================================")
    print("Expected validation error:")
    try:
        SpaceStationModel(
            station_id="ID000",
            name="Wrong",
            crew_size=100,
            power_level=90,
            oxygen_level=90,
            last_maintenance=datetime.datetime.now(),
            is_operational=True)
    except ValidationError as error:
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
