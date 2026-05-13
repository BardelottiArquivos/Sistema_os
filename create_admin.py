import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.usuarios.models import Usuario

def create_superuser():
    username = 'admin2'
    email = 'admin@email.com'
    password = 'admin12345678'  # A senha que você tentou usar no login
    
    if not Usuario.objects.filter(username=username).exists():
        Usuario.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superusuário '{username}' criado com sucesso!")
        print(f"📧 Email: {email}")
        print(f"🔑 Senha: {password}")
    else:
        print(f"⚠️ Superusuário '{username}' já existe.")
        print("Tente fazer login diretamente ou use outro nome de usuário.")

if __name__ == '__main__':
    create_superuser()