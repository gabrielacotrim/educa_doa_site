# EducaDoa — Plataforma de Doações Escolares

O **EducaDoa** é uma aplicação web desenvolvida com o framework **Django** que conecta doadores a escolas públicas e instituições de ensino, facilitando o apoio financeiro a campanhas e necessidades educacionais.

---

## Funcionalidades e Arquitetura

### 1. Estruturação MVT (Model-View-Template)

* Organização modular com o projeto principal `educadoa_project` e a aplicação `core`.
* Separação de recursos estáticos e templates nas pastas `static/` e `templates/`.
* Padronização visual através do template matriz `base.html`, gerenciando dinamicamente a navegação (Header e Footer) conforme o estado de autenticação do usuário.

### 2. Modelagem de Dados (SQLite)

* **Usuario:** Custom User Model herdando de `AbstractUser` para controle flexível de perfis e permissões.
* **Escola:** Perfil institucional vinculado ao usuário, identificado por CNPJ e localização.
* **Doador:** Perfil de apoiador identificado por CPF.
* **Necessidade:** Campanhas criadas pelas escolas contendo descrição, meta de arrecadação, valor arrecadado e imagem comprobatória.
* **Doacao:** Registro transacional que vincula o doador à necessidade e atualiza automaticamente o saldo arrecadado.

### 3. Gestão de Mídia e Validações

* Suporte a upload de imagens (`models.ImageField` e `enctype="multipart/form-data"`) armazenadas no diretório `media/`.
* Validação de dados de entrada implementada via `forms.ModelForm` em `core/forms.py`.

---

## Mapa de Rotas e Operações CRUD

| Rota | Descrição | Operação |
| :--- | :--- | :--- |
| `/` | Página inicial com listagem de campanhas em destaque | Read |
| `/cadastro/doador/` e `/cadastro/escola/` | Criação de contas por perfil de acesso | Create |
| `/login/doador/` e `/login/escola/` | Autenticação nativa baseada no papel do usuário | Auth |
| `/escolas/` | Catálogo completo das escolas cadastradas | Read |
| `/dashboard/doador/` e `/dashboard/escola/` | Painéis administrativos de acompanhamento | Read |
| `/necessidade/nova/` | Cadastro de nova campanha pela escola (com upload) | Create |
| `/necessidade/<id>/editar/` | Edição de dados e metas de campanhas existentes | Update |
| `/necessidade/<id>/doar/` | Registro de contribuição financeira e atualização de saldo | Create / Update |

---

## Como Executar o Projeto Localmente

### Pré-requisitos

* Python 3.10 ou superior instalado
* Git

### Passo a passo

1. **Clone o repositório e acesse a pasta do projeto:**

   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd labProgramacao
   ```

2. **Crie e ative o ambiente virtual (`venv`):**
   * **Windows (PowerShell/CMD):**

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

   * **Linux / macOS:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações do banco de dados:**
   *(Caso o arquivo `db.sqlite3` não esteja versionado ou precise ser atualizado)*

   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor de desenvolvimento:**

   ```bash
   python manage.py runserver
   ```

6. **Acesse a aplicação:**
   Abra o navegador em `http://127.0.0.1:8000/`.

### Roteiro Sugerido para Testes

1. Acesse `/cadastro/escola/`, crie uma conta institucional e faça login.
2. No painel da escola, crie uma **Nova Necessidade** anexando uma imagem comprobatória.
3. Encerre a sessão, crie uma conta em `/cadastro/doador/` e faça login.
4. Escolha a campanha criada, realize uma doação e verifique a atualização automática da barra/valor de arrecadação.

---

## Guia de Versionamento e Contribuição (Git/GitHub)

Para manter o repositório limpo, leve e compatível entre diferentes sistemas operacionais (Windows, Linux e macOS), **nunca versione a pasta `venv/` ou arquivos de cache**.

1. **Atualizar dependências:** Sempre que instalar um novo pacote no ambiente virtual ativo, atualize o arquivo de requisitos:

   ```bash
   pip freeze > requirements.txt
   ```

2. **Configuração do `.gitignore`:** Certifique-se de que a raiz do projeto possui um arquivo `.gitignore` contendo no mínimo:

   ```text
   venv/
   __pycache__/
   *.pyc
   db.sqlite3
   media/
   ```

   *(Nota: caso o banco de dados de testes precise ser enviado preenchido para avaliação, `db.sqlite3` e `media/` podem ser removidos temporariamente do `.gitignore`, mantendo `venv/` e `__pycache__/` sempre ignorados).*
