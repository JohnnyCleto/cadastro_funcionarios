import mysql.connector
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'User'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'empresa'

mydb = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'])


@app.route('/funcionario', methods=['GET'])
def get_funcionario():
    my_cursor = mydb.cursor()

    query = '''
        SELECT funcionário.id, funcionário.nome, funcionário.sobrenome, funcionário.data_de_admissão, 
        funcionário.status_funcionário, setor.nome AS setor, cargo.nome AS cargo
        FROM funcionário
        LEFT JOIN setor ON funcionário.setor_id = setor.id
        LEFT JOIN cargo ON funcionário.cargo_id = cargo.id;
        '''

    my_cursor.execute(query)
    funcionarios = my_cursor.fetchall()

    return render_template('index.html', funcionarios=funcionarios)  # Passando funcionarios para o template HTML


@app.route('/adicionar_funcionario', methods=['POST'])
def adicionar_funcionario():
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    cargo = request.form['cargo']
    setor = request.form['setor']
    data_de_admissao = request.form['data_de_admissao']
    status_funcionario = 1 if 'status_funcionario' in request.form else 0  # Verifique se o checkbox está marcado

    my_cursor = mydb.cursor()

    setor_data = (setor,)
    setor_insert_query = 'INSERT INTO setor (nome) VALUES (%s)'
    my_cursor.execute(setor_insert_query, setor_data)
    setor_id = my_cursor.lastrowid

    cargo_data = (cargo, setor_id)
    cargo_insert_query = 'INSERT INTO cargo (nome, setor_id) VALUES (%s, %s)'
    my_cursor.execute(cargo_insert_query, cargo_data)
    cargo_id = my_cursor.lastrowid

    funcionario_data = (nome, sobrenome, data_de_admissao, status_funcionario, cargo_id, setor_id)
    funcionario_insert_query = 'INSERT INTO funcionário (nome, sobrenome, data_de_admissão, status_funcionário, cargo_id, setor_id) VALUES (%s, %s, %s, %s, %s, %s)'
    my_cursor.execute(funcionario_insert_query, funcionario_data)

    mydb.commit()
    my_cursor.close()

    return redirect('/funcionario')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')