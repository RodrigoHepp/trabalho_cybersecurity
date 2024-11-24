# Trabalho de Cibersegurança

## Descrição

Este projeto foi desenvolvido como parte do trabalho final do curso de Cibersegurança. Ele consiste em desenvolver uma aplicação web segura, implementando os requisitos de autenticação e autorização apresentados em aula conforme detalhamento a seguir.

## Estrutura do Projeto

- `main.py`: [Entry Point do Projeto]
- `requirements.txt`: Lista de dependências necessárias para executar o projeto.
- `website/`: Contém os arquivos HTML, CSS e JavaScript da interface web.

## Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Frameworks**: Flask
- **Banco de Dados**: MySQL

## Dependencias

- Python 3.12.2
- pip 24.0
- MySQL Workbench 8.0 CE

## .env

- SECRET_KEY=sua_senha_secreta_do_flask
- SENHA_DB=sua_senha_de_acesso_do_banco_de_dados
- NOME_BANCO=cybersecurity
- CLIENT_ID=seu_id_de_acesso_da_api_do_oauth_do_google
- CLIENT_SECRET=seu_client_secret_da_api_do_oauth_do_google

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/RodrigoHepp/trabalho_cybersecurity.git
   ```
2. **Navegue até o diretório do projeto**:
   ```bash
   cd trabalho_cybersecurity
   ```
3. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

4. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure o banco de dados:**

- Execute o script sqlcreation.sql no seu SGBD para criar as tabelas necessárias.

6. **OAuth:**

- Ha a necessidade da configuracao da API do google para o funcionamento adequado do OAuth 2.0.

## Uso

1. **Inicie a aplicação**

   ```bash
    python main.py
   ```

2. **Acesse a aplicação:**

- Abra o navegador e vá para http://localhost:5000 (ou a porta configurada)

## Funcionalidades

1. **Autenticação**

- Implementar um fluxo de autenticação stateless utilizando tokens de acesso.
  Usuários devem autenticar-se com e-mail e senha, recebendo um token JWT válido.
- O token deve ser enviado em todas as requisições que exigem autenticação.
  Autorização

2. **Autorização**

- Implementar algum recurso como guards de navegação e autenticação para proteção de rotas no lado do cliente.
- Aplicar algum recurso como gates ou policies para controle de permissões específicas no lado do servidor.

3. **Armazenamento Seguro de Credenciais**

- Utilizar hash seguro para armazenar senhas (bcrypt ou outro algoritmo de segurança).

4. **Manuseio de Tokens**

- Implementar mecanismos para gerenciar a validade e a revogação do token.

5. **OAuth 2.0**

- Integrar um provedor OAuth para login, como Google ou Facebook.

## Exemplos

Somente usuarios com a 'role' admin podem acessar a rota "http://127.0.0.1:5000/adm".
Caso contrario, devem ter sua permissão negada.
