from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
import datetime


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime.datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_fields(self):
        if self.mission_id[0] != 'M':
            raise ValueError("Mission ID must start with \"M\"")
        commander_or_captain = False
        high_experience = 0
        for member in self.crew:
            if member.rank == Rank.CAPTAIN or member.rank == Rank.COMMANDER:
                commander_or_captain = True
            if not member.is_active:
                raise ValueError("All crew members must be active")
            if member.years_experience >= 5:
                high_experience += 1
        if not commander_or_captain:
            raise ValueError("Must have at least one Commander or Captain")
        if len(self.crew) / 2 > high_experience:
            raise ValueError("Long missions (> 365 days) need 50"
                             "% experienced crew (5+ years)")
        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")
    mission = SpaceMission(mission_id="M2024_MARS",
                           mission_name="Mars Colony Establishment",
                           destination="Mars",
                           launch_date=datetime.datetime.now(),
                           duration_days=900,
                           crew=[
                               CrewMember(member_id="MBR_00",
                                          name="Sarah Connor",
                                          rank=Rank.COMMANDER,
                                          age=42,
                                          specialization="Mission Command",
                                          years_experience=20,
                                          is_active=True),
                               CrewMember(member_id="MBR_01",
                                          name="John Smith",
                                          rank=Rank.LIEUTENANT,
                                          age=35,
                                          specialization="Navigation",
                                          years_experience=4,
                                          is_active=True),
                               CrewMember(member_id="MBR_02",
                                          name="Alice Johnson",
                                          rank=Rank.OFFICER,
                                          age=55,
                                          specialization="Engineering",
                                          years_experience=8,
                                          is_active=True)
                            ],
                           mission_status="planned",
                           budget_millions=2500.0)
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")
    print()
    print("=========================================")
    print("Expected validation error:")
    try:
        SpaceMission(mission_id="MWRONG",
                     mission_name="None",
                     destination="Nowhere",
                     launch_date=datetime.datetime.now(),
                     duration_days=10,
                     crew=[
                         CrewMember(member_id="MBR_00",
                                    name="Sarah Connor",
                                    rank=Rank.CADET,
                                    age=42,
                                    specialization="Mission Command",
                                    years_experience=20,
                                    is_active=True),
                         CrewMember(member_id="MBR_01",
                                    name="John Smith",
                                    rank=Rank.CADET,
                                    age=35,
                                    specialization="Navigation",
                                    years_experience=4,
                                    is_active=True),
                         CrewMember(member_id="MBR_02",
                                    name="Alice Johnson",
                                    rank=Rank.CADET,
                                    age=55,
                                    specialization="Engineering",
                                    years_experience=8,
                                    is_active=True)
                      ],
                     mission_status="planned",
                     budget_millions=2500.0)
    except ValidationError as error:
        print(error.errors()[0]["ctx"]["error"])
