"""Hospital patient records and admission manager.

Admits patients into wards, processes discharges, calculates treatment
costs and exports the admission ledger.
"""

import hashlib
import json
import secrets

patient_records = {
    "P101": {"name": "John Doe", "ward": "ICU", "is_admitted": True, "bill": 2400.0},
    "P102": {"name": "Jane Smith", "ward": "General", "is_admitted": False, "bill": 450.0},
    "P103": {"name": "Robert Brown", "ward": "Private", "is_admitted": True, "bill": 1200.0},
}


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient into a ward.

    Returns False if the patient ID already exists, otherwise True.
    When an intake_log list is given, a log entry is appended to it.
    """
    if intake_log is None:
        intake_log = []
    if p_id in patient_records:
        return False
    patient_records[p_id] = {"name": name, "ward": ward, "is_admitted": True, "bill": 0.0}
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Mark a patient as discharged. Returns False for an unknown ID."""
    if p_id not in patient_records:
        return False
    patient_records[p_id]["is_admitted"] = False
    return True


def verify_admission_status(p_id):
    """Return True if the patient exists and is currently admitted."""
    record = patient_records.get(p_id)
    return record is not None and record["is_admitted"]


def calculate_treatment_cost(p_id, multiplier=1.12):
    """Return the patient's bill times multiplier, rounded to 2 decimals."""
    if isinstance(multiplier, bool) or not isinstance(multiplier, (int, float)):
        raise ValueError("multiplier must be a number")
    if multiplier < 0:
        raise ValueError("multiplier must not be negative")
    base_bill = patient_records[p_id]["bill"]
    return round(base_bill * multiplier, 2)


def generate_patient_hash(p_id):
    """Return the SHA-256 hex digest of a patient ID."""
    return hashlib.sha256(p_id.encode()).hexdigest()


def generate_ward_token():
    """Return a 4-digit ward token (1000-9999) from a secure source."""
    return 1000 + secrets.randbelow(9000)


def export_patient_ledger(filename="patient_records.txt"):
    """Write all patient records to filename as JSON."""
    with open(filename, "w", encoding="utf-8") as ledger:
        json.dump(patient_records, ledger, indent=2)
    print("Patient ledger exported to:", filename)


def get_ward_summary(records):
    """Return the number of currently admitted patients in records."""
    return sum(1 for details in records.values() if details["is_admitted"])


def main():
    """Run a short demonstration of the patient system."""
    intake_log = []
    admit_patient("P104", "Alice Walker", "General", intake_log)
    discharge_patient("P101")
    print("Intake log:", intake_log)
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103", 1.12))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))


if __name__ == "__main__":
    main()
