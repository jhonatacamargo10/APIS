from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# API para consultar informações do IP (IPinfo.io)
IPINFO_API_URL = "https://ipinfo.io/{}/json"

@app.get("/verificar/ip/{ip}")
def verificar_ip(ip: str):
    try:
        # Realizando a requisição na API do IPinfo com verificação SSL desabilitada
        resposta = requests.get(IPINFO_API_URL.format(ip), verify=False)

        if resposta.status_code == 200:
            dados = resposta.json()
            return {"status": "válido", "dados": dados}
        else:
            raise HTTPException(status_code=400, detail="Erro ao consultar IP")
    except requests.exceptions.RequestException as e:
        # Captura de erro de rede ou timeout
        print(f"Erro ao consultar a API: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar a API externa")
