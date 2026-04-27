import json
from datetime import datetime

FILE_PATH = "patients.json"


def load_data():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return {"patients": []}


def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_patient(name):
    data = load_data()
    for patient in data["patients"]:
        if patient["name"].lower() == name.lower():
            return patient
    return None


# def add_or_update_patient(name, symptoms, notes):  # Added notes also

#     data = load_data()
#     patient = get_patient(name)

#     new_entry = {
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "symptoms": symptoms,
#         "notes": ""
#     }

#     if patient:
#         patient["history"].append(new_entry)
#     else:
#         data["patients"].append({
#             "name": name,
#             "history": [new_entry]
#         })

#     save_data(data)

def add_or_update_patient(name, symptoms, notes):
    data = load_data()

    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "symptoms": symptoms.strip(),
        "notes": notes.strip()
    }

    # Check if patient exists
    for patient in data["patients"]:
        if patient["name"].lower() == name.lower():
            patient["history"].append(new_entry)
            save_data(data)
            return

    # New patient
    data["patients"].append({
        "name": name,
        "history": [new_entry]
    })

    save_data(data)


def get_patient_summary(name):
    patient = get_patient(name)
    if not patient:
        return "No previous history found."

    summary = ""
    for visit in patient["history"]:
        summary += f"Date: {visit['date']}, Symptoms: {visit['symptoms']}\n"

    return summary







def get_all_patients():
    data = load_data()
    return [p["name"] for p in data["patients"]]


def get_patient_full_history(name):
    patient = get_patient(name)
    if not patient:
        return []

    return patient["history"]