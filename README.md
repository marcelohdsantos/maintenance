# Projeto de Monitoramento de Diretórios com Watchdog

Este projeto utiliza a biblioteca Watchdog para monitorar diretórios específicos e processar arquivos automaticamente quando eles são alterados. As configurações de diretórios são gerenciadas por meio de um arquivo `.env`.

## Funcionalidades

- **Monitoramento de Diretórios**: Observa mudanças em arquivos específicos nos diretórios configurados.
- **Processamento de Arquivos**: Executa ações definidas quando os arquivos monitorados são modificados.
- **Integração com Banco de Dados**: Atualiza informações em um banco de dados PostgreSQL.
- **Configuração Flexível**: Utiliza um arquivo `.env` para gerenciar diretórios e outras configurações de maneira segura.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python 3.6+
- pip
- PostgreSQL (se estiver usando funcionalidades de banco de dados)

### Instalação de Dependências

Instale as dependências Python utilizando o `requirements.txt`:

```bash
pip install -r requirements.txt
```


## Como Executar

#### 1 - Ative um Ambiente Virtual (opcional, mas recomendado):
``` bash 
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate    # Windows
```
#### 2 - Execute o Script Principal:
``` bash 
python app.py
```
Onde main.py é o arquivo onde o script principal reside.

## Estrutura do projeto

``` kotlin

├── DB/                   # Diretório contendo arquivos relacionados ao banco de dados
│   └── db_handler.py     # Módulo responsável por gerenciar conexões e operações no banco de dados
├── utils.py              # Contém classes e funções como EventHandler e processar_inicialmente
├── app.py                # Script principal que configura e inicia o monitoramento
├── requirements.txt      # Lista de dependências do projeto
├── file_viewer.py        # Script do monitoramento dos diretórios e processamento dos eventos.  
└── .env                  # Configurações de ambiente, não deve ser versionado
```


## Variáveis de Ambiente

1. Crie um Arquivo .env na raiz do seu projeto com os seguintes conteúdos:

`DB_NAME=` 
`DB_USER=`
`DB_PASSWORD=`
`DB_HOST=`
`DB_PORT=`
`OPTIONS=`

2. Configuração do Banco de Dados: Se o projeto integrar com um banco de dados PostgreSQL, certifique-se de ter um banco de dados configurado e que as credenciais estejam corretas.