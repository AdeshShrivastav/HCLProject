import pandas as pd
from database import get_patient_data, save_patient_data

class Patient:
    def __init__(self, name, age, gender, disease, email, phone_number, address, aadhar_id, boarding_date, room_number, bed_number, logging_off_time=None, patient_id=None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.disease = disease
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.aadhar_id = aadhar_id
        self.boarding_date = boarding_date
        self.room_number = room_number
        self.bed_number = bed_number
        self.logging_off_time = logging_off_time

    def to_dict(self):
        return {
            'ID': self.patient_id,
            'Name': self.name,
            'Age': self.age,
            'Gender': self.gender,
            'Disease': self.disease,
            'Email': self.email,
            'Phone Number': self.phone_number,
            'Address': self.address,
            'Aadhar ID': self.aadhar_id,
            'Boarding Date': self.boarding_date,
            'Room Number': self.room_number,
            'Bed Number': self.bed_number,
            'Logging Off Time': self.logging_off_time
        }

class Hospital:
    def __init__(self):
        self.patients_df = get_patient_data()

    def add_patient(self, patient):
        if not self.patients_df[self.patients_df['Aadhar ID'] == patient.aadhar_id].empty:
            return False, "A patient with this Aadhar ID already exists."

        if self.patients_df.empty or 'ID' not in self.patients_df.columns or self.patients_df['ID'].isnull().all():
            patient.patient_id = 'HS-001'
        else:
            last_id = self.patients_df['ID'].astype(str).str.extract(r'HS-(\d+)').astype(int).max().values[0]
            new_id = last_id + 1
            patient.patient_id = f'HS-{new_id:03d}'
        new_patient_df = pd.DataFrame([patient.to_dict()])
        self.patients_df = pd.concat([self.patients_df, new_patient_df], ignore_index=True)
        save_patient_data(self.patients_df)
        return True, f"Patient {patient.name} added successfully."

    def view_patients(self):
        print(self.patients_df)

    def search_patient_by_id(self, patient_id):
        patient = self.patients_df[self.patients_df['ID'] == patient_id]
        if not patient.empty:
            return patient
        else:
            return None

    def search_patient_by_name(self, name):
        patients = self.patients_df[self.patients_df['Name'].str.contains(name, case=False, na=False)]
        if not patients.empty:
            return patients
        else:
            return None

    def delete_patient_by_id(self, patient_id):
        initial_len = len(self.patients_df)
        self.patients_df = self.patients_df[self.patients_df['ID'] != patient_id]
        if len(self.patients_df) < initial_len:
            save_patient_data(self.patients_df)
            return True
        else:
            return False

    def update_patient(self, patient_id, updated_info):
        idx = self.patients_df.index[self.patients_df['ID'] == patient_id].tolist()
        if not idx:
            return False
        for key, value in updated_info.items():
            self.patients_df.loc[idx[0], key] = value
        save_patient_data(self.patients_df)
        return True
