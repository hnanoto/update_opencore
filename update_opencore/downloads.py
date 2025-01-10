import os
import requests
import subprocess
from logger import log, RED, YELLOW, GREEN, NC

def download_hfs_driver():
    """Baixa o HFSPlus.efi do repositório OcBinaryData."""
    log(f"{YELLOW}Baixando HFSPlus.efi do repositório OcBinaryData...{NC}")
    # Link correto para o HFSPlus.efi (2024-01-09)
    hfs_driver_url = "https://github.com/acidanthera/OcBinaryData/blob/master/Drivers/HfsPlus.efi"

    log(f"Link de download do HFSPlus.efi encontrado: {hfs_driver_url}")
    try:
        response = requests.get(hfs_driver_url, stream=True)
        response.raise_for_status()  # Verifica se houve erro na requisição
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "HfsPlus.efi"), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        log(f"{RED}Erro: O download do HFSPlus.efi falhou: {e}{NC}")
        sys.exit(1)

    if not os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "HfsPlus.efi")):
        log(f"{RED}Erro: O download do HFSPlus.efi falhou.{NC}")
        sys.exit(1)

    log(f"{GREEN}HFSPlus.efi baixado com sucesso.{NC}")

def download_oc(build_type="RELEASE"):
    """Baixa e extrai a versão Release ou Debug do OpenCore."""
    log(f"{YELLOW}Baixando OpenCore versão {build_type}...{NC}")
    try:
        response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest")
        response.raise_for_status()
        
        oc_url = None
        for asset in response.json()["assets"]:
            if f"-{build_type}.zip" in asset["browser_download_url"]:
                oc_url = asset["browser_download_url"]
                break

        if not oc_url:
            log(f"{RED}Erro: Não foi possível obter o link da versão {build_type} do OpenCore.{NC}")
            sys.exit(1)

        log(f"Link de download do OpenCore versão {build_type} encontrado: {oc_url}")
        response = requests.get(oc_url, stream=True)
        response.raise_for_status()
        with open("OpenCore.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        log(f"{RED}Erro: Não foi possível acessar a API do GitHub ou baixar o OpenCore: {e}{NC}")
        sys.exit(1)

    if not os.path.isfile("OpenCore.zip"):
        log(f"{RED}Erro: O download do OpenCore falhou.{NC}")
        sys.exit(1)

    # Verificar se o arquivo ZIP é válido antes de tentar descompactá-lo
    try:
        subprocess.run(["unzip", "-tq", "OpenCore.zip"], check=True)
    except subprocess.CalledProcessError:
        log(f"{RED}Erro: O arquivo ZIP do OpenCore está corrompido ou inválido.{NC}")
        sys.exit(1)

    try:
        subprocess.run(["unzip", "-o", "OpenCore.zip", "-d", "OpenCore"], check=True)
    except subprocess.CalledProcessError:
        log(f"{RED}Erro: Falha ao extrair OpenCore.zip.{NC}")
        sys.exit(1)
    log(f"{GREEN}OpenCore versão {build_type} baixado e extraído com sucesso.{NC}")

def get_latest_opencore_version():
    """Obtém a versão mais recente do OpenCore da API do GitHub."""
    try:
        response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest")
        response.raise_for_status()
        return response.json()["tag_name"]
    except requests.exceptions.RequestException as e:
        log(f"{RED}Erro: Não foi possível obter a versão mais recente do OpenCore: {e}{NC}")
        return "Desconhecida"