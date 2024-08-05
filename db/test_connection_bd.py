import psycopg2

from psycopg2 import OperationalError


def create_connection():
    host = '10.58.64.199'
    database = 'iotf2'
    user = 'postgres'
    password = 'icct@2023'
    port = 5432

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("conexão com o banco de dados estabelecida com sucesso.")
        return connection
    except OperationalError as e:
        print(f" Erro ao conectar ao banco de dados: {e}")
        return None


if __name__ == "__main__":
    conn = create_connection()
    if conn:
        # feche a conexão após o teste
        conn.close()
        print("Conexão fechada com sucesso. ")
