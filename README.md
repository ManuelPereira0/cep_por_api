# Automação em python, com consumo de API

## Programa que verifica se existe o CEP, e trás as informações do mesmo.

## Fonte da API: https://brasilapi.com.br/docs

# Passo a passo para utilizar o programa

## Configurar DB
> Atualizar as informações abaixo para o seu DB
```python
host='seu host',
user='seu user',
database='seu database',
password='sua password',
```

### No Linux
Bibliotecas para serem instaladas:
- instalar o pip: sudo apt-get install python3-pip
- pip install pymysql 
- sudo apt update
- sudo apt install firefox 
> Somente se não tiver o FireFox instalado no computador

### No Windows
Para fazer a instalação da versão mais recente do Python no Windows: https://www.python.org/downloads/windows/
- pip install pymysql 

### Para rodar o programa
> No Linux: python3 nome_do_arquivo.py <br>
> No Windows: python nome_do_arquivo.py