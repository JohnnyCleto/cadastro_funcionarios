from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario_mysql'
app.config['MYSQL_PASSWORD'] = 'sua_senha_mysql'
app.config['MYSQL_DB'] = 'empresa'

# Função para estabelecer a conexão com o MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Rota para criar as tabelas "Setor" e "Cargo" no MySQL
@app.route('/criar_tabelas')
def criar_tabelas():
    try:
        conn = conectar_mysql()
        cursor = conn.cursor()

        # Crie a tabela Setor
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL
            )
        ''')

        # Crie a tabela Cargo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cargo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        return "Tabelas Setor e Cargo criadas com sucesso."
    except mysql.connector.Error as err:
        # Lide com erros de banco de dados aqui
        print(f"Erro MySQL: {err}")
        return "Erro ao criar tabelas Setor e Cargo."

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

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        data_de_admissao = request.form['data_de_admissao']
        status_funcionario = request.form['status_funcionario']
        cargo_id = request.form['cargo_id']
        setor_id = request.form['setor_id']
        try:
            conn = conectar_mysql()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO funcionario (nome, sobrenome, data_de_admissao, status_funcionario, cargo_id, setor_id) VALUES (%s, %s, %s, %s, %s, %s)',
                (nome, sobrenome, data_de_admissao, status_funcionario, cargo_id, setor_id))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            # Lide com erros de banco de dados aqui
            print(f"Erro MySQL: {err}")
            return "Erro de banco de dados"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
