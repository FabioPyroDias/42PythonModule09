from enum import Enum
from pydantic import BaseModel, ValidationError, Field, model_validator
from typing import Optional
import datetime


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime.datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1.0, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_fields(self):
        if self.contact_id[0:2] != "AC":
            raise ValueError("Contact ID must start "
                             "with \"AC\" (Alien Contact)")
        if self.contact_type == ContactType.PHYSICAL:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")
        elif self.contact_type == ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError("Telepathic contact requires "
                                 "at least 3 witnesses")
        if self.signal_strength > 7.0:
            if not self.message_received:
                raise ValueError("Strong signals (> 7.0) should include "
                                 "received messages")
        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")
    contact = AlienContact(contact_id="AC_2024_001",
                           timestamp=datetime.datetime.now(),
                           location="Area 51, Nevada",
                           contact_type=ContactType.RADIO,
                           signal_strength=8.5,
                           duration_minutes=45,
                           witness_count=5,
                           message_received="Greetings from Zeta Reticuli",
                           is_verified=True)
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witness: {contact.witness_count}")
    if contact.message_received:
        print(f"Message: '{contact.message_received}'")
    else:
        print("No message received")
    print()
    print("======================================")
    print("Expected validation error:")
    try:
        AlienContact(contact_id="AC_ERROR",
                     timestamp=datetime.datetime.now(),
                     location="Here",
                     contact_type=ContactType.TELEPATHIC,
                     signal_strength=2,
                     duration_minutes=5,
                     witness_count=2,
                     message_received="Ola",
                     is_verified=True)
    except ValidationError as error:
        print(error.errors()[0]["ctx"]["error"])
