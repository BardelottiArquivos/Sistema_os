import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.usuarios.models import Usuario # Verifique se o caminho do seu modelo está correto

def create_superuser():
    username = 'admin'
    email = 'admin@email.com'
    password = 'SuaSenhaForteAqui' # Mude isso depois!

    if not Usuario.objects.filter(username=username).exists():
        Usuario.objects.create_superuser(username, email, password)
        print("Superusuário criado com sucesso!")
    else:
        print("Superusuário já existe.")

if __name__ == '__main__':
    create_superuser()