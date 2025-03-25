import ssl
import socket
from fastapi import FastAPI, HTTPException

app = FastAPI()

def verificar_ssl(hostname: str):
    try:
        # Conectando ao servidor usando o protocolo SSL
        contexto_ssl = ssl.create_default_context()
        conexao = contexto_ssl.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conexao.settimeout(5)

        # Conectando ao servidor na porta 443 (HTTPS)
        conexao.connect((hostname, 443))

        # Obtendo o certificado SSL
        certificado = conexao.getpeercert()

        if certificado:
            return {"status": "válido", "certificado": certificado}
        else:
            raise HTTPException(status_code=400, detail="Certificado SSL não encontrado")
    except ssl.SSLError as e:
        raise HTTPException(status_code=400, detail=f"Erro no certificado SSL: {e}")
    except socket.error as e:
        raise HTTPException(status_code=400, detail=f"Erro ao conectar com o servidor: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
    finally:
        conexao.close()

@app.get("/verificar/ssl/{hostname}")
def verificar_ssl_api(hostname: str):
    # Validando o hostname (sem a parte "https://")
    if "http://" in hostname or "https://" in hostname:
        hostname = hostname.split("://")[1]

    return verificar_ssl(hostname)
