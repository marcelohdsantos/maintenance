import shutil
import os
import hashlib
from db.db_hundler import DBHandler


def calcula_hash_arquivo(caminho):
    hasher = hashlib.md5()
    with open(caminho, 'rb') as arquivo:
        while chunk := arquivo.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def processar_arquivo(arquivo_origem, arquivo_destino, filtro):
    try:
        shutil.copy(arquivo_origem, arquivo_destino)
        print(f"[DEBUG] Cópia do arquivo {arquivo_origem} para {
              arquivo_destino} criada com sucesso.")

        with open(arquivo_origem, 'r') as file:
            conteudo = file.read()
        print(f"[DEBUG] Conteúdo do arquivo {
              arquivo_origem} lido com sucesso.")

        conteudo = conteudo.replace("DELETE FROM table_maintenancedate2;", "")
        conteudo = conteudo.replace(
            "INSERT INTO table_maintenancedate2 VALUES", "")
        conteudo = conteudo.replace(
            "UPDATE table_tableinfo SET MaintenanceTable2Time=NOW(); ", "")
        conteudo = conteudo.replace(
            "UPDATE table_tableinfo SET MaintenanceTable1Time=NOW(); ", "")
        conteudo = conteudo.replace("),(", ")\n(")

        linhas = conteudo.split('\n')

        ultima_manutencao = None
        penultima_manutencao = None
        duracao_ultima_manutencao = None

        for linha in linhas:
            campos = linha.strip().strip('()').split(",")
            campos = [campo.strip("'") for campo in campos]
            if len(campos) > 6:
                if campos[6] == 'Finished' and campos[2] == filtro:
                    penultima_manutencao = ultima_manutencao
                    ultima_manutencao = campos[1]
                    duracao_ultima_manutencao = campos[3]
                # print(f"[DEBUG] Linha com 'Finished' encontrada: {linha}")
                    print(f"[DEBUG] Última manutenção atualizada para: {
                        ultima_manutencao} para a filtro: {filtro}")

            if filtro in ['S1', 'S2']:
                manutencao_a_retorna = penultima_manutencao if penultima_manutencao is not None else ultima_manutencao
            else:
                manutencao_a_retorna = ultima_manutencao

            if manutencao_a_retorna is None:
                print(
                    f"[DEBUG] Não há manutenções 'Finished' para o filtro: {filtro}")
            else:
                print(f"[RESULT] Manutenção a retornar para o filtro {filtro}: {
                      manutencao_a_retorna} com duração {duracao_ultima_manutencao}")

        # if penultima_manutencao is None:
        #     print(
        #         f"[DEBUG] Não há penúltima encontrada para o filtro: {filtro}")
        #     return ultima_manutencao
        # else:
        #     print(f"[RESULT] Penúltima manutenção para o filtro {
        #           filtro}: {penultima_manutencao}")

        linhas_filtradas = [
            linha for linha in linhas if "Finished" not in linha and filtro in linha]

        with open(arquivo_destino, 'w') as file:

            for linha in linhas_filtradas:
                file.write(linha + '\n')

        # print(f"[DEBUG] Arquivo {
        #       arquivo_destino} processado e salvo com sucesso.")
        # print(f"[DEBUG] Penúltima manutenção para filtro {
        #       filtro}: {penultima_manutencao}")

        print(f"[DEBUG] Arquivo {
              arquivo_destino} processado e salvo com sucesso.")
        return manutencao_a_retorna, duracao_ultima_manutencao

    except Exception as e:
        print(f"[ERRO] Erro ao processar o arquivo {arquivo_origem}: {e}")
        return None, None


def extrair_dados(arquivo):
    try:
        dados_extraidos = []
        with open(arquivo, 'r') as file:
            for linha in file:
                linha = linha.strip().strip('()')
                campos = linha.split("','")
                campos = [campo.strip("'") for campo in campos]
                dados_extraidos.append(campos)
        print(f"[DEBUG] Dados extraídos do arquivo {arquivo} com sucesso.")
        return dados_extraidos
    except Exception as e:
        print(f"[ERRO] Erro ao extrair dados do arquivo {arquivo}: {e}")
        return []


def extrair_datas(dados, filtro):
    try:
        resultados = []

        if len(dados) == 1 and isinstance(dados[0], list):
            dados = dados[0]

        for i, dado in enumerate(dados):
            if (dado[4] in ['']) and (dado[6] == 'Waiting'):
                data_atual_manutencao = dado[1]
                # duracao_manutencao = dado[3]
                proxima_data_manutencao = dados[i +
                                                1][1] if i + 1 < len(dados) else None

                # Encontrar a duração da última manutenção 'Finished'
                duracao_ultima_manutencao = None
                for j in range(i - 1, -1, -1):
                    if dados[j][6] == 'Finished' and dados[j][2] == filtro:
                        duracao_ultima_manutencao = dados[j][3]
                        break

                resultados.append(
                    (filtro, data_atual_manutencao,
                     duracao_ultima_manutencao, proxima_data_manutencao)
                )
                print(f"[DEBUG] Adicionando ao resultado: {filtro}, {data_atual_manutencao}, {
                      duracao_ultima_manutencao}, {proxima_data_manutencao}")
                break

        print(f"[DEBUG] Resultados finais: {resultados}") 
        return resultados
    except Exception as e:
        print(f"[ERRO] Erro ao extrair dados: {e}")
        return []


def processar_inicialmente(diretorio_filtros, db_config):
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_hundler = DBHandler(db_config)

    for arquivo_origem, filtro in diretorio_filtros.items():
        filtro_dir = os.path.join(base_path, filtro)
        os.makedirs(filtro_dir, exist_ok=True)
        caminho_arquivo_copia = os.path.join(
            filtro_dir, 'copia_' + os.path.basename(arquivo_origem))
        try:
            print(f"[DEBUG] Processando o arquivo inicial: {arquivo_origem}")

            ultima_manutencao, duracao_ultima_manutencao = processar_arquivo(
                arquivo_origem, caminho_arquivo_copia, filtro)

            dados = extrair_dados(caminho_arquivo_copia)
            resultados = extrair_datas(dados, filtro)

            print(f"[DEBUG] Resultados que irão ser salvos no banco: {
                  resultados}")

            conn = db_hundler.connect_db()
            if conn:
                for resultado in resultados:
                    if len(resultado) < 4:
                        print(f"[ERROR] Resultado inválido: {resultado}")
                    else:
                        # definir próxima data de manutenção com base nos dados extraídos
                        proxima_data_manutencao = resultado[1]

                        data_to_insert = (
                            ultima_manutencao,
                            proxima_data_manutencao,
                            duracao_ultima_manutencao,
                            filtro,
                        )

                        print(f"[DEBUG] Inserindo dados: {data_to_insert}")
                        db_hundler.insert_data(conn, data_to_insert)
                    conn.close()
                    print("[DEBUG] Conexão com o banco de dados fechada.")

            for resultado in resultados:
                print(f"[RESULT] Linha {resultado[0]} Data atual de manutenção: {
                      resultado[1]}, Duração da manutenção: {resultado[2]}, Próxima data de manutenção: {resultado[3]}")

            if ultima_manutencao:
                print(f"[RESULT] Última manutenção para filtro {
                      filtro}: {ultima_manutencao}")

        except Exception as e:
            print(f"[ERRO] Erro ao processar o arquivo inicial: {
                  arquivo_origem}: {e}")
