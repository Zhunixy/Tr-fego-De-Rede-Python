import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'proj_dponet'
)

cursor = conexao.cursor()

def login(email:str, senha:str):
    try:
        sql = f'SELECT ID FROM `USER` WHERE EMAIL = "{email}" AND PASSWORD = MD5("{senha}")'
        cursor.execute(sql)
        sql = cursor.fetchall()

        if len(sql) > 0:
            return {'type': 'success', 'mensagem': 'Entrando...', 'id': sql[0][0]}
        else:
            return {'type': 'error', 'mensagem' : 'E-mail ou senha incorreto(s)'}
    except:
        return {'type': 'error', 'mensagem': 'Falha ao efetuar login'}

def cadastro(nome:str, cnpj:str, telefone:str, email:str, senha:str):
    try:
        sql = f'INSERT INTO USER VALUES (NULL, "{nome}", "{cnpj}", "{telefone}", "{email}", MD5("{senha}"))'
        cursor.execute(sql)
        conexao.commit()

        return {'type': 'success', 'mensagem': 'Cadastrado com sucesso'}
    except:
        return {'type': 'error', 'mensagem': 'Falha no cadastro'}

    # cursor.close()
    # conexao.close()