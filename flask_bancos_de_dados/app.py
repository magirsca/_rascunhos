from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'  # Chave secreta para proteger formulários
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'  # Usando SQLite como banco de dados

db = SQLAlchemy(app)


# Modelo de dados para as tarefas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Formulário para adicionar tarefas
class TaskForm(FlaskForm):
    content = StringField('Tarefa', validators=[DataRequired()])
    submit = SubmitField('Adicionar')

@app.route('/')
def index():
    tasks = Task.query.all()
    form = TaskForm()
    return render_template('index.html', tasks=tasks, form=form)

@app.route('/add_task', methods=['POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task_content = form.content.data
        new_task = Task(content=task_content, created_at=datetime.now())  # Use datetime.now() para obter a data/hora atual
        db.session.add(new_task)
        db.session.commit()
        flash('Tarefa adicionada com sucesso!', 'success')
    else:
        flash('Falha ao adicionar tarefa. Certifique-se de preencher o campo.', 'danger')
    return redirect(url_for('index'))

@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm()
    if form.validate_on_submit():
        task.content = form.content.data
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.content.data = task.content
    return render_template('update_task.html', form=form, task=task)

@app.route('/delete_task/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)