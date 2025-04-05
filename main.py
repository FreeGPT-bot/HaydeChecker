import os
import base64
import hashlib
import asyncio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from telethon import TelegramClient, functions

# Security Configuration
SECRET_SALT = "HaydeSecureSalt2023!@#"
ENCRYPTED_USERNAME = "TmFtZUNoZWNrZXJCeUhheWRl"
ENCRYPTED_PASSWORD = "Q2hlY2tlcjgzNzM5MTgzOTE3MzYyODE3MjZIYXlkZQ=="

class SecurityManager:
    @staticmethod
    def encrypt(data):
        salted = data + SECRET_SALT
        return base64.b64encode(salted.encode()).decode()
    
    @staticmethod
    def decrypt(encrypted):
        decoded = base64.b64decode(encrypted).decode()
        return decoded.replace(SECRET_SALT, "")
    
    @staticmethod
    def verify_credentials(username, password):
        try:
            decrypted_user = SecurityManager.decrypt(ENCRYPTED_USERNAME)
            decrypted_pass = SecurityManager.decrypt(ENCRYPTED_PASSWORD)
            return username == decrypted_user and password == decrypted_pass
        except:
            return False

class GradientButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = get_color_from_hex('#121212')
        self.font_size = dp(16)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#FFD700'))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            Color(rgba=get_color_from_hex('#121212'))
            RoundedRectangle(pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)), 
                           size=(self.size[0]-dp(4), self.size[1]-dp(4)), 
                           radius=[dp(13)])

class LoginScreen(BoxLayout):
    def __init__(self, success_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(15)
        self.padding = dp(50)
        self.success_callback = success_callback
        
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#121212'))
            Rectangle(pos=self.pos, size=self.size)
        
        self.title = Label(
            text='SECURE LOGIN', 
            font_size=dp(24),
            bold=True,
            color=get_color_from_hex('#FFD700'),
            size_hint=(1, 0.2)
        )
        
        self.username = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint=(1, 0.15),
            background_color=get_color_from_hex('#222222'),
            foreground_color=get_color_from_hex('#FFFFFF'),
            padding=dp(10)
        )
        
        self.password = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint=(1, 0.15),
            background_color=get_color_from_hex('#222222'),
            foreground_color=get_color_from_hex('#FFFFFF'),
            padding=dp(10)
        )
        
        self.login_btn = GradientButton(text='AUTHENTICATE')
        self.login_btn.bind(on_press=self.attempt_login)
        
        self.error_label = Label(
            text='',
            color=get_color_from_hex('#FF3333'),
            size_hint=(1, 0.1)
        )
        
        self.add_widget(self.title)
        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.login_btn)
        self.add_widget(self.error_label)
    
    def attempt_login(self, instance):
        if SecurityManager.verify_credentials(self.username.text, self.password.text):
            self.success_callback()
        else:
            self.error_label.text = "ACCESS DENIED"
            self.password.text = ""

class SessionManager:
    def __init__(self):
        self.sessions = []
        self.current_session_dir = ""
        self.phone_numbers = []
        self.current_numbers_file = ""
    
    def load_sessions_from_dir(self, path):
        self.current_session_dir = path
        self.sessions = []
        try:
            for file in os.listdir(path):
                if file.endswith('.session'):
                    self.sessions.append(os.path.join(path, file))
            return bool(self.sessions)
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return False
    
    def load_phone_numbers_from_file(self, filepath):
        self.current_numbers_file = filepath
        self.phone_numbers = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    phone = line.strip()
                    if phone:
                        self.phone_numbers.append(phone)
            return bool(self.phone_numbers)
        except Exception as e:
            print(f"Error loading phone numbers: {e}")
            return False
    
    async def check_session(self, session_path, api_id, api_hash):
        try:
            async with TelegramClient(session_path, api_id, api_hash) as client:
                me = await client.get_me()
                return True, f"{me.phone} (@{me.username})"
        except Exception as e:
            return False, str(e)
    
    async def check_phone_number(self, api_id, api_hash, phone_number):
        try:
            async with TelegramClient(':memory:', api_id, api_hash) as client:
                await client.send_code_request(phone_number)
                return True, "Account exists"
        except Exception as e:
            return False, str(e)

class MainAppScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(15)
        self.padding = dp(20)
        self.session_manager = SessionManager()
        self.api_id = 12345  # Замените на ваш API ID
        self.api_hash = 'your_api_hash'  # Замените на ваш API HASH
        
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#121212'))
            Rectangle(pos=self.pos, size=self.size)
            Color(rgba=get_color_from_hex('#FFD700aa'))
            RoundedRectangle(pos=(self.pos[0], self.pos[1]+self.height*0.7), 
                           size=(self.width, self.height*0.3), 
                           radius=[dp(30)])
        
        self.title_label = Label(
            text='HAYDE CHECKER', 
            font_size=dp(24),
            bold=True,
            color=get_color_from_hex('#FFD700'),
            size_hint=(1, 0.1)
        
        self.btn_load_sessions = GradientButton(text='LOAD SESSIONS')
        self.btn_load_numbers = GradientButton(text='LOAD PHONE NUMBERS')
        self.btn_check_sessions = GradientButton(text='CHECK SESSIONS')
        self.btn_check_numbers = GradientButton(text='CHECK PHONE NUMBERS')
        self.btn_logout = GradientButton(text='LOGOUT', background_color=get_color_from_hex('#FF3333'))
        
        self.btn_load_sessions.bind(on_press=self.show_session_loader)
        self.btn_load_numbers.bind(on_press=self.show_numbers_loader)
        self.btn_check_sessions.bind(on_press=self.check_sessions)
        self.btn_check_numbers.bind(on_press=self.check_phone_numbers)
        self.btn_logout.bind(on_press=self.logout)
        
        self.log_scroll = ScrollView(size_hint=(1, 0.6))
        self.log_label = Label(
            text='SYSTEM READY', 
            size_hint_y=None,
            height=dp(400),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            valign='top',
            text_size=(Window.width - dp(40), None),
            markup=True
        )
        self.log_scroll.add_widget(self.log_label)
        
        self.add_widget(self.title_label)
        self.add_widget(self.btn_load_sessions)
        self.add_widget(self.btn_load_numbers)
        self.add_widget(self.btn_check_sessions)
        self.add_widget(self.btn_check_numbers)
        self.add_widget(self.btn_logout)
        self.add_widget(self.log_scroll)
    
    def log_message(self, message):
        self.log_label.text += f"\n[color=#FFD700]{message}[/color]"
        self.log_scroll.scroll_to(self.log_label)
    
    def show_session_loader(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(
            path=os.getcwd(),
            dirselect=True,
            size_hint=(1, 0.8)
        )
        
        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))
        btn_cancel = GradientButton(text='CANCEL')
        btn_select = GradientButton(text='SELECT FOLDER')
        
        popup = Popup(
            title='Select Session Directory',
            content=content,
            size_hint=(0.9, 0.7),
            separator_color=get_color_from_hex('#FFD700')
        )
        
        def select_dir(btn):
            if file_chooser.selection:
                path = file_chooser.selection[0]
                if self.session_manager.load_sessions_from_dir(path):
                    self.log_message(f"Loaded {len(self.session_manager.sessions)} sessions from:\n{path}")
                else:
                    self.log_message("ERROR: No .session files found")
            popup.dismiss()
        
        btn_cancel.bind(on_press=popup.dismiss)
        btn_select.bind(on_press=select_dir)
        
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_select)
        content.add_widget(file_chooser)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def show_numbers_loader(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(
            path=os.getcwd(),
            filters=['*.txt'],
            size_hint=(1, 0.8)
        )
        
        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))
        btn_cancel = GradientButton(text='CANCEL')
        btn_select = GradientButton(text='SELECT FILE')
        
        popup = Popup(
            title='Select Phone Numbers File',
            content=content,
            size_hint=(0.9, 0.7),
            separator_color=get_color_from_hex('#FFD700')
        )
        
        def select_file(btn):
            if file_chooser.selection:
                filepath = file_chooser.selection[0]
                if self.session_manager.load_phone_numbers_from_file(filepath):
                    self.log_message(f"Loaded {len(self.session_manager.phone_numbers)} numbers from:\n{filepath}")
                else:
                    self.log_message("ERROR: No valid phone numbers found")
            popup.dismiss()
        
        btn_cancel.bind(on_press=popup.dismiss)
        btn_select.bind(on_press=select_file)
        
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_select)
        content.add_widget(file_chooser)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def check_sessions(self, instance):
        if not self.session_manager.sessions:
            self.log_message("ERROR: No sessions loaded")
            return
        
        self.log_message("\nCHECKING SESSIONS...")
        
        async def check_all():
            for session in self.session_manager.sessions:
                success, result = await self.session_manager.check_session(
                    session, self.api_id, self.api_hash
                )
                if success:
                    self.log_message(f"[color=#00FF00]VALID: {os.path.basename(session)} - {result}[/color]")
                else:
                    self.log_message(f"[color=#FF0000]INVALID: {os.path.basename(session)} - {result}[/color]")
        
        asyncio.create_task(check_all())
    
    def check_phone_numbers(self, instance):
        if not self.session_manager.phone_numbers:
            self.log_message("ERROR: No phone numbers loaded")
            return
        
        if not self.session_manager.sessions:
            self.log_message("ERROR: No sessions loaded")
            return
        
        self.log_message("\nCHECKING PHONE NUMBERS...")
        
        async def check_all_numbers():
            # Используем первую сессию для проверки
            session = self.session_manager.sessions[0]
            
            try:
                async with TelegramClient(session, self.api_id, self.api_hash) as client:
                    for phone in self.session_manager.phone_numbers:
                        try:
                            # Проверяем через поиск контакта
                            result = await client(functions.contacts.GetContactsRequest(
                                hash=0
                            ))
                            
                            user_exists = any(u.phone == phone for u in result.users)
                            if user_exists:
                                self.log_message(f"[color=#00FF00]EXISTS: {phone}[/color]")
                            else:
                                self.log_message(f"[color=#FFFF00]NOT FOUND: {phone}[/color]")
                        except Exception as e:
                            self.log_message(f"[color=#FF0000]ERROR: {phone} - {str(e)}[/color]")
            except Exception as e:
                self.log_message(f"[color=#FF0000]SESSION ERROR: {str(e)}[/color]")
        
        asyncio.create_task(check_all_numbers())
    
    def logout(self, instance):
        self.parent.show_login_screen()

class HaydeCheckerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#121212')
        self.main_screen = MainAppScreen()
        self.login_screen = LoginScreen(success_callback=self.show_main_screen)
        return self.login_screen
    
    def show_main_screen(self):
        self.root_window.remove_widget(self.login_screen)
        self.root_window.add_widget(self.main_screen)
    
    def show_login_screen(self):
        self.root_window.remove_widget(self.main_screen)
        self.root_window.add_widget(self.login_screen)

if __name__ == '__main__':
    HaydeCheckerApp().run()