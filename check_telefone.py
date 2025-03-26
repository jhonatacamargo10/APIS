from fastapi import FastAPI, HTTPException
import phonenumbers
from phonenumbers import geocoder, carrier

app = FastAPI()

@app.get("/verificar/telefone/{numero}")
def verificar_telefone(numero: str):
    try:
        # Analisa o número de telefone
        numero_parsed = phonenumbers.parse(numero)

        # Verifica se o número é válido
        if not phonenumbers.is_valid_number(numero_parsed):
            raise HTTPException(status_code=400, detail="Número de telefone inválido")

        # Verifica se o número é possível
        if not phonenumbers.is_possible_number(numero_parsed):
            raise HTTPException(status_code=400, detail="Número de telefone impossível")

        # Obtém o país e a operadora
        pais = geocoder.region_code_for_number(numero_parsed)
        operadora = carrier.name_for_number(numero_parsed, "en")

        return {
            "status": "válido",
            "numero": numero,
            "pais": pais,
            "operadora": operadora
        }

    except phonenumbers.phonenumberutil.NumberParseException:
        raise HTTPException(status_code=400, detail="Número de telefone inválido")
