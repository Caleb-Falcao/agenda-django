from django import forms
from django.core.exceptions import ValidationError
from . import models

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a classe-b',
                'placeholder':'Aqui veio do init',
            }
        ),
        label='Primeiro Nome',
        help_text='Texto de ajuda para seu usuário'
    )
    
    class Meta:
        
        model = models.Contact
        fields = (
            'first_name','last_name','phone',
            )
        #widgets = {
        #    'first_name': forms.TextInput(
        #        attrs={
        #            'class':'classe'
        #        }
        #    )
        #}

    def clean(self):
        #cleaned_data = self.cleaned_data

        #self.add_error(
        #    None,
        #    ValidationError(
        #        'Mensagem de erro',
        #        code='invalid'
        #    )                
        #)

       
       
        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == 'admin':
            self.add_error(
                'first_name',
                ValidationError(
                    'Nome não pode ser admin',
                    code='invalid'
                )  
            )
        
        return first_name
