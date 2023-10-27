from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'MYSQL_USER'
app.config['MYSQL_PASSWORD'] = 'MYSQL_PASSWORD'
app.config['MYSQL_DB'] = 'empresa'


# Função para estabelecer a conexão com o MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
        )


@app.route('/adicionar_funcionario', methods=['GET', 'POST'])
def adicionar_funcionario():
    if request.method == 'GET':
        try:
            conn = conectar_mysql()
            cursor = conn.cursor()

            conn.commit()
            cursor.close()
            conn.close()
            return "Tabelas Setor e Cargo criadas com sucesso."
        except mysql.connector.Error as err:
            # Lide com erros de banco de dados aqui
            print(f"Erro MySQL: {err}")
            return "Erro ao criar tabelas Setor e Cargo."
    elif request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        data_de_admissão = request.form.get('data_de_admissão')
        status_funcionário = request.form.get('status_funcionario')
        cargo_id = request.form.get('cargo_id')
        setor_id = request.form.get('setor_id')

        try:
            conn = conectar_mysql()
            cursor = conn.cursor()

            # Use uma transação para garantir a consistência dos dados
            cursor.execute('START TRANSACTION')

            # Inserir dados na tabela funcionário
            cursor.execute(
                'INSERT INTO funcionário (nome, sobrenome, data_de_admissão, status_funcionário, cargo_id, setor_id) VALUES (%s, %s, %s, %s, %s, %s)',
                (nome, sobrenome, data_de_admissão, status_funcionário, cargo_id, setor_id)
            )
            # Buscar o nome do cargo da tabela "cargo" com base no ID
            if cargo_id is not None:
                cursor.execute('SELECT nome FROM cargo WHERE id = %s', (cargo_id,))
                cargo_id = cursor.fetchone()[0]
            else:
                cargo_id = None

            # Buscar o nome do setor da tabela "setor" com base no ID
            if setor_id is not None:
                cursor.execute('SELECT nome FROM setor WHERE id = %s', (setor_id,))
                setor_id = cursor.fetchone()[0]
            else:
                setor_id = None
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            # Lide com erros de banco de dados aqui
            print(f"Erro MySQL: {err}")
            return "Erro de banco de dados"
        return redirect(url_for('index'))

@app.route('/')
def index():
    try:
        conn = conectar_mysql()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.id, f.nome, f.sobrenome, f.data_de_admissão, f.status_funcionário, c.nome AS cargo, s.nome AS setor
            FROM funcionário f
            LEFT JOIN cargo c ON f.cargo_id = c.id
            LEFT JOIN setor s ON f.setor_id = s.id
         ''')
        funcionarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', funcionarios=funcionarios)
    except mysql.connector.Error as err:
        # Lide com erros de banco de dados aqui
        print(f"Erro MySQL: {err}")
        return "Erro de banco de dados"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')