#instalações:
#pip install google-generativeai
#pip install kiv
#pip install markdown

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder  # Adicionado para carregar o arquivo kv
import google.generativeai as genai
import markdown
import re
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp

GOOGLE_API_KEY = "AIzaSyCrPJDuUObb1q9y3JKci1CGdQQwDffnW3o"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-pro")

class CustomScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 0.6)  # Defina a cor da barra de rolagem aqui
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class CuidadorIdosoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Widget para a pergunta
        pergunta_box = BoxLayout(orientation='vertical', padding=5, spacing=20, size_hint_y=0.4)
        pergunta_label = Label(text="Digite sua dúvida sobre o cuidado com o Idoso:", color=(1, 1, 1, 1))
        self.pergunta_input = TextInput(size_hint_y=0.3)
        pergunta_box.add_widget(pergunta_label)
        pergunta_box.add_widget(self.pergunta_input)
        layout.add_widget(pergunta_box)

        # Widget para a resposta com barra de rolagem
        scroll_view = ScrollView(scroll_type=['bars'], bar_width=10)  # Adicionando barras de rolagem
        resposta_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.resposta_label = Label(text="Resposta:", size_hint_x=1, color=(1, 1, 1, 1), valign='top')
        self.resposta_label.text_size = (Window.width - dp(20), None)  # Definir text_size para largura da janela
        self.resposta_label.bind(texture_size=self._update_label_height)  # Atualizar altura conforme o conteúdo
        resposta_layout.add_widget(self.resposta_label)
        scroll_view.add_widget(resposta_layout)
        layout.add_widget(scroll_view)

        botao_enviar = Button(text="Enviar", background_color=(0, 0.7, 0, 1), size_hint_y=0.1)  # Cor verde para o botão
        botao_enviar.bind(on_press=self.enviar_pergunta)
        layout.add_widget(botao_enviar)

        return layout

    def _update_label_height(self, instance, size):
        # Atualizar a altura do layout de resposta para corresponder ao tamanho do Label
        resposta_layout = self.resposta_label.parent
        resposta_layout.height = size[1]

    def enviar_pergunta(self, instance):
        pergunta = self.pergunta_input.text.strip()
        if pergunta:
            resposta = self.obter_resposta_ia(pergunta)
            texto_completo = f"Pergunta: {pergunta}\n\nResposta: {resposta}"
            self.resposta_label.text = texto_completo
        else:
            self.resposta_label.text = "Por favor, digite uma pergunta."

        self.pergunta_input.text = ""

    def obter_resposta_ia(self, pergunta):
        """Obtém a resposta da IA, converte Markdown para texto simples e ajusta o espaçamento."""
        response = model.generate_content(pergunta)
        texto_html = markdown.markdown(response.text)
        texto_simples = re.sub('<[^<]+?>', '', texto_html)  # Remove as tags HTML
        texto_formatado = re.sub(r'\n+', '\n', texto_simples)  # Remove linhas em branco extras
        return texto_formatado

#Builder.load_file("scrollview.kv")  # Carregar o arquivo kv

if __name__ == "__main__":
    CuidadorIdosoApp().run()