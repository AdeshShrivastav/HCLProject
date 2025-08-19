import pandas as pd
import os

DATA_FILE = 'patients.xlsx'
BACKUP_FILE = 'patients_backup.csv'

def initialize_database():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            'ID', 'Name', 'Age', 'Gender', 'Disease', 'Email', 'Phone Number',
            'Address', 'Aadhar ID', 'Boarding Date', 'Room Number', 'Bed Number', 'Logging Off Time'
        ])
        df.to_excel(DATA_FILE, index=False, engine='openpyxl')

def get_patient_data():
    initialize_database()
    if os.path.exists(BACKUP_FILE):
        backup_df = pd.read_csv(BACKUP_FILE)
        if not backup_df.empty:
            try:
                main_df = pd.read_excel(DATA_FILE, engine='openpyxl')
                combined_df = pd.concat([main_df, backup_df], ignore_index=True)
                combined_df.to_excel(DATA_FILE, index=False, engine='openpyxl')
                os.remove(BACKUP_FILE)
            except Exception as e:
                print(f"Could not merge backup file: {e}")
    return pd.read_excel(DATA_FILE, engine='openpyxl')

def save_patient_data(df):
    try:
        df.to_excel(DATA_FILE, index=False, engine='openpyxl')
    except PermissionError:
        print("Permission denied. Could not save to Excel. Saving to backup CSV.")
        df.to_csv(BACKUP_FILE, index=False)
        raise PermissionError(f"Could not save to {DATA_FILE}. It may be open in another program. "
                              f"Your data has been saved to a temporary file ({BACKUP_FILE}) and will be merged on next run.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        df.to_csv(BACKUP_FILE, index=False)
        raise




initialize_database()
