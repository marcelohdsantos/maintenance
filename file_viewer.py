import os
from watchdog.events import PatternMatchingEventHandler
from utils import processar_arquivo, extrair_dados, extrair_datas, calcula_hash_arquivo
from db.db_hundler import DBHandler


class EventHandler(PatternMatchingEventHandler):
    def __init__(self, padroes, diretorio_filtros, db_config):
        super().__init__(patterns=padroes)
        self.diretorio_filtros = diretorio_filtros
        self.db_handler = DBHandler(db_config)
        self.hash_anterior = {}

    def processa_evento(self, event):
        print(f"[DEBUG] Evento detectado: {
              event.event_type} - {event.src_path}")
        if not event.is_directory:
            arquivo_monitorado = self.diretorio_filtros.get(event.src_path)
            if arquivo_monitorado:
                print(f"[DEBUG] Evento válido para processamento: {
                      event.src_path}")
                try:
                    filtro = self.diretorio_filtros.get(event.src_path)
                    if filtro:
                        novo_hash = calcula_hash_arquivo(event.src_path)
                        hash_anterior = self.hash_anterior.get(event.src_path)

                        print(f"[DEBUG] Novo hash: {
                              novo_hash}, Hash anterior: {hash_anterior}")

                        if novo_hash != hash_anterior:
                            self.hash_anterior[event.src_path] = novo_hash
                            print(f"[DEBUG] O arquivo {
                                event.src_path} foi realmente alterado, processando com filtro {filtro}...")
                            base_path = os.path.dirname(
                                os.path.abspath(__file__))
                            filtro_dir = os.path.join(base_path, filtro)
                            os.makedirs(filtro_dir, exist_ok=True)
                            caminho_arquivo_copia = os.path.join(
                                filtro_dir, 'copia_' + os.path.basename(event.src_path))

                            print(f"[DEBUG] Caminho do arquivo original: {
                                event.src_path}")
                            print(f"[DEBUG] Caminho do arquivo de cópia: {
                                caminho_arquivo_copia}")

                            ultima_manutencao = processar_arquivo(
                                event.src_path, caminho_arquivo_copia, filtro)

                            dados = extrair_dados(caminho_arquivo_copia)
                            resultados = extrair_datas(dados, filtro)

                            conn = self.db_handler.connect_db()

                            if conn:
                                print(
                                    "[DEBUG] Conexão com o banco de dados estabelecida.")
                                for resultado in resultados:
                                    # Preparar os dados para a atualização
                                    data_to_update = (
                                        # last: data da última manutenção
                                        ultima_manutencao,
                                        # next_event: duração da próxima manutenção
                                        resultado[2],
                                        # next: data da próxima manutenção
                                        resultado[3],
                                        # filtro: linha (line) correspondente no banco de dados
                                        filtro
                                    )
                                    print(f"[DEBUG] Atualizando dados: {
                                          data_to_update}")
                                    self.db_handler.update_data(
                                        conn, data_to_update)
                                conn.close()
                                print(
                                    "[DEBUG] Conexão com o banco de dados fechada.")

                            for resultado in resultados:
                                print(f"[RESULT] Data atual de manutenção: {resultado[0]}, Duração da manutenção: {
                                    resultado[1]}, Próxima data de manutenção: {resultado[2]}, Última data de manutenção: {resultado[4]}")

                            if ultima_manutencao:
                                print(f"[RESULT] Última manutenção para filtro {
                                    filtro}: {ultima_manutencao}")
                        else:
                            print(f"[DEBUG] O arquivo {
                                  event.src_path} não teve mudanças reais no conteúdo.")
                except Exception as e:
                    print(f"[ERROR] Erro ao processar o arquivo {
                          event.src_path}: {e}")
            else:
                print(
                    f"[DEBUG] {event.src_path} não está na lista de arquivos monitorados.")

    def on_modified(self, event):
        print(f"[DEBUG] Evento on_modified chamado para: {event.src_path}")
        self.processa_evento(event=event)

    def on_created(self, event):
        print(f"[DEBUG] Evento on_created chamado para: {event.src_path}")
        self.processa_evento(event=event)

    def on_deleted(self, event):
        print(f"[DEBUG] Evento on_deleted chamado: {event.src_path}")
        self.processa_evento(event=event)
