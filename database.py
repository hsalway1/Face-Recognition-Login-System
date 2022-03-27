import sqlite3 as sql
from datetime import date

class DATABASE():
    def __init__(self, name):
        self.connection = sql.connect(f'{name}.db')
        self.database = self.connection.cursor()

        self.database.execute('''CREATE TABLE IF NOT EXISTS USERS
        (
        User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First TEXT,
        Last TEXT,
        Email TEXT,
        Department TEXT,
        Profession TEXT,
        College TEXT,
        DOB TEXT,
        Password TEXT,
        Date TEXT
        )''')

    # inserting user details
    def insert(self, first, last, email, department, profession, college, DOB, password, date = date.today()):
        self.database.execute('''INSERT INTO USERS (First, Last, Email, Department, Profession, College, DOB, Password, Date) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        , (first, last, email, department, profession, college, DOB, password, date))
        self.connection.commit()

        self.database.execute('''SELECT * FROM USERS WHERE Email = ?''', (email,))

        self.account = self.database.fetchone()

    # validating user details
    def validate(self, email, password):  
        self.database.execute('''SELECT * FROM USERS WHERE Email = ?''', (email, ))
        self.account = self.database.fetchone()

        # if account does not exist or password does not match
        try:
            if len(self.account) == 0 or self.account[8] != password:
                return False

            else:
                return True
            
        except TypeError:
            return False

    def delete(self):
        self.database.execute('''DELETE FROM USERS WHERE User_ID = ?''', (self.account[0], ))
        self.connection.commit()

    # loading account details after validating
    def load(self):
        return self.account



