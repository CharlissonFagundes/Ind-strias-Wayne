from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
from datetime import datetime

# Inicialização do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui_123'  # Substitua por uma chave segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wayne_security.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados e login
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelos do banco de dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='funcionario')  # funcionario, gerente, admin_seguranca

    def __repr__(self):
        return f'<User {self.username}>'

class RestrictedArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    permitted_roles = db.Column(db.String(100))  # ex: 'gerente,admin_seguranca'

    def __repr__(self):
        return f'<RestrictedArea {self.name}>'

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # equipamento, veiculo, dispositivo_seguranca
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    responsible_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    responsible = db.relationship('User', backref='resources')

    def __repr__(self):
        return f'<Resource {self.name}>'

class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('restricted_area.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    authorized = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='access_logs')
    area = db.relationship('RestrictedArea', backref='access_logs')

    def __repr__(self):
        return f'<AccessLog {self.user.username} - {self.area.name}>'

# Carrega usuário para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Função auxiliar para verificar permissões
def is_admin_or_gerente():
    return current_user.is_authenticated and current_user.role in ['gerente', 'admin_seguranca']

# Inicializa o banco e cria usuário admin (executar apenas uma vez)
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        admin = User(username='admin', password_hash=hashed_password, role='admin_seguranca')
        db.session.add(admin)
        # Dados de exemplo
        area1 = RestrictedArea(name='Laboratório Secreto', description='Acesso apenas para gerentes e admins', permitted_roles='gerente,admin_seguranca')
        area2 = RestrictedArea(name='Sala de Controle', description='Acesso para todos', permitted_roles='funcionario,gerente,admin_seguranca')
        db.session.add_all([area1, area2])
        db.session.commit()

# Rotas
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('login.html')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if not username or not password or not role:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe.', 'danger')
            return render_template('register.html')
        if role not in ['funcionario', 'gerente', 'admin_seguranca']:
            flash('Papel inválido.', 'danger')
            return render_template('register.html')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário criado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    areas = RestrictedArea.query.filter(RestrictedArea.permitted_roles.contains(current_user.role)).all()
    return render_template('dashboard.html', areas=areas)

@app.route('/access_area/<int:area_id>')
@login_required
def access_area(area_id):
    area = RestrictedArea.query.get_or_404(area_id)
    authorized = current_user.role in area.permitted_roles.split(',')
    log = AccessLog(user_id=current_user.id, area_id=area.id, authorized=authorized)
    db.session.add(log)
    db.session.commit()
    flash('Acesso registrado com sucesso.', 'success' if authorized else 'danger')
    return render_template('access_result.html', authorized=authorized, area=area)

@app.route('/resources', methods=['GET', 'POST'])
@login_required
def manage_resources():
    if not is_admin_or_gerente():
        flash('Acesso negado: apenas gerentes e administradores podem gerenciar recursos.', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        try:
            resource = Resource(
                type=request.form['type'],
                name=request.form['name'],
                quantity=int(request.form['quantity']),
                description=request.form['description'],
                responsible_id=current_user.id
            )
            db.session.add(resource)
            db.session.commit()
            flash('Recurso adicionado com sucesso!', 'success')
        except ValueError:
            flash('Quantidade inválida. Insira um número válido.', 'danger')
        except Exception as e:
            flash(f'Erro ao adicionar recurso: {str(e)}', 'danger')
        return redirect(url_for('manage_resources'))
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/resources/edit/<int:resource_id>', methods=['GET', 'POST'])
@login_required
def edit_resource(resource_id):
    if current_user.role != 'admin_seguranca':
        flash('Acesso negado: apenas administradores podem editar recursos.', 'danger')
        return redirect(url_for('manage_resources'))
    
    resource = Resource.query.get_or_404(resource_id)
    
    if request.method == 'POST':
        try:
            resource.type = request.form['type']
            resource.name = request.form['name']
            resource.quantity = int(request.form['quantity'])
            resource.description = request.form['description']
            db.session.commit()
            flash('Recurso atualizado com sucesso!', 'success')
            return redirect(url_for('manage_resources'))
        except ValueError:
            flash('Quantidade inválida. Insira um número válido.', 'danger')
        except Exception as e:
            flash(f'Erro ao atualizar recurso: {str(e)}', 'danger')
    
    return render_template('edit_resource.html', resource=resource)

@app.route('/resources/delete/<int:resource_id>', methods=['POST'])
@login_required
def delete_resource(resource_id):
    if current_user.role != 'admin_seguranca':
        flash('Acesso negado: apenas administradores podem excluir recursos.', 'danger')
        return redirect(url_for('manage_resources'))
    
    resource = Resource.query.get_or_404(resource_id)
    try:
        db.session.delete(resource)
        db.session.commit()
        flash('Recurso excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir recurso: {str(e)}', 'danger')
    
    return redirect(url_for('manage_resources'))

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# Executa o aplicativo
if __name__ == '__main__':
    app.run(debug=True)