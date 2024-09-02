import time
import os
from watchdog.observers import Observer
from file_viewer import EventHandler
from utils import processar_inicialmente
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do banco de dados usando variáveis de ambiente
db_config = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT'),
    'options': os.getenv('OPTIONS')
}

if __name__ == '__main__':
    # mapear os diretórios para filtrar
    # diretorio_filtros = {
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S1',
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S2',
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S3',
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S4',
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S5',
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S6',
    #     r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S7',
    # }

    diretorio_filtros = {
        r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
    }

    # verificar e normalizar os caminhos dos arquivos
    normalized_diretorios_filtros = {}

    for path, filtro in diretorio_filtros.items():
        if isinstance(path, (str, bytes, os.PathLike)) and path:
            normalized_path = os.path.normpath(path)
            normalized_diretorios_filtros[normalized_path] = filtro
        else:
            print(f"[ERROR] Caminho inválido detectado: {path}")

    diretorio_filtros = normalized_diretorios_filtros

    for path in diretorio_filtros.keys():
        if not isinstance(path, (str, bytes, os.PathLike)) or not path:
            raise ValueError(f"O caminho '{path}' não é valido.")

    for path, filtros in diretorio_filtros.items():
        for filtro in filtros:
            # Processar os arquivos inicialmente
            processar_inicialmente({path: filtro}, db_config)

    padroes = ["*maintenanceCommand.txt"]
    observers = []

    for path, filtros in diretorio_filtros.items():
        for filtro in filtros:
            try:
                print(f"[DEBUG] Configurando monitoramento para o diretório: {
                      os.path.dirname(path)} com o filtro: {filtro}")
                event_handler = EventHandler(
                    padroes, {path: filtro}, db_config)
                observer = Observer()
                observer.schedule(
                    event_handler, path=os.path.dirname(path), recursive=False)
                observers.append(observer)
                print(f"[DEBUG] Monitoramento iniciado para o diretório: {
                      os.path.dirname(path)} com o filtro: {filtro}")
            except Exception as e:
                print(f"[ERROR] Erro ao configurar o monitoramento para o diretório {
                      os.path.dirname(path)} com o filtro: {filtro}: {e}")

    try:
        for observer in observers:
            observer.start()
            print(
                f"[DEBUG] Monitoramento iniciado para o diretório: {observer}")

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
    except Exception as e:
        print(f"[ERROR] Erro durante o monitoramento: {e}")
    finally:
        for observer in observers:
            observer.join()
            print(
                f"[DEBUG] Monitoramento finalizado para o diretório: {observer}")
