from fastapi import FastAPI, HTTPException
import requests
import re

app = FastAPI()

# API gratuita para CNPJ (ReceitaWS)
CNPJ_API_URL = "https://www.receitaws.com.br/v1/cnpj/{}"

@app.get("/verificar/{cnpj}")
def verificar_cnpj(cnpj: str):
    cnpj = re.sub(r'\D', '', cnpj)  # Remove caracteres não numéricos

    if len(cnpj) != 14:
        raise HTTPException(status_code=400, detail="CNPJ inválido")

    # Adicionando log para ver se a URL está correta
    print(f"Consultando CNPJ: {cnpj}")

    try:
        # A requisição agora tem um timeout de 10 segundos
        resposta = requests.get(CNPJ_API_URL.format(cnpj), timeout=10)

        # Adicionando log para verificar a resposta
        print(f"Status Code: {resposta.status_code}")
        print(f"Resposta: {resposta.text}")

        if resposta.status_code == 200:
            dados = resposta.json()
            return {"status": "válido", "dados": dados}
        else:
            raise HTTPException(status_code=400, detail="Erro ao consultar CNPJ")
    except requests.exceptions.RequestException as e:
        # Captura de erro de rede ou timeout
        print(f"Erro ao consultar a API: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar a API externa")
