import requests 
import ssl 
import socket
from urllib.parse import urlparse

def obter_certificado(url):
    hostname = urlparse(url).hostname
    contexto = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=5) as conexao:
        with contexto.wrap_socket(
            conexao,
            server_hostname=hostname
        ) as conexao_segura:
            
            certificado = conexao_segura.getpeercert()

    return certificado

def normalizarurl(url): 
    if not url.startswith('http://') and not url.startswith('https://'):
        normalizada = 'https://' + url 
        return normalizada
    else: 
        return url
    
def classificar(resposta): 
    if 200 <= resposta < 300: 
        return 'Sucesso'
    elif 300 <= resposta < 400: 
        return 'Redirecionamento'
    elif 400 <= resposta < 500: 
        return 'Erro de cliente'
    elif 500 <= resposta < 600:
        return 'Erro de servidor'
    else: 
        return 'Erro desconhecido'

def analisar_site(url):
    url = normalizarurl(url)
    resposta = requests.get(
        url,
        timeout=5
    )
    tempo = resposta.elapsed.total_seconds() * 1000
    certificado = obter_certificado(url)
    
    return {
        "url": url,
        "status": resposta.status_code,
        "classificacao": classificar(resposta.status_code),
        "tempo": tempo,
        "https": url.startswith("https://"),
        "certificado": certificado["notAfter"]
    }