import os
import requests
import subprocess
import sys
from logger import log, RED, YELLOW, GREEN, NC, get_translation
from tqdm import tqdm
import hashlib

def download_hfs_driver():
    """Baixa o HFSPlus.efi do repositório OcBinaryData."""
    log(f"{YELLOW}{get_translation('downloading_hfs')}{NC}")
    # Link correto para o HFSPlus.efi (2024-01-09)
    hfs_driver_url = "https://raw.githubusercontent.com/acidanthera/OcBinaryData/master/Drivers/HfsPlus.efi"

    log(f"{get_translation('hfs_download_link_found', True)} {hfs_driver_url}")
    try:
        response = requests.get(hfs_driver_url, stream=True)
        response.raise_for_status()  # Verifica se houve erro na requisição
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "HfsPlus.efi"), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        log(f"{RED}{get_translation('hfs_download_failed', True)}: {e}{NC}")
        sys.exit(1)

    if not os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "HfsPlus.efi")):
        log(f"{RED}{get_translation('hfs_not_found')}{NC}")
        sys.exit(1)

    log(f"{GREEN}{get_translation('hfs_download_success')}{NC}")

def calculate_sha256(file_path):
    """Calcula o SHA-256 de um arquivo."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_oc(build_type="RELEASE", pre_release=False):
    """Baixa e extrai a versão Release ou Debug do OpenCore."""
    log(f"{YELLOW}Baixando OpenCore versão {build_type}...{NC}")
    try:
        if pre_release:
            response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases")
            response.raise_for_status()
            releases = response.json()
            # Encontrar a versão pré-lançamento mais recente (invertendo a lista)
            latest_pre_release = None
            for release in reversed(releases):
                if release["prerelease"]:
                    latest_pre_release = release
                    break

            if not latest_pre_release:
                log(f"{RED}Erro: Não foi possível encontrar uma versão pré-lançamento do OpenCore.{NC}")
                return False  # Retorna False em vez de sys.exit(1)

            oc_url = None
            for asset in latest_pre_release["assets"]:
                if f"-{build_type}.zip" in asset["browser_download_url"]:
                    oc_url = asset["browser_download_url"]
                    oc_sha256_url = asset["browser_download_url"] + ".sha256"
                    break

            if not oc_url:
                log(f"{RED}Erro: Não foi possível obter o link da versão pré-lançamento {build_type} do OpenCore.{NC}")
                return False  # Retorna False em vez de sys.exit(1)

            log(f"Link de download do OpenCore versão pré-lançamento {build_type} encontrado: {oc_url}")
        else:
            response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest")
            response.raise_for_status()
            oc_url = None
            for asset in response.json()["assets"]:
                if f"-{build_type}.zip" in asset["browser_download_url"]:
                    oc_url = asset["browser_download_url"]
                    oc_sha256_url = asset["browser_download_url"] + ".sha256"
                    break

            if not oc_url:
                log(f"{RED}Erro: Não foi possível obter o link da versão {build_type} do OpenCore.{NC}")
                sys.exit(1)

            log(f"Link de download do OpenCore versão {build_type} encontrado: {oc_url}")

        # Tenta baixar o checksum SHA-256
        try:
            sha256_response = requests.get(oc_sha256_url)
            sha256_response.raise_for_status()
            expected_checksum = sha256_response.text.strip().split()[0]
            verificar_checksum = True
        except requests.exceptions.RequestException as e:
            log(f"{YELLOW}Não foi possível obter o checksum SHA-256 para {build_type}. A verificação de integridade será pulada. Erro: {e}{NC}")
            verificar_checksum = False
            expected_checksum = None

        # Baixa o arquivo do OpenCore com barra de progresso
        response = requests.get(oc_url, stream=True)
        response.raise_for_status()
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=f"Baixando OpenCore {build_type}")
        with open("OpenCore.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=block_size):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            log(f"{RED}Erro: Falha no download do OpenCore.{NC}")
            sys.exit(1)

        # Verifica o checksum SHA-256, se disponível
        if verificar_checksum:
            downloaded_checksum = calculate_sha256("OpenCore.zip")
            if downloaded_checksum != expected_checksum:
                log(f"{RED}Erro: A integridade do download do OpenCore não pôde ser verificada. Checksum esperado: {expected_checksum}, checksum baixado: {downloaded_checksum}{NC}")
                sys.exit(1)
            else:
                log(f"{GREEN}Checksum SHA-256 verificado com sucesso.{NC}")

    except requests.exceptions.RequestException as e:
        log(f"{RED}{get_translation('download_fail')}: {e}{NC}")
        sys.exit(1)

    if not os.path.isfile("OpenCore.zip"):
        log(f"{RED}{get_translation('download_fail_zip')}{NC}")
        sys.exit(1)

    # Verificar se o arquivo ZIP é válido antes de tentar descompactá-lo
    try:
        subprocess.run(["unzip", "-tq", "OpenCore.zip"], check=True)
    except subprocess.CalledProcessError:
        log(f"{RED}{get_translation('invalid_zip')}{NC}")
        sys.exit(1)

    try:
        subprocess.run(["unzip", "-o", "OpenCore.zip", "-d", "OpenCore"], check=True)
    except subprocess.CalledProcessError:
        log(f"{RED}{get_translation('extract_error')}{NC}")
        sys.exit(1)
    log(f"{GREEN}OpenCore versão {build_type} baixado e extraído com sucesso.{NC}")
    return True # Retorna True se o download e a extração forem bem-sucedidos

def get_latest_opencore_version():
    """Obtém a versão mais recente do OpenCore da API do GitHub."""
    try:
        response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest")
        response.raise_for_status()
        return response.json()["tag_name"]
    except requests.exceptions.RequestException as e:
        log(f"{RED}Erro: Não foi possível obter a versão mais recente do OpenCore: {e}{NC}")
        return "Desconhecida"