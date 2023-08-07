from dataclasses import dataclass
from typing import List
from datetime import date

from pydantic import BaseModel

class Command:
    pass
# Commande pour créer un nouveau patient
@dataclass(frozen=True)
class CreatePatient(Command,BaseModel):
    family_name : str
    given_name : List[str]
    phone_number : str
    active : bool
    gender : str
    birthdate : date

# Commande pour mettre à jour les détails d'un patient
@dataclass(frozen=True)
class UpdatePatientDetails(Command):
    patient_id: str
    name: str
    age: int
    address: str

@dataclass(frozen=True)
class UpdateHumanNamePatient(Command):
    family_name : str
    given_name : List[str]

#Commande pour ajouter un contact à un patient
@dataclass(frozen=True)
class AddContact(Command):
    patient_id:str
    relationship_system: str
    relationship_code: str
    family: str
    given: List[str]
    telecom_system: str
    telecom_value: str
    phone_number:str

# Commande pour supprimer un patient
@dataclass(frozen=True)
class DeletePatient(Command):
    patient_id: str


