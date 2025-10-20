# Ind-strias-Wayne
Projeto final infinity school


🦇 Sistema de Controle de Acesso — Indústrias Wayne 🏢🔐

Este projeto é um sistema de controle de acesso e gerenciamento de recursos desenvolvido em Python com Flask, utilizando banco de dados SQLite.

Ele permite:

Autenticação de usuários com diferentes permissões (funcionário, gerente e administrador de segurança).

Controle de acesso a áreas restritas com registro de logs.

Cadastro, edição e exclusão de recursos.

Proteção de rotas conforme o nível de acesso do usuário.

🧰 Tecnologias Utilizadas

🐍 Python 3.x

🌐 Flask

🔐 Flask-Login – autenticação de usuários

🧭 Flask-SQLAlchemy – ORM

🧂 bcrypt – hash seguro de senhas

🗄️ SQLite – banco de dados local

🚀 Funcionalidades

✅ Autenticação de Usuários

Registro e login de usuários com diferentes papéis: funcionario, gerente e admin_seguranca.

✅ Controle de Acesso

Áreas restritas com acesso limitado por função.

Registro automático de log de acessos bem-sucedidos ou negados.

✅ Gerenciamento de Recursos

Cadastro de novos recursos (equipamentos, veículos, dispositivos de segurança).

Edição e exclusão de recursos (restrito a administradores).

Listagem de todos os recursos cadastrados.

✅ Proteção de Rotas

Apenas usuários autenticados podem acessar o sistema.

Permissões baseadas no papel do usuário.

🏗️ Estrutura do Projeto
📁 projeto/
│
├── app.py                        # Código principal Flask
├── wayne_security.db             # Banco de dados SQLite
├── requirements.txt              # Dependências do projeto
│
├── 📁 templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── resources.html
│   ├── edit_resource.html
│   └── access_result.html
│
├── 📁 static/
│   └── (arquivos CSS, JS, imagens, favicon)
│
└── README.md                     # Documentação do projeto

⚡ Como Executar o Projeto
1. 📦 Clonar o Repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

2. 🐍 Criar Ambiente Virtual
python -m venv venv
source venv/bin/activate   # Linux ou Mac
venv\Scripts\activate      # Windows

3. 📥 Instalar Dependências

Crie um arquivo requirements.txt com o conteúdo abaixo (ou use o que já tiver):

Flask
Flask-Login
Flask-SQLAlchemy
bcrypt


Depois, instale:

pip install -r requirements.txt

4. 🧱 Inicializar Banco de Dados

O banco de dados será criado automaticamente ao rodar o app pela primeira vez.
Ele cria um usuário admin padrão:

Usuário: admin

Senha: admin123

Papel: admin_seguranca

5. ▶️ Rodar o Servidor
python app.py


Acesse no navegador:

http://127.0.0.1:5000

👮‍♂️ Papéis e Permissões
Papel	Acesso a Áreas Restritas	Gerenciar Recursos	Editar/Excluir Recursos
funcionario	Acesso limitado	❌ Não permitido	❌ Não
gerente	Acesso ampliado	✅ Pode adicionar	❌ Não
admin_seguranca	Acesso total	✅ Pode tudo	✅ Sim
📝 Como Editar Recursos

Vá para Gerenciar Recursos no painel.

Clique em Editar no recurso desejado.

Altere os campos necessários e clique em Salvar Alterações.

Apenas usuários com papel admin_seguranca podem fazer isso.

🧠 Dicas

Use senhas fortes e altere a senha padrão do admin na primeira utilização.

Caso queira usar outro banco de dados (ex: MySQL ou PostgreSQL), basta alterar a URI em:

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wayne_security.db'


Você pode expandir o sistema adicionando logs mais detalhados ou relatórios de acesso.

🧑‍💻 Autor

Desenvolvido por Charlisson Fagundes — FagundAI Tecnologia 💻✨
📅 2025

🛡️ Licença

Este projeto é de uso livre para fins educacionais e pode ser adaptado.
Sinta-se à vontade para modificar e melhorar! 🚀

Quer que eu adicione também no README um passo a passo para implantar online (deploy) — por exemplo, no Render ou Railway? 🌐✨
