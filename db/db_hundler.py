import psycopg2
from psycopg2 import sql
from datetime import datetime


class DBHandler:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect_db(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            print("[DEBUG] Conexão com o banco de dados estabelecida com sucesso.")
            return conn
        except Exception as e:
            print(f"[ERROR] Erro ao conectar no banco de dados: {e}")
            return None

    def insert_data(self, conn, data):
        try:
            with conn.cursor() as cursor:
                insert_query = sql.SQL(
                    """
                    UPDATE calibration
                    SET maintance_last_date = %s,
                        maintance_next_event = %s,
                        maintance_next_date = %s
                    WHERE line = %s
                    """
                )

                print(f"[DEBUG] Dados recebidos para inserção: {data}")

                if len(data) != 4:
                    raise ValueError(f"[ERROR] Esperado 4 elementos em 'data', mas recebeu: {
                                     len(data)}: {data} ")

                # converter strings de dara para timestamps
                last, next_data, next_event, filtro = data
                last = datetime.strptime(
                    last, '%Y%m%d%H%M%S') if last else None
                next_data = datetime.strptime(
                    next_data, '%Y%m%d%H%M%S') if next_data else None

                print("[DEBUG] Executando query de atualização com dados:",
                      (last, next_data, next_event, filtro))
                cursor.execute(
                    insert_query, (last, next_event, next_data, filtro))
            conn.commit()
            print("[DEBUG] Dados inseridos com sucesso no banco de dados.")
        except Exception as e:
            print(f"[ERROR] Erro ao inserir dados no banco de dados: {e}")
            conn.rollback()
