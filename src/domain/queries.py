from dataclasses import dataclass
class Query:
    pass

# Requête pour récupérer les détails d'un patient
@dataclass(frozen=True)
class GetPatientDetails(Query):
    patient_id: str

# Requête pour rechercher des patients par nom de famille
@dataclass(frozen=True)
class SearchPatients(Query):
    family_name: str

# Requête pour récupérer tous les patients
@dataclass(frozen=True)
class GetAllPatients(Query):
    pass
