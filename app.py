from flask import Flask, jsonify, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)


# criação de tabela e colunas (modelo)
class Pessoa(db.Model):
    __tablename__ = "cliente"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)
    
    # db.Model construtor DEFAULT
    # def __init__(self):
    #     pass

    #__init__ sempre se cria um objeto da class
    def __init__(self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email
    
#identação é o formato do codigo
# exemplo em JS: 
# while(true){
#     if(True){
#         break;
#     }
# }
# exemplo em python:
# while True:
#     if True:
#         break
    
# RODAR no SHELL /TERMINAL
# db.create_all()


# criação de rotas e função.
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

#endpoint ou rota para criar
@app.route("/pessoa", methods=[ 'POST'])
def cadastro(): 
    data = request.get_json()
    print(data)
    if 'nome' in data and 'telefone' in data and 'cpf' in data and 'email' in data:
        nome = data['nome']
        telefone = data['telefone']
        cpf = data['cpf']
        email = data['email']
    else:
        return "Dados incompletos", 400

    
    #criação de usuario no banco de dados  
    if nome and telefone and cpf and email:
        p = Pessoa(nome, telefone, cpf, email)
        db.session.add(p)
        db.session.commit()
    else:
        return "Dados invalidos", 400

    return "Dados recebidos com sucesso"

##  DELETAR DEPOIS
# 1- criar outra funcao de recuperar um unico cliente
    # pesquisar como se passa um id de um cliente para o flask
    # usar a mesma linha de raciocionio do /Lista

#criação de lista
@app.route("/lista", methods=['GET'])
def lista():
    pessoas = Pessoa.query.all()
    lista = []

    for p in pessoas:
        objeto ={
            "nome": p.nome,
            "telefone": p.telefone,
            "cpf": p.cpf,
            "email": p.email
        }
        lista.append(objeto)

        # print(p.nome)
    return jsonify(lista)

#criação de excluir cliente 
#assim que for excluindo, a pagina lista vai ser atualiza com a informação excluida.
# retornar o id no /lista GET
# Usar método DELETE
# Usar o postman para deletar
# verificar se deletou pela lista
@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
 
    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)

#execução
if __name__ == "__main__":
    app.run(debug=True)
