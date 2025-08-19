from Hospital import Hospital, Patient
import streamlit as st
from var import *
import pandas as pd
from receptiondb import receptionist

def main():
    st.title("Hospital Patient Record System")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Patient System", "Add Receptionist"])

    if page == "Patient System":
        hospital = Hospital()

        menu = ["Add Patient", "View Patients", "Search Patient", "Update Patient", "Delete Patient"]
        choice = st.sidebar.radio("Menu", menu)

        if choice == "Add Patient":
            st.subheader("Add New Patient")
            with st.form(key='add_patient_form', clear_on_submit=True):
                name = st.text_input("Enter Patient Name")
                age = st.number_input("Enter Patient Age", min_value=0, step=1, value=18)
                gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
                disease = st.text_input("Enter Patient Disease")
                email = st.text_input("Enter Patient Email")
                phone_number = st.text_input("Enter Patient Phone Number")
                address = st.text_area("Enter Patient Address")
                aadhar_id = st.number_input("Enter Aadhar Card ID",max_value=99999999999999)
                boarding_date = st.date_input("Select Boarding Date")
                room_number = st.text_input("Enter Room Number")
                bed_number = st.text_input("Enter Bed Number")
                submit_button = st.form_submit_button(label='Add Patient')

                if submit_button:
                    if name and disease and aadhar_id:
                        patient = Patient(name, age, gender, disease, email, phone_number, address, aadhar_id, boarding_date, room_number, bed_number)
                        success, message = hospital.add_patient(patient)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill in all required fields (Name, Disease, Aadhar ID).")


        elif choice == "View Patients":
            st.subheader("All Patients")
            patients_df = hospital.patients_df
            if not patients_df.empty:
                st.dataframe(patients_df)
            else:
                st.info("No patients in the records.")

        elif choice == "Search Patient":
            st.subheader("Search Patient")
            search_by = st.radio("Search by", ("ID", "Name"))
            if search_by == "ID":
                search_id = st.text_input("Enter Patient ID to search (e.g., HS-001)")
                if st.button("Search by ID"):
                    patient = hospital.search_patient_by_id(search_id)
                    if patient is not None:
                        st.dataframe(patient)
                    else:
                        st.warning(f"No patient found with ID: {search_id}")
            elif search_by == "Name":
                search_name = st.text_input("Enter Patient Name to search")
                if st.button("Search by Name"):
                    patients = hospital.search_patient_by_name(search_name)
                    if patients is not None:
                        st.dataframe(patients)
                    else:
                        st.warning(f"No patient found with name: {search_name}")

        elif choice == "Update Patient":
            st.subheader("Update Patient Details")
            update_id = st.text_input("Enter Patient ID to update (e.g., HS-001)")
            user_id = st.text_input("Enter your Receptionist ID", key="update_user_id")
            password = st.text_input("Enter your Password", type="password", key="update_password")
            if st.button("Get Patient Details"):
                try:
                    rec = receptionist(user_id, None) # Phone number is not needed for getting password
                    if password == rec.getpass():
                        patient_data = hospital.search_patient_by_id(update_id)
                        if patient_data is not None:
                            st.write("Current Patient Details:")
                            st.dataframe(patient_data)

                            with st.form(key='update_patient_form'):
                                st.write("Enter New Details (leave blank to keep current value):")
                                name = st.text_input("Name", value=patient_data.iloc[0]['Name'])
                                age = st.number_input("Age", min_value=0, step=1, value=patient_data.iloc[0]['Age'])
                                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient_data.iloc[0]['Gender']))
                                disease = st.text_input("Disease", value=patient_data.iloc[0]['Disease'])
                                email = st.text_input("Email", value=patient_data.iloc[0]['Email'])
                                phone_number = st.text_input("Phone Number", value=patient_data.iloc[0]['Phone Number'])
                                address = st.text_area("Address", value=patient_data.iloc[0]['Address'])
                                aadhar_id = st.text_input("Aadhar ID", value=patient_data.iloc[0]['Aadhar ID'])
                                boarding_date = st.date_input("Boarding Date", value=patient_data.iloc[0]['Boarding Date'])
                                room_number = st.text_input("Room Number", value=patient_data.iloc[0]['Room Number'])
                                bed_number = st.text_input("Bed Number", value=patient_data.iloc[0]['Bed Number'])
                                logging_off_time = st.time_input("Logging Off Time")

                                update_button = st.form_submit_button(label='Update Patient')

                                if update_button:
                                    updated_info = {
                                        'Name': name,
                                        'Age': age,
                                        'Gender': gender,
                                        'Disease': disease,
                                        'Email': email,
                                        'Phone Number': phone_number,
                                        'Address': address,
                                        'Aadhar ID': aadhar_id,
                                        'Boarding Date': boarding_date.strftime('%Y-%m-%d'),
                                        'Room Number': room_number,
                                        'Bed Number': bed_number,
                                        'Logging Off Time': logging_off_time.strftime('%H:%M:%S') if logging_off_time else None
                                    }
                                    if hospital.update_patient(update_id, updated_info):
                                        st.success(f"Patient with ID {update_id} updated successfully.")
                                    else:
                                        st.error("Failed to update patient.")
                        else:
                            st.warning(f"No patient found with ID: {update_id}")
                    else:
                        st.error("Incorrect password. You are not authorized to update patient records.")
                except ValueError as e:
                    st.error(e)


        elif choice == "Delete Patient":
            st.subheader("Delete Patient by ID")
            delete_id = st.text_input("Enter Patient ID to delete (e.g., HS-001)")
            user_id = st.text_input("Enter your Receptionist ID", key="delete_user_id")
            password = st.text_input("Enter your Password", type="password", key="delete_password")
            if st.button("Delete"):
                try:
                    rec = receptionist(user_id, None) # Phone number is not needed for getting password
                    if password == rec.getpass():
                        if hospital.delete_patient_by_id(delete_id):
                            st.success(f"Patient with ID {delete_id} deleted successfully.")
                        else:
                            st.warning(f"No patient found with ID: {delete_id}")
                    else:
                        st.error("Incorrect password. Patient not deleted.")
                except ValueError as e:
                    st.error(e)

    elif page == "Add Receptionist":
        import add_receptionist
        add_receptionist.main()
    
    # Remove the debugging prints from receptiondb.py
    with open("receptiondb.py", "r") as f:
        lines = f.readlines()
    with open("receptiondb.py", "w") as f:
        for line in lines:
            if not line.strip().startswith("print("):
                f.write(line)

if __name__ == "__main__":
    main()
