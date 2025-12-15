# 🧠 MVP Arquitetura de Software – Backend

Bem-vinda(o) ao repositório do **MVP Arquitetura de Software – Backend**!  

Essa API tem como objetivo fornecer endpoints para registro e gerenciamento de um **diário de introdução alimentar**, permitindo armazenar, consultar e organizar entradas relacionadas à alimentação do bebê e também realizar a busca de receitas.

Ele se comunica com o frontend Lit através de REST, com toda a aplicação rodando em containers independentes via Docker.

> **Cenário implementado: Cenário 1.1**
---
## 📊 Fluxograma

<img width="800" height="382" alt="image" src="https://github.com/user-attachments/assets/e20f2030-9094-47c0-9a11-b66c44dee8ad" />


---

## ✨ Tecnologias Utilizadas

### 🔹 Python 3.13 
https://docs.python.org/3.13/

### 🔹 Flask
https://flask.palletsprojects.com/en/stable/

### 🔹 SQLAlchemy  
https://docs.sqlalchemy.org/en/20/

### 🔹 OpenAPI3
https://swagger.io/specification/

### 🔹 SQLite
https://www.sqlite.org/docs.html

### 🔹 Docker 🐳   
https://docs.docker.com/

---

## 🛠️ Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- **Docker** (para rodar o projeto em containers) → https://docs.docker.com/
- **Docker Compose** (geralmente incluso no Docker Desktop)

---

### 🔌 Comunicação com o Frontend

A comunicação entre o frontend e este backend é feita através de uma API REST, utilizando requisições HTTP e respostas em formato JSON.

## 📡 Padrões adotados

Base URL: http://localhost:5000

Formato de dados: JSON

Métodos HTTP: GET, POST, PUT, DELETE

Status Codes seguindo o padrão REST 

## 🧩 Integração com o Frontend

O frontend é responsável por:

Consumir os endpoints da API

Enviar dados de formulários

Exibir dados retornados pela API

---

## ▶️ Como Rodar o Projeto 

### 🔹 Clonar o repositório
   ```bash
   git clone https://github.com/brufonseca/mvp-arq-backend.git
   cd mvp-arq-backend
   ```

### 🔹 Configurando variáveis de ambiente

Este projeto utiliza variáveis de ambiente para configurar chaves de API

1. Faça uma cópia do arquivo .env.template:
  ```bash
  cp .env.template .env
  ```
2. Abra o arquivo .env e informe as chaves de API (SPOONACULAR_API_KEY, GOOGLE_TRANSLATE_API_KEY)


### 💻 Execução em Modo de Desenvolvimento

Na raiz do repositório:

**Criar e ativar um ambiente virtual**:

    ````bash
    python -m venv env
    source env/bin/activate  #  Linux ou Mac
    venv\Scripts\activate     #  Windows


**Instalar as dependências**:

    ````bash
    pip install -r requirements.txt

**Executar a aplicação**:

    ````bash
    flask run --host 0.0.0.0 --port 5000


Acesse no navegador:
👉 http://localhost:5000


### 🐳 Docker

### 🔹 Rodando apenas o Backend com Docker

**Os comandos a seguir devem ser executados na raiz do repositório e com privilégios de administrador ou usuário pertencente ao grupo docker**

Construção da imagem Docker
   ```bash
   docker build -t mvp-arq-backend .  
   ```

Execução do container
   ```bash
   docker run -p 5000:5000 mvp-arq-backend
   ```

Acesse no navegador:
👉 http://localhost:5000/


### 🐳 Docker Compose (Frontend + Backend)

Um arquivo **docker-compose.yml** está disponível na raiz do repositório do frontend, responsável por subir **tanto o frontend quanto o backend** juntos.  
Isso facilita o desenvolvimento e garante que os dois serviços conversem corretamente dentro da mesma rede Docker.

Repositório do Frontend:
👉 https://github.com/brufonseca/mvp-arq-frontend



