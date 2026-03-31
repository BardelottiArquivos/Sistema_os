import requests
import logging

logger = logging.getLogger(__name__)

class ViaCEPService:
    BASE_URL = "https://viacep.com.br/ws"
    
    @classmethod
    def consultar_cep(cls, cep):
        try:
            cep_limpo = cep.replace('-', '').replace('.', '')
            url = f"{cls.BASE_URL}/{cep_limpo}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                if 'erro' not in dados:
                    return {
                        'cep': dados['cep'],
                        'logradouro': dados['logradouro'],
                        'bairro': dados['bairro'],
                        'cidade': dados['localidade'],
                        'estado': dados['uf'],
                        'complemento': dados.get('complemento', '')
                    }
            return None
        except Exception as e:
            logger.error(f"Erro ao consultar CEP: {str(e)}")
            return None
