import streamlit as st
from receptiondb import receptionist

def main():
    st.title("Add New Receptionist")

    with st.form(key='add_receptionist_form', clear_on_submit=True):
        rec_id = st.text_input("Enter Receptionist ID")
        name = st.text_input("Enter Name")
        phone = st.text_input("Enter Phone Number")
        password = st.text_input("Enter Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button(label='Add Receptionist')

        if submit_button:
            if rec_id and name and phone and password and confirm_password:
                if password == confirm_password:
                    success, message = receptionist.add_receptionist(rec_id, name, phone, password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Passwords do not match.")
            else:
                st.warning("Please fill in all fields.")

if __name__ == "__main__":
    main()
