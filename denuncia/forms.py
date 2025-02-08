from django import forms
from .models import Denuncia
import os

def carregar_palavras_ofensivas(arquivo):
    """Lê o arquivo e retorna uma lista de palavras ofensivas."""
    with open(arquivo, 'r', encoding='utf-8') as f:
        palavras = [linha.strip().lower() for linha in f.readlines()]
    return palavras

PALAVRAS_OFENSIVAS = carregar_palavras_ofensivas('denuncia/palavras.txt')

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['titulo', 'descricao', 'local', 'fotos']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Título da denúncia',
                'class': 'form-control'
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Descrição detalhada',
                'class': 'form-control',
                'rows': 3 
            }),
            'local': forms.TextInput(attrs={
                'placeholder': 'Local do incidente',
                'class': 'form-control'
            }),
            'fotos': forms.FileInput(attrs={
                'class': 'form-control-file',
                'required': False
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        titulo = cleaned_data.get('titulo')
        descricao = cleaned_data.get('descricao')
        local = cleaned_data.get('local')

        if not titulo:
            self.add_error('titulo', 'Este campo é obrigatório.')
            print(os.getcwd())
        elif len(titulo) < 7:
            self.add_error('titulo', 'O título deve ter pelo menos 7 letras.')
        elif self.contem_palavras_ofensivas(titulo):
            self.add_error('titulo', 'O título contém palavras não permitidas.')

        if not local:
            self.add_error('local', 'Este campo é obrigatório.')
        elif len(local) < 5:
            self.add_error('local', 'O local deve ter pelo menos 10 letras.')
        elif self.contem_palavras_ofensivas(local):
            self.add_error('local', 'O local contém palavras não permitidas.')

        if not descricao:
            self.add_error('descricao', 'Este campo é obrigatório.')
        elif len(descricao) < 20:
            self.add_error('descricao', 'A descrição deve ter pelo menos 25 letras.')
        elif self.contem_palavras_ofensivas(descricao):
            self.add_error('descricao', 'A descrição contém palavras não permitidas.')

    def contem_palavras_ofensivas(self, texto):
        """Verifica se o texto contém palavras ofensivas."""
        for palavra in PALAVRAS_OFENSIVAS:
            if palavra in texto.lower():
                return True
            if palavra in texto.upper():
                return True
        return False

    def clean_fotos(self):
        photo = self.cleaned_data.get('fotos')
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        max_file_size = 50 * 1024 * 1024

        if photo:
            ext = os.path.splitext(photo.name)[1][1:].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Formato inválido: {photo.name}. Os tipos permitidos são: {', '.join(allowed_extensions)}")
            if photo.size > max_file_size:
                raise forms.ValidationError(f"O arquivo {photo.name} é maior que 50 MB.")
        
        return photo
