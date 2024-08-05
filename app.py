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
    diretorio_filtros = {
        # r'C:\\Users\\bc2g8585\\Desktop\\teste_iot\\Line1\\maintenanceCommand.txt': 'S1',
        # r'C:\\Users\\bc2g8585\\Desktop\\teste_iot\\Line2\\maintenanceCommand.txt': 'S2',
        r'\\10.58.141.21\\d\\setup_lineS1\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S1',
        # r'\\10.58.141.22\\d\\setup-lineS2\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S2',
        # r'\\10.58.141.23\\d\\setup-lineS3\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S3',
        # r'\\10.58.141.24\\d\\setup-lineS4\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S4',
        # r'\\10.58.141.25\\d\\setup-lineS5\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S5',
        # r'\\10.58.141.26\\d\\setup_lineS6\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S6',
        # r'\\10.58.141.27\\SetupL7\\iotsoftware\\SMT_Center_LogAnalyzer\\maintenanceCommand.txt': 'S7'
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

    # Processar os arquivos inicialmente
    processar_inicialmente(diretorio_filtros, db_config)

    padroes = ["*maintenanceCommand.txt"]
    observers = []

    for diretorio in set(os.path.dirname(arquivo) for arquivo in diretorio_filtros.keys()):
        try:
            print(f"[DEBUG] Configurando monitoramento para o diretório: {
                  diretorio}")
            event_handler = EventHandler(padroes, diretorio_filtros, db_config)
            observer = Observer()
            observer.schedule(event_handler, path=diretorio, recursive=False)
            observers.append(observer)
            print(f"[DEBUG] Monitoramento iniciado para o diretório: {
                  diretorio}")
        except Exception as e:
            print(f"[ERROR] Erro ao configurar o monitoramento para o diretório {
                  diretorio}: {e}")

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
