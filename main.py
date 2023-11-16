from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.spinner import Spinner
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput  
from kivy.uix.button import Button  
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase 
from kivy.config import Config
import re
import gspread
import time
import pyrebase
import json
from PIL import Image as PILImage
from PIL import ImageEnhance

from kivy.core.window import Window

Window.clearcolor = get_color_from_hex('#010e1f')

LabelBase.register(name='LemonMilk', fn_regular='LEMONMILK.otf')

with open('config.json') as config_file:
    config = json.load(config_file)

firebase_config = config['firebaseConfig']
firebase_config2 = config['firebaseConfig2']

google_credentials_file = config['googleCredentialsFile']

spreadsheet_id = config['spreadsheetId']
spreadsheet_id2 = config['spreadsheetId2']
spreadsheet_id3 = config['spreadsheetId3']
spreadsheet_id4 = config['spreadsheetId4']
worksheet_name = config['worksheetName']
worksheet_name2 = config['worksheetName2']
worksheet_name3 = config['worksheetName3']

json_key_file = config['jsonKeyFile']

apiKey = firebase_config['apiKey']
authDomain = firebase_config['authDomain']
databaseURL = firebase_config['databaseURL']
projectId = firebase_config['projectId']
storageBucket = firebase_config['storageBucket']
messagingSenderId = firebase_config['messagingSenderId']
appId = firebase_config['appId']

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

apiKey2 = firebase_config2['apiKey']
authDomain2 = firebase_config2['authDomain']
databaseURL2 = firebase_config2['databaseURL']
projectId2 = firebase_config2['projectId']
storageBucket2 = firebase_config2['storageBucket']
messagingSenderId2 = firebase_config2['messagingSenderId']
appId2 = firebase_config2['appId']

firebase2 = pyrebase.initialize_app(firebase_config2)
auth2 = firebase2.auth()

titulos = [
    "PGR - PROGRAMA DE \nGERENCIAMENTO DE RISCO",
    "PGR - PROGRAMA DE \nGERENCIAMENTO DE RISCO",
    "PGR - PROGRAMA DE \nGERENCIAMENTO DE RISCO",
    "PGR - PROGRAMA DE \nGERENCIAMENTO DE RISCO",
    "PGR - PROGRAMA DE \nGERENCIAMENTO DE RISCO",
    "CONTROLE DE SAÚDE\nOCUPACIONAL",
    "CONTROLE DE SAÚDE\nOCUPACIONAL",
    "CONTROLE DE SAÚDE\nOCUPACIONAL",
    "CONTROLE DE SAÚDE\nOCUPACIONAL",
    "CONTROLE DE\nCOLABORADORES",
]    
perguntas = [
    "1 - O PGR foi elaborado e\nimplementado na obra?",
    "2 - O PGR foi elaborado por um\n profissional legalmente habilitado?",
    "3 - Possui projeto de área de vivência?",
    "4 - Possui projeto elétrico de instalações\n temporárias,sistemas de proteção \ncoletiva e projeto de SPIQ?",
    "5 -  Possui relação de EPI's\n e especificações técnicas?",
    "6 -  A obra possui PCMSO \n(Programa de gereciamento de risco)?",
    "7 -  Os ASO'S estão em dias?",
    "8 -  As Vacinas dos colaboradores\n está em dias?",
    "9 -  A planilha de vacinas está atualizada?",
    "10 -  A planilha de controle de\ncolaboradores internos e\n externos está atualizada?",
]
perguntas2 = [
    "1 - Atendimento geral da construtora\n na fase de negociação da obra.",
    "2 - Adaptação da empresa às rotinas\n administrativas da Empresa.",
    "3 - Facilidade de troca de informação\n com a TOP Construtora.",
    "4 - O(s) Engenheiro(s) da obra foi (foram)\n solicito(s) e cordial(is) no\n  atendimento da sua equipe?",
    "5 -  Os colaboradores foram solícitos e\n cordiais no atendimento da sua equipe?",
    "6 -  Empenho do(s) Engenheiro(s) da obra\n  na solução dos problemas.",
    "7 -  A organização física da obra.",
    "8 -  Organização da área financeira \ne entrega das notas fiscais.",
    "9 -  Cumprimento do cronogrma\n físico acordado.",
    "10 -  Limpeza da Obra.",
    "11 - Interferências da obra na operação do\n empreendimento. (Quando aplicável)",
    "12 - Atendimento às normas de\n segurança do trabalho.",
]
perguntas3 = [
    "1 - Agilidade na execução do reparo.",
    "2 - Atendimento da equipe construtora.",
    "3 - Facilidade de troca de informação\n com a TOP Construtora.",
    "4 - O engenheiro da assistência técnica\n é solicito e cordial no atendimento\n da sua equipe?",
    "5 - Os colaboradores são solícitos\n e cordiais no atendimento?",
    "6 - Empenho do Engenheiro na\n solução dos problemas.",
    "7 - Interferências da obra na operação\n do empreendimento. (Quando aplicável)",
    "8 - Qual o nível de satisfação\n na realização do reparo?",
    "9 - Atendimento às normas de\n segurança do trabalho."
]

class DarkenedImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 0.5)  # Cor preta com um alpha (transparência) de 0,5
            Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.5)  # Cor preta com um alpha (transparência) de 0,5
            Rectangle(pos=self.pos, size=self.size)

class inicialPage(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
            
        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82} 

        button = Image(source='images/button.png', size_hint=(0.273, 0.143), size=(200, 200))
        button.pos_hint = {'center_x': 0.3, 'center_y': 0.6}   

        lupa = Image(source='images/lupa.png', size_hint=(0.325, 0.195), size=(200, 200))
        lupa.pos_hint = {'center_x': 0.3, 'center_y': 0.4}

        comercial = Image(source='images/comercial.png', size_hint=(0.325, 0.195), size=(200, 200))
        comercial.pos_hint = {'center_x': 0.3, 'center_y': 0.2}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.inicial_button =Button(
            text='[b]SST[/b]',
            size_hint=(0.6, None),
            font_name='LemonMilk',
            font_size=50,
            size=(800, 60),
            pos_hint={'center_x': 0.53, 'center_y': 0.6},
            color=get_color_from_hex('#baa673'),
            halign='center',
            background_color=(0, 0, 0, 0),
            markup=True
        )
        self.inicial_button.bind(on_release=self.go_to_login_page)

        fundobotao = Image(source='images/fundo_botao.png', size_hint=(1.2, 1.25), size=(200, 200))
        fundobotao.pos_hint = {'center_x': 0.5, 'center_y': 0.6}

        self.inicial_button2 =Button(
            text='[b]ATC[/b]',
            size_hint=(0.6, None),
            font_name='LemonMilk',
            font_size=50,
            size=(800, 60),
            pos_hint={'center_x': 0.54, 'center_y': 0.4},
            color=get_color_from_hex('#baa673'),
            halign='center',
            background_color=(0, 0, 0, 0),
            markup=True
        )
        self.inicial_button2.bind(on_release=self.go_to_login2_page)

        fundobotao2 = Image(source='images/fundo_botao.png', size_hint=(1.2, 1.25), size=(200, 100))
        fundobotao2.pos_hint = {'center_x': 0.5, 'center_y': 0.4}

        self.inicial_button3 =Button(
            text='[b]SGQ[/b]',
            size_hint=(0.6, None),
            font_name='LemonMilk',
            font_size=50,
            size=(800, 60),
            pos_hint={'center_x': 0.53, 'center_y': 0.2},
            color=get_color_from_hex('#baa673'),
            halign='center',
            background_color=(0, 0, 0, 0),
            markup=True
        )
        self.inicial_button3.bind(on_release=self.go_to_dados_clientes)

        fundobotao3 = Image(source='images/fundo_botao.png', size_hint=(1.2, 1.25), size=(200, 200))
        fundobotao3.pos_hint = {'center_x': 0.5, 'center_y': 0.2}

        self.layout.add_widget(self.inicial_button)
        self.layout.add_widget(self.inicial_button2)
        self.layout.add_widget(self.inicial_button3)
        self.layout.add_widget(fundobotao)
        self.layout.add_widget(fundobotao2)
        self.layout.add_widget(fundobotao3)
        self.layout.add_widget(logo)
        self.layout.add_widget(button)
        self.layout.add_widget(lupa)
        self.layout.add_widget(comercial)
        self.add_widget(self.layout)

    def go_to_login_page(self, instance):
        self.manager.current = 'Login'

    def go_to_login2_page(self, instance):
        self.manager.current = 'Login2'    

    def go_to_dados_clientes(self, instance):
        self.manager.current = 'Cliente'
    
class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.6)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.53, 'center_y': 0.82}

        user = Image(source='images/do-utilizador.png', size_hint=(0.05, 0.05), size=(150, 150))
        user.pos_hint = {'center_x': 0.13, 'center_y': 0.55}

        senha = Image(source='images/chave.png', size_hint=(0.05, 0.05), size=(150, 150))
        senha.pos_hint = {'center_x': 0.13, 'center_y': 0.47}

        self.titulo_label = Label(
            text="[b]Saúde e Segurança\n do Trabalho[/b]",
            size_hint=(0.8, None),
            font_name='LemonMilk',
            font_size=30,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.email_input = TextInput(
            hint_text='Digite seu e-mail',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        self.senha_input = TextInput(
            hint_text='Digite sua senha',
            font_size=25,
            size_hint=(0.65, 0.05),
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.47},
            password=True
        )

        self.next_button = Button(
            text='Fazer login',
            size_hint=(0.5, 0.1),
            font_size=30,
            font_name='LemonMilk',
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.login)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.1, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.titulo_label)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(self.senha_input)
        self.layout.add_widget(logo)
        self.layout.add_widget(user)
        self.layout.add_widget(senha)
        self.add_widget(self.layout)
    
    def login(self, instance):
        email = self.email_input.text
        password = self.senha_input.text

        try:
            auth = firebase.auth()
            user = auth.sign_in_with_email_and_password(email, password)
            self.manager.current = 'Obras'
            App.get_running_app().email = email
            print("Login bem-sucedido:", user)
            
        except Exception as e:
            print("Erro de login:", str(e))
            self.show_login_error_popup(str(e))

    def show_login_error_popup(self, message):
        error_popup = Popup(
            title='Erro de Login',
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 150)
        )
        error_popup.open()

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class LoginPage2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.6)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.53, 'center_y': 0.82}

        user = Image(source='images/do-utilizador.png', size_hint=(0.05, 0.05), size=(150, 150))
        user.pos_hint = {'center_x': 0.13, 'center_y': 0.55}

        senha = Image(source='images/chave.png', size_hint=(0.05, 0.05), size=(150, 150))
        senha.pos_hint = {'center_x': 0.13, 'center_y': 0.47}

        self.titulo_label = Label(
            text="[b]sistema de gestão de qualidade[/b]",
            size_hint=(0.8, None),
            font_name='LemonMilk',
            font_size=30,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.email_input = TextInput(
            hint_text='Digite seu e-mail',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        self.senha_input = TextInput(
            hint_text='Digite sua senha',
            font_size=25,
            size_hint=(0.65, 0.05),
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.47},
            password=True
        )

        self.next_button = Button(
            text='Fazer login',
            size_hint=(0.5, 0.1),
            font_size=30,
            font_name='LemonMilk',
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.login)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.1, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.titulo_label)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(self.senha_input)
        self.layout.add_widget(logo)
        self.layout.add_widget(user)
        self.layout.add_widget(senha)
        self.add_widget(self.layout)
    
    def login(self, instance):
        email = self.email_input.text
        password = self.senha_input.text

        try:
            auth2 = firebase2.auth()
            user = auth2.sign_in_with_email_and_password(email, password)
            self.manager.current = 'Cliente'
            App.get_running_app().email = email
            print("Login bem-sucedido:", user)
            
        except Exception as e:
            print("Erro de login:", str(e))
            self.show_login_error_popup(str(e))

    def show_login_error_popup(self, message):
        error_popup = Popup(
            title='Erro de Login',
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 150)
        )
        error_popup.open()

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class ObrasPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.obra_label = Label(
            text='Escolha a Obra:',
            size_hint=(None, None),
            font_name='LemonMilk',
            font_size=40,
            size=(800, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        self.obra_spinner = Spinner(
            text='Selecione uma obra',
            values=('MANDACARU', 'VIDA', 'AQUARELA', 'LIBERTÁ', 'BRAVIELLO', 'SOLAR PLANALTO', 'CORTEVA - COMERCIAL', 'FOCO-COMERCIAL'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.6, 0.08),
            size=(600, 50),
            background_color=get_color_from_hex('#80ecff'),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_data_avaliacao)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.obra_label)
        self.layout.add_widget(self.obra_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_data_avaliacao(self, instance):
        email = App.get_running_app().email
        obra = self.obra_spinner.text
        App.get_running_app().responses = {'email': email, 'obra': obra}
        App.get_running_app().root.current = 'DataAvaliacao'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class DataAvaliacaoPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        # Salve a imagem processada temporariamente em um arquivo
        darkened_image.save('images/darkened_fundo.jpg')

        # Exiba a imagem processada na interface do usuário
        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.data_label = Label(
            text='DATA DA AVALIAÇÃO:',
            size_hint=(None, None),
            font_name='LemonMilk',
            font_size=40,
            size=(800, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        self.data_input = TextInput(
            hint_text='DD/MM/AAAA',
            multiline=False,
            size_hint=(0.3, 0.05),
            font_size=26,
            size=(200, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.5, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_nome_avaliador)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.data_label)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(self.data_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

        Clock.schedule_interval(self.automatic_date_input, 0.1)

    def automatic_date_input(self, dt):
        current_text = self.data_input.text
        if len(current_text) == 2 or len(current_text) == 5:
            current_text += '/'
            self.data_input.text = current_text

    def switch_to_nome_avaliador(self, instance):
        email = App.get_running_app().email
        obra = App.get_running_app().responses['obra']
        data_avaliacao = self.data_input.text
        App.get_running_app().responses['data_avaliacao'] = data_avaliacao
        App.get_running_app().root.current = 'NomeAvaliador'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class NomeAvaliadorPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.nome_avaliador_label = Label(
            text='NOME DO AVALIADOR:',
            size_hint=(None, None),
            font_name='LemonMilk',
            font_size=40,
            size=(800, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        self.nome_avaliador_input = TextInput(
            hint_text='Digite o nome do avaliador',
            size_hint=(0.7, 0.06),
            font_size=30,
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.5, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_pergunta_multipla_escolha)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.nome_avaliador_label)
        self.layout.add_widget(self.nome_avaliador_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_pergunta_multipla_escolha(self, instance):
        email = App.get_running_app().email
        obra = App.get_running_app().responses['obra']
        data_avaliacao = App.get_running_app().responses['data_avaliacao']
        nome_avaliador = self.nome_avaliador_input.text
        App.get_running_app().responses['nome_avaliador'] = nome_avaliador
        App.get_running_app().root.current = 'PerguntaMultiplaEscolha_1'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PerguntaMultiplaEscolhaPage(Screen):
    def __init__(self, pergunta, titulo, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.titulo_label = Label(
            text=f'[b]{titulo}[/b]',
            size_hint=(0.8, None),  # Define o tamanho do widget Label para ocupar a largura total
            height=50,  # Defina a altura desejada para o título
            font_name='LemonMilk',
            font_size=32,
            pos_hint={'center_x': 0.5, 'center_y': 0.675},  # Ajuste o posicionamento conforme necessário
            text_size=(None,self.width),  # Define o tamanho do texto para ocupar a largura total do widget Label
            color=get_color_from_hex('#baa673'),
            halign='center',
            markup=True
        )

        fundo = Image(source='images/pretin.png', size_hint=(1.0, 0.65), size=(200, 200))
        fundo.pos_hint = {'center_x': 0.5, 'center_y': 0.51}
        fundo.color = [1, 1, 1, 0.3]

        self.layout.add_widget(fundo)

        self.pergunta_label = Label(
            text=pergunta,
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.51},
            halign='center',
            markup=True
        )   

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('CONFORME', 'NÃO CONFORME', 'NÃO SE APLICA'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.325},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.7, 'center_y': 0.15},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_next_page)

        self.back_button = Button(
            text='Voltar',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.3, 'center_y': 0.15},
            background_color=get_color_from_hex('#80ecff')
        )
        self.back_button.bind(on_press=self.switch_to_previous_page)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.titulo_label)
        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_next_page(self, instance):
        opcao_selecionada = self.opcoes_spinner.text

        if opcao_selecionada != 'Selecione uma opção':
            page_number = int(self.name.split('_')[-1])
            pergunta_key = f'pergunta_{page_number}'

            # Adicione a resposta à lista de respostas
            App.get_running_app().responses[pergunta_key] = opcao_selecionada

            # Verifica se há mais perguntas a serem exibidas
            if page_number < len(perguntas):
                next_page = f'PerguntaMultiplaEscolha_{page_number + 1}'
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = next_page
            else:
                # Todas as perguntas foram respondidas, então vá para a página de salvar dados
                self.manager.current = 'SalvarDados'
        else:
            self.show_selection_error_popup()
        
    def switch_to_previous_page(self, instance):
        page_number = int(self.name.split('_')[-1])
        if page_number > 1:
            previous_page = f'PerguntaMultiplaEscolha_{page_number - 1}'  # Volta para a pergunta anterior
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = previous_page
        else:
            self.manager.current = 'NomeAvaliador'    

    def show_selection_error_popup(self):
        error_popup = Popup(
            title='Erro de Seleção',
            content=Label(text='Por favor, selecione uma \nopção antes de avançar.'),
            font_name='LemonMilk',
            size_hint=(None, None),
            size=(300, 150)
        )
        error_popup.open()

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class SalvarDadosPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.salvar_button = Button(
            text='Salvar',
            size_hint=(0.5, 0.2),
            font_name='LemonMilk',
            font_size=30,
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0, 1, 0, 1)
        )
        self.salvar_button.bind(on_press=self.salvar_dados)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.salvar_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def salvar_dados(self, instance):
        email = App.get_running_app().email
        obra = App.get_running_app().responses['obra']
        data_avaliacao = App.get_running_app().responses['data_avaliacao']
        nome_avaliador = App.get_running_app().responses['nome_avaliador']

        # Autentique com as credenciais JSON
        gc = gspread.service_account(filename=json_key_file)

        # Abra a primeira planilha (índice 0) no arquivo do Google Sheets
        worksheet = gc.open_by_key(spreadsheet_id).sheet1  # Acesse a primeira planilha usando .sheet1

        # Dados a serem inseridos na planilha
        data_to_insert = [email, obra, data_avaliacao, nome_avaliador]

        # Adicione as respostas das perguntas de escolha múltipla às colunas
        for i, pergunta in enumerate(perguntas, start=1):
            pergunta_key = f'pergunta_{i}'
            if pergunta_key in App.get_running_app().responses:
                data_to_insert.append(App.get_running_app().responses[pergunta_key])
            else:
                data_to_insert.append('')

        # Insira os dados na planilha
        worksheet.append_row(data_to_insert)

        self.confirmacao_label = Label(
            text="[color=#00FF00]dados salvos com sucesso![/color]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            halign='center',
            markup=True
        )
        self.layout.add_widget(self.confirmacao_label)

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class ClientePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        fundobotao = Image(source='images/fundo_botao2.png', size_hint=(1.0, 0.5), size=(200, 200))
        fundobotao.pos_hint = {'center_x': 0.5, 'center_y': 0.595}
        self.layout.add_widget(fundobotao)

        fundobotao2 = Image(source='images/fundo_botao2.png', size_hint=(1.0, 0.5), size=(200, 200))
        fundobotao2.pos_hint = {'center_x': 0.5, 'center_y': 0.395}
        self.layout.add_widget(fundobotao2)

        fundobotao3 = Image(source='images/fundo_botao2.png', size_hint=(1.0, 0.5), size=(200, 200))
        fundobotao3.pos_hint = {'center_x': 0.5, 'center_y': 0.195}
        self.layout.add_widget(fundobotao3)

        self.cliente_button =Button(
            text='[b]Entrega da Obra[/b]',
            size_hint=(0.6, None),
            font_name='LemonMilk',
            font_size=30,
            size=(800, 60),
            pos_hint={'center_x': 0.56, 'center_y': 0.6},
            color=get_color_from_hex('#baa673'),
            background_color=(0, 0, 0, 0),
            markup=True
        )
        self.cliente_button.bind(on_release=self.go_to_entrega_page)

        entrega = Image(source='images/entrega.png', size_hint=(0.28, 0.28), size=(200, 200))
        entrega.pos_hint = {'center_x': 0.15, 'center_y': 0.6}

        self.cliente2_button =Button(
            text='[b]Pós Entrega[/b]',
            size_hint=(0.6, None),
            font_name='LemonMilk',
            font_size=30,
            size=(800, 60),
            halign='center',
            pos_hint={'center_x': 0.57, 'center_y': 0.4},
            color=get_color_from_hex('#baa673'),
            background_color=(0, 0, 0, 0),
            markup=True
        )
        self.cliente2_button.bind(on_release=self.go_to_posentrega_page)

        pos = Image(source='images/pos.png', size_hint=(0.3, 0.3), size=(200, 200))
        pos.pos_hint = {'center_x': 0.15, 'center_y': 0.4}

        self.cliente3_button =Button(
            text='[b]Assistência Técnica[/b]',
            size_hint=(0.6, None),
            font_name='LemonMilk',
            font_size=28,
            size=(800, 60),
            pos_hint={'center_x': 0.575, 'center_y': 0.2},
            color=get_color_from_hex('#baa673'),
            background_color=(0, 0, 0, 0),
            markup=True
        )
        self.cliente3_button.bind(on_release=self.go_to_assist)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        assistenciatec = Image(source='images/assistenciatec.png', size_hint=(0.28, 0.28), size=(200, 200))
        assistenciatec.pos_hint = {'center_x': 0.15, 'center_y': 0.2}

        self.layout.add_widget(self.cliente_button)
        self.layout.add_widget(self.cliente2_button)
        self.layout.add_widget(self.cliente3_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.layout.add_widget(entrega)
        self.layout.add_widget(pos)
        self.layout.add_widget(assistenciatec)
        self.add_widget(self.layout)

    def go_to_entrega_page(self, instance):
        self.manager.current = 'EntregaObra'

    def go_to_posentrega_page(self, instance):
        self.manager.current = 'Posentrega'

    def go_to_assist(self, instance):
        self.manager.current = 'AssistEntrega'        

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class EntregaObraPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.cliente_label = Label(
            text="Cliente:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.6},
            halign='center',
            markup=True
        )

        self.data_label = Label(
            text="Data:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.5},
            halign='center',
            markup=True
        )

        self.obra_label = Label(
            text="Emp/Obra:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.4},
            halign='center',
            markup=True
        )

        self.responsavel_label = Label(
            text="Responsável:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=18,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.3},
            halign='center',
            markup=True
        )

        self.cliente_input = TextInput(
            hint_text='Digite o nome do cliente',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.6}
        )

        self.data_input = TextInput(
            hint_text='DD/MM/AAAA',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.5}
        )

        self.obra_input = TextInput(
            hint_text='Empreendimento/obra',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.4}
        )

        self.responsavel_input = TextInput(
            hint_text='Digite o nome do responsável',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.3}
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png', 
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        Clock.schedule_interval(self.automatic_date_input, 0.1)

        self.layout.add_widget(self.cliente_label)
        self.layout.add_widget(self.data_label)
        self.layout.add_widget(self.obra_label)
        self.layout.add_widget(self.responsavel_label)
        self.layout.add_widget(self.cliente_input)
        self.layout.add_widget(self.data_input)
        self.layout.add_widget(self.obra_input)
        self.layout.add_widget(self.responsavel_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def automatic_date_input(self, dt):
        current_text = self.data_input.text
        if len(current_text) == 2 or len(current_text) == 5:
            current_text += '/'
            self.data_input.text = current_text

    def switch_to_perguntas(self, instance):
        data = self.data_input.text
        cliente = self.cliente_input.text 
        obra = self.obra_input.text
        responsavel = self.responsavel_input.text
        App.get_running_app().responses['data'] = data
        App.get_running_app().responses['cliente'] = cliente
        App.get_running_app().responses['obra'] = obra
        App.get_running_app().responses['responsavel'] = responsavel
        App.get_running_app().root.current = 'Pergunta_1'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PerguntasPage(Screen):
    def __init__(self,pergunta2, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.titulo_label = Label(
            text="[b]A - Atributos da Qualidade[/b]",
            size_hint=(0.8, None),
            font_name='LemonMilk',
            font_size=30,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.675},
            halign='center',
            markup=True
        )

        fundo = Image(source='images/pretin.png', size_hint=(1.0, 0.65), size=(200, 200))
        fundo.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
        fundo.color = [1, 1, 1, 0.3]

        self.layout.add_widget(fundo)

        self.pergunta_label = Label(
            text=pergunta2,
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_name='LemonMilk',
            font_size=25,
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=get_color_from_hex('#80ecff')
        )

        self.pergunta2_label = Label(
            text="é importante pra você?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.325},
            halign='center',
            markup=True
        )

        self.opcoes_spinner2 = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('SIM', 'NÃO'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.05),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.275},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.7, 'center_y': 0.15},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_next_page)

        self.back_button = Button(
            text='Voltar',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.3, 'center_y': 0.15},
            background_color=get_color_from_hex('#80ecff')
        )
        self.back_button.bind(on_press=self.switch_to_previous_page)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.titulo_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.opcoes_spinner2)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_next_page(self, instance):
        opcao_selecionada = self.opcoes_spinner.text
        opcao_selecionada2 = self.opcoes_spinner2.text

        if opcao_selecionada != 'Selecione uma opção':
            if opcao_selecionada2 != 'É importante pra você?':
                page_number = int(self.name.split('_')[-1])  # Obtém o número da página atual
                pergunta_key = f'pergunta_{page_number}'

                # Adicione a resposta à lista de respostas
                App.get_running_app().responses[pergunta_key] = opcao_selecionada
                App.get_running_app().responses['Importante'] = opcao_selecionada2

            # Verifica se há mais perguntas a serem exibidas
                if page_number < len(perguntas2):
                    next_page = f'Pergunta_{page_number + 1}'
                    self.manager.transition = SlideTransition(direction="left")
                    self.manager.current = next_page
                else:
                # Todas as perguntas foram respondidas, então vá para a página de salvar dados
                    self.manager.current = 'Perguntas3'
            else:
                self.show_selection_error_popup()
        else:
            self.show_selection_error_popup()          

    def switch_to_previous_page(self, instance):
        page_number = int(self.name.split('_')[-1])
        if page_number > 1:
            previous_page = f'Pergunta_{page_number - 1}'  # Volta para a pergunta anterior
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = previous_page
        else:
            self.manager.current = 'DadosCliente'    

    def show_selection_error_popup(self):
        error_popup = Popup(
            title='Erro de Seleção',
            content=Label(text='Por favor, selecione uma \nopção antes de avançar.'),
            size_hint=(None, None),
            size=(300, 150)
        )
        error_popup.open()

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class Perguntas3Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="B - Você já fez alguma\nreclamação na construtora?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            color=get_color_from_hex('#baa673'),
            font_size=30,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.resposta_spinner = Spinner(
            text="Selecione a resposta",
            values=["Sim", "Não"],
            font_name='LemonMilk',
            size_hint=(0.5, 0.1),
            font_size=25,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            background_color=get_color_from_hex('#80ecff')
        )
        self.resposta_spinner.bind(text=self.on_resposta_selected)

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_name='LemonMilk',
            font_size=25,
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=get_color_from_hex('#80ecff')
        )
        
        self.pergunta2_label = Label(
            text="O atendimento da construtora \nda sua reclamação foi...",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            halign='center',
            markup=True
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.resposta_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def on_resposta_selected(self, instance, text):
        if text == "Sim":
            self.layout.add_widget(self.opcoes_spinner)
            self.layout.add_widget(self.pergunta2_label)
        elif text == "Não":
            self.layout.remove_widget(self.opcoes_spinner)
            self.layout.remove_widget(self.pergunta2_label)    

    def switch_to_perguntas(self, instance):
        respostas2 = self.resposta_spinner.text
        spinner2 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['respostas2'] = respostas2
        App.get_running_app().responses['spinner2'] = spinner2
        App.get_running_app().root.current = 'Perguntas4'


    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class Perguntas4Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]C - Sobre sua impressao geral\n a imagem...[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta1_label = Label(
            text="Da construtora",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            background_color=get_color_from_hex('#80ecff')
        )

        self.pergunta2_label = Label(
            text="Da obra",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            halign='center',
            markup=True
        )

        self.opcoes2_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta1_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.opcoes2_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        spinner3 = self.opcoes_spinner.text
        spinner4 = self.opcoes2_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['respostas2'] 
        App.get_running_app().responses['spinner2'] 
        App.get_running_app().responses['spinner3'] = spinner3
        App.get_running_app().responses['spinner4'] = spinner4
        App.get_running_app().root.current = 'Perguntas5'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class Perguntas5Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]D - Se você pudesse\nvoltar no tempo...[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta2_label = Label(
            text="Contrataria da TOP Construtora para\nexecutar outra obra?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('Certamente que não', 'É provável que não', 'Talvez sim, talvez não','É provavel que sim', 'Certamente que sim'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        spinner5 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['respostas2'] 
        App.get_running_app().responses['spinner2'] 
        App.get_running_app().responses['spinner3'] 
        App.get_running_app().responses['spinner4'] 
        App.get_running_app().responses['spinner5'] = spinner5
        App.get_running_app().root.current = 'Perguntas6'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class Perguntas6Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="O Sr. (a) tem algum comentário,\n sugestão ou crítica a fazer?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.cliente_input = TextInput(
            hint_text='Digite aqui...',
            size_hint=(0.8, 0.2),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.next_button = Button(
            text='Salvar respostas',
            size_hint=(0.5, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.salvar_dados)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(logo)
        self.layout.add_widget(self.cliente_input)
        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.add_widget(self.layout)

    def salvar_dados(self, instance):
        comentario = self.cliente_input.text
        data = App.get_running_app().responses['data'] 
        cliente = App.get_running_app().responses['cliente'] 
        obra = App.get_running_app().responses['obra'] 
        responsavel1 = App.get_running_app().responses['responsavel'] 
        respostas2 = App.get_running_app().responses['respostas2'] 
        spinner2 = App.get_running_app().responses['spinner2'] 
        spinner3 = App.get_running_app().responses['spinner3'] 
        spinner4 = App.get_running_app().responses['spinner4'] 
        spinner5 = App.get_running_app().responses['spinner5'] 
        App.get_running_app().responses['input'] = comentario

        gc = gspread.service_account(filename=json_key_file)

        # Abra a primeira planilha (índice 0) no arquivo do Google Sheets
        worksheet = gc.open_by_key(spreadsheet_id2).sheet1  # Acesse a primeira planilha usando .sheet1

        # Dados a serem inseridos na planilha
        data_to_insert = [data, cliente, obra, responsavel1] 

        data_to_insert2 = []

        for i, pergunta in enumerate(perguntas2, start=1):
            pergunta_key = f'pergunta_{i}'
            if pergunta_key in App.get_running_app().responses:
                data_to_insert2.append(App.get_running_app().responses[pergunta_key])
            else:
                data_to_insert2.append('')

        for i, pergunta in enumerate(perguntas2, start=1):
            pergunta_key = f'pergunta_{i}'
            if pergunta_key in App.get_running_app().responses:
                data_to_insert2.append(App.get_running_app().responses['Importante'])
            else:
                data_to_insert2.append('')   

        data_to_insert3 = [spinner2, spinner3, spinner4, respostas2, spinner5, comentario]

        worksheet.append_row(data_to_insert + data_to_insert2 + data_to_insert3)
        
        self.confirmacao_label = Label(
            text="[color=#00FF00]dados salvos com sucesso![/color]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            halign='center',
            markup=True
        )
        self.layout.add_widget(self.confirmacao_label)

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'    

class PosEntregaPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.cliente_label = Label(
            text="Cliente:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.6},
            halign='center',
            markup=True
        )

        self.data_label = Label(
            text="Data:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.5},
            halign='center',
            markup=True
        )

        self.obra_label = Label(
            text="Emp/Obra:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.4},
            halign='center',
            markup=True
        )

        self.responsavel_label = Label(
            text="Responsável:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=18,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.3},
            halign='center',
            markup=True
        )

        self.cliente_input = TextInput(
            hint_text='Digite o nome do cliente',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.6}
        )

        self.data_input = TextInput(
            hint_text='DD/MM/AAAA',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.5}
        )

        self.obra_input = TextInput(
            hint_text='Empreendimento/obra',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.4}
        )

        self.responsavel_input = TextInput(
            hint_text='Digite o nome do responsável',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.3}
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png', 
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        Clock.schedule_interval(self.automatic_date_input, 0.1)

        self.layout.add_widget(self.cliente_label)
        self.layout.add_widget(self.data_label)
        self.layout.add_widget(self.obra_label)
        self.layout.add_widget(self.responsavel_label)
        self.layout.add_widget(self.cliente_input)
        self.layout.add_widget(self.data_input)
        self.layout.add_widget(self.obra_input)
        self.layout.add_widget(self.responsavel_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def automatic_date_input(self, dt):
        current_text = self.data_input.text
        if len(current_text) == 2 or len(current_text) == 5:
            current_text += '/'
            self.data_input.text = current_text

    def switch_to_perguntas(self, instance):
        data = self.data_input.text
        cliente = self.cliente_input.text 
        obra = self.obra_input.text
        responsavel = self.responsavel_input.text
        App.get_running_app().responses['data'] = data
        App.get_running_app().responses['cliente'] = cliente
        App.get_running_app().responses['obra'] = obra
        App.get_running_app().responses['responsavel'] = responsavel
        App.get_running_app().root.current = 'PosPerguntas'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PosPerguntasPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]A - Atributos da Qualidade[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta1_label = Label(
            text="1 - Como avalia o atendimento\n de assistência técnica?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            background_color=get_color_from_hex('#80ecff')
        )

        self.pergunta2_label = Label(
            text="2 - Qual o seu nível de satisfação\n com o empreendimento/obra?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            halign='center',
            markup=True
        )

        self.opcoes2_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta1_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.opcoes2_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        spinner3 = self.opcoes_spinner.text
        spinner4 = self.opcoes2_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta1'] = spinner3
        App.get_running_app().responses['pergunta2'] = spinner4
        App.get_running_app().root.current = 'PosPerguntas2'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PosPerguntas2Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="B - Você já fez alguma\nreclamação na construtora?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            color=get_color_from_hex('#baa673'),
            font_size=30,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.resposta_spinner = Spinner(
            text="Selecione a resposta",
            values=["Sim", "Não"],
            font_name='LemonMilk',
            size_hint=(0.5, 0.1),
            font_size=25,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            background_color=get_color_from_hex('#80ecff')
        )
        self.resposta_spinner.bind(text=self.on_resposta_selected)

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_name='LemonMilk',
            font_size=25,
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=get_color_from_hex('#80ecff')
        )
        
        self.pergunta2_label = Label(
            text="O atendimento da construtora \nda sua reclamação foi...",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            halign='center',
            markup=True
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.resposta_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def on_resposta_selected(self, instance, text):
        if text == "Sim":
            self.layout.add_widget(self.opcoes_spinner)
            self.layout.add_widget(self.pergunta2_label)
        elif text == "Não":
            self.layout.remove_widget(self.opcoes_spinner)
            self.layout.remove_widget(self.pergunta2_label)    

    def switch_to_perguntas(self, instance):
        respostas3 = self.resposta_spinner.text
        respostas4 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta1']
        App.get_running_app().responses['pergunta2']
        App.get_running_app().responses['pergunta3'] = respostas3
        App.get_running_app().responses['pergunta4'] = respostas4
        App.get_running_app().root.current = 'PosPerguntas3'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PosPerguntas3Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]C - Sobre sua impressao geral\n a imagem...[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta1_label = Label(
            text="Da construtora",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            background_color=get_color_from_hex('#80ecff')
        )

        self.pergunta2_label = Label(
            text="Da obra",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            halign='center',
            markup=True
        )

        self.opcoes2_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta1_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.opcoes2_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        pergunta5 = self.opcoes_spinner.text
        pergunta6 = self.opcoes2_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta1']
        App.get_running_app().responses['pergunta2']
        App.get_running_app().responses['pergunta3'] 
        App.get_running_app().responses['pergunta4'] 
        App.get_running_app().responses['pergunta5'] = pergunta5
        App.get_running_app().responses['pergunta6'] = pergunta6
        App.get_running_app().root.current = 'PosPerguntas4'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PosPerguntas4Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]D - Se você pudesse\nvoltar no tempo...[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta2_label = Label(
            text="Contrataria da TOP Construtora para\nexecutar outra obra?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('Certamente que não', 'É provável que não', 'Talvez sim, talvez não','É provavel que sim', 'Certamente que sim'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        resposta7 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta1']
        App.get_running_app().responses['pergunta2']
        App.get_running_app().responses['pergunta3'] 
        App.get_running_app().responses['pergunta4'] 
        App.get_running_app().responses['pergunta5'] 
        App.get_running_app().responses['pergunta6'] 
        App.get_running_app().responses['pergunta7'] = resposta7
        App.get_running_app().root.current = 'PosPerguntas5'
        
    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PosPerguntas5Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]E - Tempo de Entrega[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta2_label = Label(
            text="Há quanto tempo recebeu\n o empreendimento/obra?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('1 - 3 meses','4 - 6 meses','acima de seis meses'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        resposta8 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta1']
        App.get_running_app().responses['pergunta2']
        App.get_running_app().responses['pergunta3'] 
        App.get_running_app().responses['pergunta4'] 
        App.get_running_app().responses['pergunta5'] 
        App.get_running_app().responses['pergunta6'] 
        App.get_running_app().responses['pergunta7'] 
        App.get_running_app().responses['pergunta8'] = resposta8
        App.get_running_app().root.current = 'PosPerguntas6'
        
    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class PosPerguntas6Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="O Sr. (a) tem algum comentário,\n sugestão ou crítica a fazer?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.cliente_input = TextInput(
            hint_text='Digite aqui...',
            size_hint=(0.8, 0.2),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.next_button = Button(
            text='Salvar respostas',
            size_hint=(0.5, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.salvar_dados)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(logo)
        self.layout.add_widget(self.cliente_input)
        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.add_widget(self.layout)

    def salvar_dados(self, instance):
        comentario = self.cliente_input.text
        data = App.get_running_app().responses['data'] 
        cliente = App.get_running_app().responses['cliente'] 
        obra = App.get_running_app().responses['obra'] 
        responsavel = App.get_running_app().responses['responsavel']  
        App.get_running_app().responses['comentario'] = comentario
        pergunta1 = App.get_running_app().responses['pergunta1']
        pergunta2 = App.get_running_app().responses['pergunta2']
        pergunta3 = App.get_running_app().responses['pergunta3'] 
        pergunta4 = App.get_running_app().responses['pergunta4'] 
        pergunta5 = App.get_running_app().responses['pergunta5'] 
        pergunta6 = App.get_running_app().responses['pergunta6'] 
        pergunta7 = App.get_running_app().responses['pergunta7'] 
        pergunta8 = App.get_running_app().responses['pergunta8'] 

        gc = gspread.service_account(filename=json_key_file)

        # Abra a primeira planilha (índice 0) no arquivo do Google Sheets
        worksheet = gc.open_by_key(spreadsheet_id3).sheet1  # Acesse a primeira planilha usando .sheet1

        # Dados a serem inseridos na planilha
        data_to_insert = [data, cliente, obra, responsavel, pergunta1, pergunta2, pergunta3, pergunta4, pergunta5, pergunta6, pergunta7, pergunta8, comentario]  

        worksheet.append_row(data_to_insert)

        self.confirmacao_label = Label(
            text="[color=#00FF00]dados salvos com sucesso![/color]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            halign='center',
            markup=True
        )
        self.layout.add_widget(self.confirmacao_label)

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class AssistEntregaObraPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.cliente_label = Label(
            text="Cliente:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.6},
            halign='center',
            markup=True
        )

        self.data_label = Label(
            text="Data:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.5},
            halign='center',
            markup=True
        )

        self.obra_label = Label(
            text="Emp/Obra:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=23,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.4},
            halign='center',
            markup=True
        )

        self.responsavel_label = Label(
            text="Responsável:",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=18,
            size=self.size,
            pos_hint={'center_x': 0.15, 'center_y': 0.3},
            halign='center',
            markup=True
        )

        self.cliente_input = TextInput(
            hint_text='Digite o nome do cliente',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.6}
        )

        self.data_input = TextInput(
            hint_text='DD/MM/AAAA',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.5}
        )

        self.obra_input = TextInput(
            hint_text='Empreendimento/obra',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.4}
        )

        self.responsavel_input = TextInput(
            hint_text='Digite o nome do responsável',
            size_hint=(0.65, 0.05),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.6, 'center_y': 0.3}
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png', 
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        Clock.schedule_interval(self.automatic_date_input, 0.1)

        self.layout.add_widget(self.cliente_label)
        self.layout.add_widget(self.data_label)
        self.layout.add_widget(self.obra_label)
        self.layout.add_widget(self.responsavel_label)
        self.layout.add_widget(self.cliente_input)
        self.layout.add_widget(self.data_input)
        self.layout.add_widget(self.obra_input)
        self.layout.add_widget(self.responsavel_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def automatic_date_input(self, dt):
        current_text = self.data_input.text
        if len(current_text) == 2 or len(current_text) == 5:
            current_text += '/'
            self.data_input.text = current_text

    def switch_to_perguntas(self, instance):
        data = self.data_input.text
        cliente = self.cliente_input.text 
        obra = self.obra_input.text
        responsavel = self.responsavel_input.text
        App.get_running_app().responses['data'] = data
        App.get_running_app().responses['cliente'] = cliente
        App.get_running_app().responses['obra'] = obra
        App.get_running_app().responses['responsavel'] = responsavel
        App.get_running_app().root.current = 'AssistPergunta_1'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'        

class AssistPerguntasPage(Screen):
    def __init__(self,pergunta3, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.titulo_label = Label(
            text="[b]A - Atributos da Qualidade[/b]",
            size_hint=(0.8, None),
            font_name='LemonMilk',
            font_size=30,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.675},
            halign='center',
            markup=True
        )

        fundo = Image(source='images/pretin.png', size_hint=(1.0, 0.65), size=(200, 200))
        fundo.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
        fundo.color = [1, 1, 1, 0.3]

        self.layout.add_widget(fundo)

        self.pergunta_label = Label(
            text=pergunta3,
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_name='LemonMilk',
            font_size=25,
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=get_color_from_hex('#80ecff')
        )

        self.pergunta2_label = Label(
            text="é importante pra você?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.325},
            halign='center',
            markup=True
        )

        self.opcoes_spinner2 = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('SIM', 'NÃO'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.05),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.275},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.7, 'center_y': 0.15},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_next_page)

        self.back_button = Button(
            text='Voltar',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.3, 'center_y': 0.15},
            background_color=get_color_from_hex('#80ecff')
        )
        self.back_button.bind(on_press=self.switch_to_previous_page)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.titulo_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.opcoes_spinner2)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_next_page(self, instance):
        opcao_selecionada = self.opcoes_spinner.text
        opcao_selecionada2 = self.opcoes_spinner2.text

        if opcao_selecionada != 'Selecione uma opção':
            if opcao_selecionada2 != 'É importante pra você?':
                page_number = int(self.name.split('_')[-1])  # Obtém o número da página atual
                pergunta_key = f'AssistPergunta_{page_number}'

                # Adicione a resposta à lista de respostas
                App.get_running_app().responses[pergunta_key] = opcao_selecionada
                App.get_running_app().responses['Importante'] = opcao_selecionada2

            # Verifica se há mais perguntas a serem exibidas
                if page_number < len(perguntas3):
                    next_page = f'AssistPergunta_{page_number + 1}'
                    self.manager.transition = SlideTransition(direction="left")
                    self.manager.current = next_page
                else:
                    self.manager.current = 'AssistPerguntas2'
            else:
                self.show_selection_error_popup()
        else:
            self.show_selection_error_popup()          

    def switch_to_previous_page(self, instance):
        page_number = int(self.name.split('_')[-1])
        if page_number > 1:
            previous_page = f'AssistPergunta_{page_number - 1}'  # Volta para a pergunta anterior
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = previous_page
        else:
            self.manager.current = 'Cliente'    

    def show_selection_error_popup(self):
        error_popup = Popup(
            title='Erro de Seleção',
            content=Label(text='Por favor, selecione uma \nopção antes de avançar.'),
            size_hint=(None, None),
            size=(300, 150)
        )
        error_popup.open()

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class AssistPerguntas2Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="B - Você já fez alguma\nreclamação na construtora?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            color=get_color_from_hex('#baa673'),
            font_size=30,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.resposta_spinner = Spinner(
            text="Selecione a resposta",
            values=["Sim", "Não"],
            font_name='LemonMilk',
            size_hint=(0.5, 0.1),
            font_size=25,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            background_color=get_color_from_hex('#80ecff')
        )
        self.resposta_spinner.bind(text=self.on_resposta_selected)

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_name='LemonMilk',
            font_size=25,
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=get_color_from_hex('#80ecff')
        )
        
        self.pergunta2_label = Label(
            text="O atendimento da construtora \nda sua reclamação foi...",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            halign='center',
            markup=True
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            font_name='LemonMilk',
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.resposta_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def on_resposta_selected(self, instance, text):
        if text == "Sim":
            self.layout.add_widget(self.opcoes_spinner)
            self.layout.add_widget(self.pergunta2_label)
        elif text == "Não":
            self.layout.remove_widget(self.opcoes_spinner)
            self.layout.remove_widget(self.pergunta2_label)    

    def switch_to_perguntas(self, instance):
        respostas3 = self.resposta_spinner.text
        respostas4 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta3'] = respostas3
        App.get_running_app().responses['pergunta4'] = respostas4
        App.get_running_app().root.current = 'AssistPerguntas3'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class AssistPerguntas3Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]C - Sobre sua impressao geral\n a imagem...[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta1_label = Label(
            text="Da construtora",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            background_color=get_color_from_hex('#80ecff')
        )

        self.pergunta2_label = Label(
            text="Da obra",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            halign='center',
            markup=True
        )

        self.opcoes2_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('RUIM', 'REGULAR', 'BOM','ÓTIMO', 'EXCELENTE'),
            font_size=30,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta1_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.opcoes2_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        spinner3 = self.opcoes_spinner.text
        spinner4 = self.opcoes2_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta3'] 
        App.get_running_app().responses['pergunta4'] 
        App.get_running_app().responses['pergunta5'] = spinner3
        App.get_running_app().responses['pergunta6'] = spinner4
        App.get_running_app().root.current = 'AssistPerguntas4'

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class AssistPerguntas4Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="[b]D - Se você pudesse\nvoltar no tempo...[/b]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=25,
            color=get_color_from_hex('#baa673'),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.pergunta2_label = Label(
            text="Contrataria da TOP Construtora para\nexecutar outra obra?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.525},
            halign='center',
            markup=True
        )

        self.opcoes_spinner = Spinner(
            markup = True,
            text='Selecione uma opção',
            values=('Certamente que não', 'É provável que não', 'Talvez sim, talvez não','É provavel que sim', 'Certamente que sim'),
            font_size=25,
            font_name='LemonMilk',
            size_hint=(0.7, 0.1),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=get_color_from_hex('#80ecff')
        )

        self.next_button = Button(
            text='Próximo',
            size_hint=(0.3, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.switch_to_perguntas)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.pergunta2_label)
        self.layout.add_widget(self.opcoes_spinner)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.layout.add_widget(logo)
        self.add_widget(self.layout)

    def switch_to_perguntas(self, instance):
        resposta7 = self.opcoes_spinner.text
        App.get_running_app().responses['data'] 
        App.get_running_app().responses['cliente'] 
        App.get_running_app().responses['obra'] 
        App.get_running_app().responses['responsavel'] 
        App.get_running_app().responses['pergunta3']
        App.get_running_app().responses['pergunta4']
        App.get_running_app().responses['pergunta5'] 
        App.get_running_app().responses['pergunta6'] 
        App.get_running_app().responses['pergunta7'] = resposta7
        App.get_running_app().root.current = 'AssistPerguntas5'
        
    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class AssistPerguntas5Page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()

        logo = Image(source='images/logo_empresa.png', size_hint=(0.9, 0.9), size=(200, 200))
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.82}

        pil_image = PILImage.open('images/fundo.jpg')
        enhancer = ImageEnhance.Brightness(pil_image)
        darkened_image = enhancer.enhance(0.8)  # Valor menor escurece mais

        darkened_image.save('images/darkened_fundo.jpg')

        background = Image(source='images/darkened_fundo.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background)

        self.pergunta_label = Label(
            text="O Sr. (a) tem algum comentário,\n sugestão ou crítica a fazer?",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            halign='center',
            markup=True
        )

        self.cliente_input = TextInput(
            hint_text='Digite aqui...',
            size_hint=(0.8, 0.2),
            font_size=25,
            size=(600, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.next_button = Button(
            text='Salvar respostas',
            size_hint=(0.5, 0.1),
            size=(200, 60),
            font_name='LemonMilk',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=get_color_from_hex('#80ecff')
        )
        self.next_button.bind(on_press=self.salvar_dados)

        self.home_button = Button(
            background_normal='images/botao-home.png',  # Substitua pelo caminho real da imagem
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.08, 'center_y': 0.05}
        )
        self.home_button.bind(on_release=self.switch_to_home)

        self.layout.add_widget(logo)
        self.layout.add_widget(self.cliente_input)
        self.layout.add_widget(self.pergunta_label)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.home_button)
        self.add_widget(self.layout)

    def salvar_dados(self, instance):
        comentario = self.cliente_input.text
        data = App.get_running_app().responses['data'] 
        cliente = App.get_running_app().responses['cliente'] 
        obra = App.get_running_app().responses['obra'] 
        responsavel = App.get_running_app().responses['responsavel'] 
        spinner1 = App.get_running_app().responses['pergunta3'] 
        spinner2 = App.get_running_app().responses['pergunta4'] 
        spinner3 = App.get_running_app().responses['pergunta5'] 
        spinner4 = App.get_running_app().responses['pergunta6'] 
        spinner5 = App.get_running_app().responses['pergunta7'] 
        App.get_running_app().responses['input'] = comentario

        gc = gspread.service_account(filename=json_key_file)

        # Abra a primeira planilha (índice 0) no arquivo do Google Sheets
        worksheet = gc.open_by_key(spreadsheet_id4).sheet1  # Acesse a primeira planilha usando .sheet1

        # Dados a serem inseridos na planilha
        data_to_insert = [data, cliente, obra, responsavel] 

        data_to_insert2 = []

        for i, pergunta in enumerate(perguntas3, start=1):
            pergunta_key = f'AssistPergunta_{i}'
            if pergunta_key in App.get_running_app().responses:
                data_to_insert2.append(App.get_running_app().responses[pergunta_key])
            else:
                data_to_insert2.append('')

        for i, pergunta in enumerate(perguntas3, start=1):
            pergunta_key = f'AssistPergunta_{i}'
            if pergunta_key in App.get_running_app().responses:
                data_to_insert2.append(App.get_running_app().responses['Importante'])
            else:
                data_to_insert2.append('')   

        data_to_insert3 = [spinner1, spinner2, spinner3, spinner4, spinner5, comentario]

        worksheet.append_row(data_to_insert + data_to_insert2 + data_to_insert3)
        
        self.confirmacao_label = Label(
            text="[color=#00FF00]dados salvos com sucesso![/color]",
            size_hint=(0.9, 0.7),
            font_name='LemonMilk',
            font_size=20,
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            halign='center',
            markup=True
        )
        self.layout.add_widget(self.confirmacao_label)

    def switch_to_home(self, instance):
        App.get_running_app().root.current = 'inicial'

class MyScreenManager(ScreenManager):
    def reset_to_first_page(self):
        self.current = 'inicial'

class MyApp(App):
    responses = {}
    def build(self):
        Config.read("config.ini")
        self.manager = MyScreenManager()
        self.inicial_page = inicialPage(name='inicial')
        self.email_page = LoginPage(name='Login')
        self.login_page = LoginPage2(name='Login2')
        self.obras_page = ObrasPage(name='Obras')
        self.data_avaliacao_page = DataAvaliacaoPage(name='DataAvaliacao')
        self.nome_avaliador_page = NomeAvaliadorPage(name='NomeAvaliador')
        self.salvar_dados_page = SalvarDadosPage(name='SalvarDados')
        self.entrega_page = EntregaObraPage(name='EntregaObra')
        self.pergunta3_page = Perguntas3Page(name='Perguntas3')
        self.pergunta4_page = Perguntas4Page(name='Perguntas4')
        self.pergunta5_page = Perguntas5Page(name='Perguntas5')
        self.pergunta6_page = Perguntas6Page(name='Perguntas6')
        self.posentrega_page = PosEntregaPage(name='Posentrega')
        self.pospergunta_page = PosPerguntasPage(name='PosPerguntas')
        self.pospergunta2_page = PosPerguntas2Page(name='PosPerguntas2')
        self.pospergunta3_page = PosPerguntas3Page(name='PosPerguntas3')
        self.pospergunta4_page = PosPerguntas4Page(name='PosPerguntas4')
        self.pospergunta5_page = PosPerguntas5Page(name='PosPerguntas5')
        self.pospergunta6_page = PosPerguntas6Page(name='PosPerguntas6')
        self.assistentrega_page = AssistEntregaObraPage(name='AssistEntrega')
        self.assistpergunta2_page = AssistPerguntas2Page(name='AssistPerguntas2')
        self.assistpergunta3_page = AssistPerguntas3Page(name='AssistPerguntas3')
        self.assistpergunta4_page = AssistPerguntas4Page(name='AssistPerguntas4')
        self.assistpergunta5_page = AssistPerguntas5Page(name='AssistPerguntas5')
        self.cliente_page = ClientePage(name='Cliente')

        self.manager.add_widget(self.inicial_page)
        self.manager.add_widget(self.email_page)
        self.manager.add_widget(self.login_page)
        self.manager.add_widget(self.obras_page)
        self.manager.add_widget(self.data_avaliacao_page)
        self.manager.add_widget(self.nome_avaliador_page)
        self.manager.add_widget(self.entrega_page)
        self.manager.add_widget(self.pergunta3_page)
        self.manager.add_widget(self.pergunta4_page)
        self.manager.add_widget(self.pergunta5_page)
        self.manager.add_widget(self.pergunta6_page)
        self.manager.add_widget(self.posentrega_page)
        self.manager.add_widget(self.pospergunta_page)
        self.manager.add_widget(self.pospergunta2_page)
        self.manager.add_widget(self.pospergunta3_page)
        self.manager.add_widget(self.pospergunta4_page)
        self.manager.add_widget(self.pospergunta5_page)
        self.manager.add_widget(self.pospergunta6_page)
        self.manager.add_widget(self.cliente_page)
        self.manager.add_widget(self.assistentrega_page)
        self.manager.add_widget(self.assistpergunta2_page)
        self.manager.add_widget(self.assistpergunta3_page)
        self.manager.add_widget(self.assistpergunta4_page)

        for i, pergunta in enumerate(perguntas, start=1):
            page = PerguntaMultiplaEscolhaPage(name=f'PerguntaMultiplaEscolha_{i}', pergunta=pergunta,titulo=titulos[i - 1])
            self.manager.add_widget(page)

        for i, pergunta2 in enumerate(perguntas2, start=1):
            page2 = PerguntasPage(name=f'Pergunta_{i}', pergunta2=pergunta2)
            self.manager.add_widget(page2)

        for i, pergunta3 in enumerate(perguntas3, start=1):
            page3 = AssistPerguntasPage(name=f'AssistPergunta_{i}', pergunta3=pergunta3)
            self.manager.add_widget(page3)

        self.manager.add_widget(self.salvar_dados_page)
        self.manager.add_widget(self.assistpergunta5_page)
        return self.manager

    def on_stop(self):
        self.manager.reset_to_first_page()

if __name__ == '__main__':
    MyApp().run()
