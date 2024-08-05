def testar_acesso_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as file:
            content = file.read()
            print(f"Arquivo '{caminho_arquivo}' aberto com sucesso.")
            print("Conteúdo do arquivo:")
            print(content[:1000])
    except Exception as e:
        print(f"Erro ao abrir o arquivo '{caminho_arquivo}': {e}")


if __name__ == '__main__':
    caminho_arquivo = r'C:\Users\bc2g8585\Desktop\teste_iot\maintenanceCommand.txt'
    testar_acesso_arquivo(caminho_arquivo)


"""
        r'10.58.141.21\d\setup_lineS1\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S1',
        r'10.58.141.22\d\setup-lineS2\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S2',
        r'10.58.141.23\d\setup-lineS3\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S3',
        r'10.58.141.24\d\setup-lineS4\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S4',
        r'10.58.141.25\d\setup-lineS5\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S5',
        r'10.58.141.26\d\setup_lineS6\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S6',
        r'10.58.141.27\SetupL7\iotsoftware\SMT_Center_LogAnalyzer\maintenanceCommand.txt': 'S7'
"""
