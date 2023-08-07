from datetime import date
import datetime
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from src.domain.model import PatientModel
from src.domain.commands import  CreatePatient
from src.interfaces.abstractrepository import AbstractRepository
from src.config import settings

class MongoDBAdapter(AbstractRepository):
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database()

    def get_patient_collection(self) -> Collection:
        """Get patient collection"""
        return self.db.get_collection(settings.MONGO_COLLECTION)

    def save_patient(self, patient: dict) -> str:
        """Save patient."""
        #patient_dict = dict(patient)
        result = self.get_patient_collection().insert_one(patient)
        return str(result.inserted_id)
    
    def get_patient_by_id(self, patient_id: str) -> CreatePatient:
        """Get patient by id."""
        patient : PatientModel = self.get_patient_collection().find_one({"_id": ObjectId(patient_id)}, {"_id": 0})
        if not patient:
            raise HTTPException(status_code=400,detail="Patient not found")
        return patient
    
    def get_patients(self) -> List[PatientModel]:
        """Get patients."""
        patients = []
        for patient in self.get_patient_collection().find({}, {"_id": 0}) :
            patients.append(patient)
        return patients
    
    def update_patient(self, id:str,patient:CreatePatient):
        """Updates the patient."""
        data = dict(patient)
        self.get_patient_collection().find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": data},
        )   
        return self.get_patient_collection().find_one({"_id": ObjectId(id)}, {"_id": 0})
    
    def update_phone_number(self,id:str, newphone: str)->PatientModel:
        """Updates the patient's phone number."""
        patient = self.get_patient_by_id(id)
        patient["phone_number"] = newphone
        result = self.update_patient(id,patient)
        return result
    
    def update_patient__birthdate(self, birth_date: date) -> PatientModel:
        pass

    def update_patient_active(self) -> PatientModel:
        pass
    
    def update_patient_family_name(self, family_name: str) -> PatientModel:
        pass
    
    def full_patient_update(self, id: str, patient: CreatePatient) -> PatientModel:
        pass
    

    def delete_patient(self, patient_id: str) -> str:
        """ Delete the patient."""
        patient = self.get_patient_collection().find_one({"_id": ObjectId(patient_id)})
        if patient:
            self.get_patient_collection().delete_one({"_id": ObjectId(patient_id)})
            return "Patient Deleted"
        return "NOT FOUND"

    def close(self):
        self.client.close()
