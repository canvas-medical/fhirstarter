from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):
    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def collect_new_events(self):
        pass

    @abstractmethod
    def add_new_event(self, event):
        pass

    # Méthodes spécifiques pour les patients
    @abstractmethod
    def add_patient(self, patient):
        pass

    @abstractmethod
    def update_patient(self, patient_id: str, patient):
        pass

    @abstractmethod
    def delete_patient(self, patient_id: str):
        pass

    @abstractmethod
    def get_patient(self, patient_id: str):
        pass

    @abstractmethod
    def close(self):
        pass
