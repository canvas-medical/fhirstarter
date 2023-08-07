from typing import Dict, List
from dataclasses import dataclass
from datetime import date
class Event():
    """Event class for events"""
    event_type: str
    event_data: Dict[str, dict]

    
@dataclass
class PatientCreated(Event):
    family_name:str
    given_name:List[str]
    phone_number:str
    gender:str
    birthdate:date


@dataclass
class PatientDeleted(Event):
    pass


@dataclass
class PatientContactAdded(Event):
    pass

@dataclass
class PatientUpdated(Event):
    patient_id:str
    family_name:str
    given_name:List[str]
    phone_number:str
    gender:str
    birthdate:date
    
@dataclass
class PatientContactRemoved(Event):
    pass


@dataclass
class PatientNameChanged(Event):
    pass


@dataclass
class PatientActivated(Event):
    pass


@dataclass
class PatientDeactivated(Event):
    pass


@dataclass
class PatientGenderChanged(Event):
    pass


@dataclass
class PatientBirthdayChanged(Event):
    pass
