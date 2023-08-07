from abc import ABC, abstractmethod
import datetime
from typing import List
from src.domain.model import PatientModel
from src.domain.commands import CreatePatient


class AbstractRepository(ABC):

    @abstractmethod
    def save_patient(patient: PatientModel) -> str:
        pass

    @abstractmethod
    def get_patient_by_id(self, patient_id: str) -> PatientModel:
        pass
    
    @abstractmethod
    def get_patients(self) -> List[PatientModel]:
        pass

    @abstractmethod
    def full_patient_update(self, id: str, patient:CreatePatient) -> PatientModel:
        pass

    @abstractmethod
    def update_phone_number(self, id :str, newphone:str) -> PatientModel:
        pass

    @abstractmethod
    def update_patient_family_name(self, family_name: str) -> PatientModel:
        pass

    @abstractmethod
    def update_patient_active(self) -> PatientModel:
        pass

    def update_patient__birthdate(self, birth_date : datetime.date) -> PatientModel:
        pass

    @abstractmethod
    def delete_patient(self, patient_id: str) -> str:
        pass