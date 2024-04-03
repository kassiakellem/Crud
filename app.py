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
        
# RODAR no SHELL /TERMINAL
# db.create_all()

#endpoint ou rota para criar
@app.route("/pessoas", methods=[ 'POST'])
def cadastro(): 
    data = request.get_json()

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

#criação de lista
# retornar o id no /lista GET
@app.route("/pessoas", methods=['GET'])
def lista():
    pessoas = Pessoa.query.all()
    lista = []

    for p in pessoas:
        objeto ={
            "nome": p.nome,
            "telefone": p.telefone,
            "cpf": p.cpf,
            "email": p.email,
            "_id": p._id
        }
        lista.append(objeto)

        # print(p.nome)
    return jsonify(lista)


# rota pra pegar pessoa pelo ID
@app.route("/pessoas/<int:id>", methods=['GET'])
def busca_pessoa(id):
    if id is None:
        return "Faltando parâmetro", 400
    
    p = Pessoa.query.get(id)

    if p:
        objeto ={
            "nome": p.nome,
            "telefone": p.telefone,
            "cpf": p.cpf,
            "email": p.email,
            "_id": p._id
        }
       
        return jsonify(objeto)
    else:
        return jsonify({"mensagem": "Pessoa não encontrada"})

# excluir cliente 
@app.route("/pessoas/<id>", methods=['DELETE'])
def api_delete(id):
    try:
        remove = Pessoa.query.get(id)
        if remove is None: 
            return "item inexistente"
        db.session.delete(remove)
        db.session.commit()
        return jsonify({'sucesso': True})
    except Exception as e: # como se ver mensagem de erro
        print('erro', e) #
        return jsonify({'sucesso': False})

#execução
if __name__ == "__main__":
    app.run(debug=True)
