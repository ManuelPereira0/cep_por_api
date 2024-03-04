import requests
import pymysql.cursors
from time import sleep
from requests.exceptions import RequestException

def criar_conexao():
    return pymysql.connect(
        host='your host',
        user='your user',
        database='your database',
        password='your password',
        cursorclass=pymysql.cursors.DictCursor
    )
    
conexao = criar_conexao()
cursor = conexao.cursor()

contador_geral = 4712
contador_sessao_atual = 1

while True:
    try:
        comando = f'SELECT cep FROM 20240227_cep WHERE observacao IS NULL LIMIT 1'
        cursor.execute(comando)
        linha = cursor.fetchone()
        
        if linha is None:
            break
        
        cep = linha['cep']
        dados_ceps = requests.get(f"https://brasilapi.com.br/api/cep/v2/{cep}")
        print(dados_ceps)
        if dados_ceps.status_code == 404:
            atualizar = f'UPDATE 20240227_cep SET observacao = "404" WHERE cep = "{cep}"'
            cursor.execute(atualizar)
            conexao.commit()
        
        else:
            dados_cep = dados_ceps.json()
            state = dados_cep.get('state')
            city = dados_cep.get('city')
            neighborhood = dados_cep.get('neighborhood')
            street = dados_cep.get('street')
            longitude = dados_cep.get('location', {}).get('coordinates', {}).get('longitude')
            latitude = dados_cep.get('location', {}).get('coordinates', {}).get('latitude')
            
            atualizar = f'''UPDATE 20240227_cep 
            SET state = "{state}", city = "{city}", neighborhood = "{neighborhood}", street = "{street}",
            longitude = "{longitude}", latitude = "{latitude}", observacao = "200" 
            WHERE cep = "{cep}"'''
            
            cursor.execute(atualizar)
            conexao.commit()
        
        print(f"Registro nº{contador_geral}, registro da sessão = {contador_sessao_atual}, cep = {cep}")
        contador_geral += 1
        contador_sessao_atual += 1
        sleep(1)

    except RequestException as e:
        # Tratamento de erro para exceções relacionadas a solicitações HTTP
        print(f"Erro ao fazer solicitação HTTP: {e}")
        continue

    except pymysql.Error as e:
        # Tratamento de erro para exceções relacionadas ao banco de dados
        print(f"Erro ao acessar o banco de dados: {e}")
        break  # Interrompe o loop se ocorrer um erro relacionado ao banco de dados

conexao.close()

