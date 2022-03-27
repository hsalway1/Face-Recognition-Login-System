from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from database import DATABASE
from custom_camera import CameraCv
import os
import face_recognition
from datetime import date

class LoginPage(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        print(self.email.text, self.password.text)
        
        if db.validate(email = self.email.text, password = self.password.text):
            sm.current = 'face_authentication'
            self.reset()

        else:
            invalid()
    

    def reset(self):
        self.email.text = ''
        self.password.text = ''


class RegistrationPage(Screen):
    first = ObjectProperty(None)
    last = ObjectProperty(None)
    email = ObjectProperty(None)
    department = ObjectProperty(None)
    college = ObjectProperty(None)
    student = ObjectProperty(None)
    teacher = ObjectProperty(None)
    dob = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm = ObjectProperty(None)

    profession = 'Teacher'

    def register_btn(self):

        a = [self.first.text, self.last.text, self.email.text, self.college.text, self.department.text, self.dob.text, 
            self.password.text, self.confirm.text]

        if '' in a:
            invalidForm()

        else:
            if self.password.text != self.confirm.text:
                invalid()

            else:
                db.insert(first = self.first.text, last = self.last.text, email = self.email.text, department = self.department.text, 
                profession = self.profession, college = self.college.text, DOB = self.dob.text, password = self.password.text)
                self.reset()
                sm.current = 'face_registration'

    def stuStat(self):
        if self.student.active:
            self.teacher.active = False
            self.profession = 'Student'

        else:
            self.teacher.active = True
            self.profession = 'Teacher'

    def teaStat(self):
        if self.teacher.active:
            self.student.active = False
            self.profession = 'Teacher'

        else:
            self.student.active = True
            self.profession = 'Student'
            
    def login(self):
        self.reset()
        sm.current = 'LoginPage'

    def reset(self):
        self.first.text = ''
        self.last.text = ''
        self.email.text = ''
        self.password.text = ''
        self.college.text = ''
        self.department.text = ''
        self.dob.text = ''
        self.confirm.text = ''

class face_authentication(Screen):
    n = ObjectProperty(None)
    cam = ObjectProperty(None)

    def on_enter(self, *args):
        self.Id, self.first, self.last = db.account[0:3]

        self.current_dir = os.getcwd()

        self.n.text = f'{self.first} please verify your face'

        self.cam.play = True

        os.chdir('Faces\\{} - {} {}'.format(self.Id, self.first, self.last))

    def on_leave(self):
        self.cam.play = False
        os.chdir(self.current_dir)

    def proceed(self):
        image = face_recognition.load_image_file('photo.png')

        face_encoding1 = face_recognition.face_encodings(image)[0]

        self.cam.export_to_png('test.png')

        test_image = face_recognition.load_image_file('test.png')

        try:
            face_encoding2 = face_recognition.face_encodings(test_image)[0]
            results = face_recognition.compare_faces([face_encoding1], face_encoding2)

            if results[0] == True:
                os.remove('test.png')
                sm.current = 'Grant'
        
            else:
                invalidFace('Your face does not match')

        # if no face detected
        except IndexError:  
            invalidFace('Please place your face properly infront of the camera', font_size = '20sp')

class face_registration(Screen):
    cam = ObjectProperty(None)
    n1 = ObjectProperty(None)
    n2 = ObjectProperty(None)
    cam_button : ObjectProperty(None)

    def on_enter(self):
        self.cam.play = True
        self.Id, self.first, self.last = db.account[0:3]
        self.n1.text = f'Welcome {self.first}'
        self.count = 1

        self.cam.play = True

        self.current_dir = os.getcwd()
        self.path = os.path.join(self.current_dir, 'Faces', '{} - {} {}'.format(self.Id, self.first, self.last))

        print(self.path)

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        os.chdir(self.path)

    def on_leave(self):
        self.cam.play = False

    def registerFace(self):

        if self.count == 1:
            self.cam.export_to_png('photo.png', dimension = (1280, 720))
            self.n2.text = f'Set a profile picture'

        elif self.count == 2:
            self.cam.export_to_png('Profile.png', dimension = (1280, 720))
            self.n2.text = 'Done! Please click the register button'
            self.cam_button.disabled = True
        
        self.count += 1
  
    def register(self):
        if self.count < 2:
            invalidPhoto()

        else:
            sm.current = 'LoginPage'
            

        os.chdir(self.current_dir)

    def cancel(self):
        os.chdir(self.current_dir)

        for image in os.listdir(f'Faces\\{self.Id} - {self.first} {self.last}'):
            os.remove(f'{self.path}\\{image}')

        os.rmdir(self.path)

        db.delete()
        sm.current = 'LoginPage'

class Granted(Screen):
    full_name = ObjectProperty(None)
    emailid = ObjectProperty(None)
    department = ObjectProperty(None)
    dob = ObjectProperty(None)
    date = ObjectProperty(None)
    img = ObjectProperty(None)

    def logout(self):
        sm.current = 'LoginPage'

    def on_enter(self, *args):  # pre defined function. Runs when we enter the granted screen
        Id, first, last, email, department, profession, college, DOB, password, date = db.account
        self.img.source = f'Faces\\{Id} - {first} {last}\\profile.png'

        self.full_name.text = first + ' ' + last
        self.emailid.text = email
        self.department.text = department
        self.college.text = college
        self.profession.text = profession
        self.dob.text = DOB
        self.date.text = date

    def delete(self):
        popup = del_account()
        popup.open()

class del_account(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Delete account'
        self.size_hint = (0.3, 0.4)

    def yes(self):
        Id, first, last = db.account[:3]
        for image in os.listdir(f'Faces\\{Id} - {first} {last}'):
            os.remove(f'Faces\\{Id} - {first} {last}\\{image}')

        os.rmdir(f'Faces\\{Id} - {first} {last}')

        db.delete()

        self.dismiss()
        sm.current = 'LoginPage'

    def no(self):
        pass

def invalid():
    pop_window = Popup(title = 'Access Denied', content = Label(text = 'Check email or password', font_size = '30sp'), 
    size = (400, 400), size_hint = (0.5, 0.5))

    pop_window.open()

def invalidForm():
    pop_window = Popup(title = 'Invalid Form', content = Label(text = 'Fill all the details', font_size = '30sp'), 
    size = (400, 400), size_hint = (0.5, 0.5))
    
    pop_window.open()

def invalidPhoto():
    pop_window = Popup(title = 'Insufficient number of photos', content = Label(text = 'You need atleast 15 photos', font_size = '30sp'), 
    size = (400, 400), size_hint = (0.5, 0.5))

    pop_window.open()

def invalidFace(text, font_size = '30sp'):
    pop_window = Popup(title = 'Access denied', content = Label(text = text, font_size = font_size), 
    size = (400, 400), size_hint = (0.5, 0.5))

    pop_window.open()

db = DATABASE('user_database')

Builder.load_file("gui.kv")

screens = [LoginPage(name = 'LoginPage'), RegistrationPage(name = 'RegistrationPage'), face_authentication(name = 'face_authentication') 
            ,face_registration(name = 'face_registration'), Granted(name = 'Grant')]

sm = ScreenManager()

for screen in screens:
    sm.add_widget(screen)

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyMainApp().run()
    db.connection.close()
    print("database connection closed")

