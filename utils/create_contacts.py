import os  # Importa o módulo os para interagir com o sistema operacional
import sys  # Importa o módulo sys para manipular o caminho do sistema
from datetime import datetime  # Importa datetime para manipulação de datas
from pathlib import Path  # Importa Path da biblioteca pathlib para manipulação de caminhos de arquivos
from random import choice  # Importa choice para selecionar aleatoriamente um item de uma lista

import django  # Importa o Django
from django.conf import settings  # Importa as configurações do Django

# Define o diretório base do projeto Django
DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000  # Define o número de objetos a serem criados

# Adiciona o diretório base do Django ao sys.path
sys.path.append(str(DJANGO_BASE_DIR))
# Define a variável de ambiente DJANGO_SETTINGS_MODULE para o arquivo de configurações do projeto
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
# Desativa o uso de timezones nas configurações do Django
settings.USE_TZ = False

# Configura o Django
django.setup()

if __name__ == '__main__':
    import faker  # Importa a biblioteca faker para gerar dados falsos

    from contact.models import Category, Contact  # Importa os modelos Category e Contact

    # Deleta todos os registros das tabelas Contact e Category
    Contact.objects.all().delete()
    Category.objects.all().delete()

    fake = faker.Faker('pt_BR')  # Inicializa o faker para gerar dados em português do Brasil
    categories = ['Amigos', 'Família', 'Conhecidos']  # Define uma lista de categorias de exemplo

    # Cria instâncias de Category para cada nome na lista categories
    django_categories = [Category(name=name) for name in categories]

    # Salva cada categoria no banco de dados
    for category in django_categories:
        category.save()

    django_contacts = []  # Inicializa uma lista para armazenar os contatos falsos

    # Cria perfis falsos e instâncias de Contact
    for _ in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()  # Gera um perfil falso
        email = profile['mail']  # Extrai o email do perfil
        first_name, last_name = profile['name'].split(' ', 1)  # Extrai o primeiro e último nome do perfil
        phone = fake.phone_number()  # Gera um número de telefone falso
        created_date: datetime = fake.date_this_year()  # Gera uma data de criação falsa
        description = fake.text(max_nb_chars=100)  # Gera uma descrição falsa com no máximo 100 caracteres
        category = choice(django_categories)  # Seleciona aleatoriamente uma categoria

        # Adiciona uma instância de Contact à lista django_contacts
        django_contacts.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                created_date=created_date,
                description=description,
                category=category,
            )
        )

    # Insere os contatos em massa no banco de dados
    if len(django_contacts) > 0:
        Contact.objects.bulk_create(django_contacts)
