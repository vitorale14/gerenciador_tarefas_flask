# Imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuração do aplicativo
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projeto.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class MinhaTarefa(db.Model):
    identificador = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(100), nullable=False)
    completar = db.Column(db.Integer, default=0)
    criado = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tarefa {self.identificador}>"

# Cria as tabelas do banco(se não existirem)
with app.app_context():
        db.create_all()

# Rota principal - READ e CREATE
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conteudo = request.form.get("conteudo")
        if conteudo:
            nova_tarefa = MinhaTarefa(conteudo=conteudo)
            try:
                db.session.add(nova_tarefa)
                db.session.commit()
            except Exception as e:
                print(f"Erro ao adicionar tarefa: {e}")
    tarefas = MinhaTarefa.query.order_by(MinhaTarefa.criado).all()
    return render_template("index.html", tarefas=tarefas)

# DELETE - Apaga a tarefa criada
@app.route("/delete/<int:id>")
def delete(id):
    tarefa = MinhaTarefa.query.get_or_404(id)
    try:
        db.session.delete(tarefa)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Erro ao deletar: {e}"

# EDIT - Edita a tarefa criada
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    tarefa = MinhaTarefa.query.get_or_404(id)
    if request.method == "POST":
        conteudo = request.form.get('conteudo')
        if conteudo:
            tarefa.conteudo = conteudo
            try:
                db.session.commit()
                return redirect("/")
            except Exception as e:
                return f"Erro ao editar: {e}"
    return render_template('edit.html', tarefa=tarefa)


# UPDATE - GET exibe form, POST atualiza
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    tarefa = MinhaTarefa.query.get_or_404(id)
    if request.method == "POST":
        conteudo = request.form.get("conteudo")
        if conteudo:
            tarefa.conteudo = conteudo
            try:
                db.session.commit()
                return redirect("/")
            except Exception as e:
                return f"Erro ao atualizar: {e}"
    return render_template("update.html", tarefa=tarefa)
    

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)