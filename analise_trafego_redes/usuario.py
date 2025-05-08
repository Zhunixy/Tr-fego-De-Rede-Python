import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'proj_dponet'
)

cursor = conexao.cursor()

def login(email, senha):
    try:
        sql = f'SELECT ID FROM `USER` WHERE EMAIL = "{email}" AND PASSWORD = "{senha}"'
        cursor.execute(sql)
        sql = len(cursor.fetchall())

        if sql > 0:
            return {'type': 'success', 'mensagem': 'Entrando...'}
        else:
            return {'type': 'error', 'mensagem' : 'Emal ou senha incorreto(s)'}
    except:
        return {'type': 'error', 'mensagem': 'Falha ao efetuar login'}

    # cursor.close()
    # conexao.close()