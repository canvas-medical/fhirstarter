from src.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from src.adapters.mongoadapter import MongoDBAdapter
from src.adapters.redisadapter import RedisAdapter
from src.domain.model import PatientModel
from src.domain.commands import CreatePatient
from src.config import settings

class MongoRedisUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.mongo_repository = MongoDBAdapter(mongo_uri=settings.MONGO_URI)
        self.redis_repository = RedisAdapter(redis_host=settings.REDIS_HOST, redis_port=settings.REDIS_PORT)
        self.new_events = []
    def commit(self):
        # Sauvegarder les modifications dans MongoDB
        self.mongo_repository.commit()

        # Sauvegarder les événements (dans le cas de l'Event Sourcing) et les réinitialiser
        new_events = self.new_events
        self.new_events = []
        # Ici vous pouvez ajouter la logique pour sauvegarder les événements dans une base de données d'événements

    def rollback(self):
        # Annuler les modifications dans MongoDB
        self.mongo_repository.rollback()

    def collect_new_events(self):
        # Renvoie la liste des nouveaux événements collectés et les réinitialise
        new_events = self.new_events
        self.new_events = []
        return new_events

    def add_new_event(self, event):
        # Ajoute un nouvel événement à la liste des événements collectés
        self.new_events.append(event)

    def add_patient(self, patient: CreatePatient):
        # Opération d'écriture : Ajouter un patient à la base de données MongoDB
        patient_id = self.mongo_repository.save_patient(patient)
        return patient_id

    def update_patient(self, patient_id: str, patient: CreatePatient):
        # Opération d'écriture : Mettre à jour un patient dans la base de données MongoDB
        self.mongo_repository.update_patient(patient_id, patient)

    def delete_patient(self, patient_id: str):
        # Opération d'écriture : Supprimer un patient de la base de données MongoDB
        self.mongo_repository.delete_patient(patient_id)

    def get_patient(self, patient_id: str) -> PatientModel:
        # Opération de lecture : Chercher d'abord dans Redis
        patient_redis = self.redis_repository.get_patient(patient_id)
        if patient_redis:
            
            return patient_redis
        print("Patient non trouvé dans la sauvegrade de redis")
        # S'il n'est pas trouvé dans Redis, chercher dans MongoDB
        patient_mongo = self.mongo_repository.get_patient_by_id(patient_id)
        if patient_mongo:
            # Mettre à jour les données dans Redis pour les requêtes futures (facultatif)
            self.redis_repository.add_patient(patient_mongo)

        return patient_mongo

    def close(self):
        self.mongo_repository.close()
