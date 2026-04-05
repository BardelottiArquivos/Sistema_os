SISTEMA DE ORDEM DE SERVIÇO - MANUTENÇÃO DE COMPUTADORES

Sistema web completo para gerenciamento de ordens de serviço em empresas de manutenção de computadores. Desenvolvido com Python/Django e PostgreSQL.

SUMÁRIO

- Sobre o Projeto		(#-sobre-o-projeto)
- Funcionalidades		(#-funcionalidades)
- Tecnologias			(#-tecnologias)
- Pré-requisitos		(#-pré-requisitos)
- Instalação Local		(#-instalação-local)
- Configuração			(#-configuração)
- Docker				(#-docker)
- Deploy				(#-deploy)
- Estrutura do Projeto	(#-estrutura-do-projeto)
- API de CEP			(#-api-de-cep)
- Contribuição			(#-contribuição)
- Licença				(#-licença)
- Autores				(#-autores)


SOBRE O PROJETO

Este sistema foi desenvolvido como projeto acadêmico para automatizar o processo de ordens de serviço em empresas de manutenção de computadores. Ele permite:

- Cadastro completo de clientes (Pessoa Física e Jurídica)
- Gerenciamento de computadores e equipamentos
- Acompanhamento de ordens de serviço
- Dashboard com gráficos e estatísticas
- Geração de relatórios em PDF
- Impressão de documentos
- Consulta automática de endereço via CEP
- Gerenciamento de técnicos


FUNCIONALIDADES

Módulo de Usuários

- Login com diferentes níveis de acesso:
  
    -   Administrador: Acesso total ao sistema
    -   Gerente: Aprovações e relatórios
    -   Técnico: Criação e acompanhamento de OS

Módulo de Clientes

- Cadastro de Pessoa Física e Jurídica
- Consulta automática de endereço via API ViaCEP
- Validação de CPF/CNPJ
- Histórico completo de serviços

Módulo de Computadores

- Cadastro detalhado de equipamentos
- Especificações técnicas completas
- Número de série e patrimônio
- Histórico de manutenções

Módulo de Ordens de Serviço

- Abertura com dados do cliente e computador
- Acompanhamento por status:

    -   Aberta
    -   Em Andamento
    -   Aguardando Peça
    -   Aguardando Cliente
    -   Concluída
    -   Cancelada

- Registro de peças utilizadas
- Cálculo automático de valores

Módulo de Relatórios

- Dashboard com gráficos interativos
- Relatório detalhado por OS (PDF)
- Relatório por período (PDF)
- Impressão direta


TECNOLOGIAS

Backend

| Tecnologia | Versão |      Descrição      |
|------------|--------|---------------------|
| Python     | 3.11   | Linguagem principal |
| Django     | 4.2.7  | Framework web       |
| Django     |        |                     |
| REST       | 3.14.0 | APIs                |
| Framework  |        |                     |
| PostgreSQL | 15     | Banco de dados      |
| Gunicorn   | 21.2.0 | Servidor WSGI       |


Frontend

| Tecnologia | Versão | Descrição       |
|------------|--------|-----------------|
| Bootstrap  | 5.3.2  | Framework CSS   |
| JavaScript | ES6    | Interatividade  |
| Chart.js   |    -   | Gráficos        |
| jQuery     | 3.7.1  | Manipulação DOM |


Infraestrutura

| Tecnologia     | Finalidade      |
|----------------|-----------------|
| Docker         | Containerização |
| Docker Compose | Orquestração    |
| Render         | Deploy em nuvem |
| GitHub Actions | CI/CD           |


PRÉ-REQUISITOS

Antes de começar, você precisa ter instalado:

- Python 3.11      → [Download](https://www.python.org/downloads/)
- PostgreSQL 17    → [Download](https://www.postgresql.org/download/) 
- Git              → [Download](https://git-scm.com/downloads) 
- Docker(opcional) → [Download](https://www.docker.com/products/docker-desktop/) 


INSTALAÇÃO LOCAL

1. Clone o repositório

git clone https://github.com/BardelottiArquivos/sistema-os.git 
cd sistema-os

2. Crie e ative o ambiente virtual

Windows:

python -m venv venv
venv\Scripts\activate

Linux/Mac:

python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Configure o banco de dados

-- Acesse o PostgreSQL
psql -U postgres

-- Crie o banco de dados
CREATE DATABASE sistema;

-- Saia

5. Configure as variáveis de ambiente

Crie um arquivo .env na raiz do projeto:

SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=sistema
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432

6. Execute as migrações

python manage.py makemigrations
python manage.py migrate

7. Crie um superusuário

python manage.py createsuperuser

8. Execute o servidor

python manage.py runserver
Acesse: http://localhost:8000
________________________________________
DOCKER

Construir e executar com Docker Compose

- Construir as imagens
docker-compose build

- Subir os containers
docker-compose up -d

- Ver logs
docker-compose logs -f

- Executar migrações
docker-compose exec web python manage.py migrate

- Criar superusuário
docker-compose exec web python manage.py createsuperuser

 =Parar containers
docker-compose down
Acesse: http://localhost:8000
________________________________________
DEPLOY
Render (Recomendado)
1.	Crie conta em render.com
2.	Conecte seu repositório GitHub
3.	Crie um Web Service com as configurações:
    -   Environment: Docker
    -   Plan: Free
4.	Adicione as variáveis de ambiente
5.	Crie um PostgreSQL (Database)
6.	Deploy automático a cada push

Variáveis de ambiente necessárias no Render:
Variável	Valor
SECRET_KEY	(chave secreta)
DEBUG	False
ALLOWED_HOSTS	seu-app.onrender.com,localhost,127.0.0.1
DB_NAME	sistema
DB_USER	postgres
DB_PASSWORD	(senha do banco)
DB_HOST	(host do banco)
DB_PORT	5432
________________________________________

ESTRUTURA DO PROJETO

sistema_os/
├── manage.py                 # Comandos do Django
├── requirements.txt          # Dependências
├── .env                      # Variáveis de ambiente
├── .gitignore                # Arquivos ignorados
├── Dockerfile                # Containerização
├── docker-compose.yml        # Orquestração
├── core/                     # Configurações principais
│   ├── settings.py           # Configurações do Django
│   ├── urls.py               # Rotas principais
│   └── wsgi.py               # Configuração WSGI
├── apps/                      # Aplicações
│   ├── usuarios/              # App de usuários
│   ├── clientes/              # App de clientes
│   ├── computadores/          # App de computadores
│   ├── ordens_servico/        # App de OS
│   └── relatorios/            # App de relatórios
├── templates/                  # Páginas HTML
├── static/                     # Arquivos estáticos
└── media/                      # Uploads
________________________________________
API DE CEP
O sistema integra com a API ViaCEP para consulta automática de endereços.

Endpoint

GET /clientes/api/consultar-cep/?cep=01001000
Exemplo de resposta
json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "bairro": "Sé",
  "cidade": "São Paulo",
  "estado": "SP"
}
________________________________________
CONTRIBUIÇÃO

1.	Faça um fork do projeto
2.	Crie uma branch (git checkout -b feature/nova-funcionalidade)
3.	Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')
4.	Push para a branch (git push origin feature/nova-funcionalidade)
5.	Abra um Pull Request
________________________________________
LICENÇA
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
________________________________________

👨‍💻 AUTORES

Carlos Bardelotti       Desenvolvedor        @BardelottiArquivos

Fabio Marquês de Paula	Documentação Técnica	

________________________________________

Desenvolvido para o Projeto Integrador III - Univesp

Data de entrega: Abril de 2026
