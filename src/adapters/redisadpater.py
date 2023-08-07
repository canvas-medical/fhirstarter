import redis
from src.domain.model import PatientModel
class RedisAdapter:
    def __init__(self, redis_host, redis_port):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def add_patient(self, patient:dict):
        # Ajouter un patient dans Redis en utilisant une clé basée sur l'ID du patient
        patient_id = "opentelemetricID"
        key = f"patient:{patient_id}"
        self.redis_client.hmset(key, patient)

    def get_patient(self, patient_id):
        # Récupérer un patient depuis Redis en utilisant son ID
        key = f"patient:{patient_id}"
        patient_data = self.redis_client.hgetall(key)
        if patient_data:
            
            return PatientModel(**patient_data)

        return None
