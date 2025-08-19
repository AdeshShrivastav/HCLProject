import os
import pandas as pd
class receptionist:
    _REC_FILE = "reception.xlsx"
    def __init__(self,id,phone):
        self.id = id
        self.phone = phone
        if not os.path.exists(receptionist._REC_FILE):
            df = pd.DataFrame(columns=[
                'ID', "Name", "Phone Number", "Password"
            ])
            df.to_excel(receptionist._REC_FILE, index=False, engine='openpyxl')


    def EncryptPassword(self,password):
        enc = ""
        for c in password:
            enc+= chr(ord(c)+3)

        return enc
    def Decrypt(self,password):
        dec = ""
        for c in password:
            dec += chr(ord(c)-3)
        return dec

    def setpass(self,newpass):
        df = pd.read_excel(receptionist._REC_FILE)
        for i in range(len(df["ID"])):
            if str(df["ID"][i]) == self.id:
                if str(df["Phone Number"][i]) == self.phone:
                    df.loc[i, "Password"] = self.EncryptPassword(newpass)
                    df.to_excel(receptionist._REC_FILE, index=False, engine='openpyxl')
                    return "Updated"
                raise ValueError("Invalid PhoneNumber")
        raise ValueError("Invalid ID")
    
    def getpass(self):
        df = pd.read_excel(receptionist._REC_FILE)
        for i in range(len(df["ID"])):
            if str(df["ID"][i]) == self.id:
                return self.Decrypt(str(df["Password"][i]))
        raise ValueError("Invalid ID")

    @staticmethod
    def add_receptionist(id, name, phone, password):
        df = pd.read_excel(receptionist._REC_FILE)
        if not df[df['ID'] == id].empty:
            return False, "A receptionist with this ID already exists."
        
        new_receptionist = {
            'ID': id,
            'Name': name,
            'Phone Number': phone,
            'Password': receptionist(id, phone).EncryptPassword(password)
        }
        df = pd.concat([df, pd.DataFrame([new_receptionist])], ignore_index=True)
        df.to_excel(receptionist._REC_FILE, index=False, engine='openpyxl')
        return True, "Receptionist added successfully."
