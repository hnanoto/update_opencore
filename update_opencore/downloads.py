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

def get_latest_opencore_version_fallback():
    """Fallback inteligente para contornar o limite da API do GitHub extraindo a tag diretamente do redirecionamento Web."""
    try:
        response = requests.get("https://github.com/acidanthera/OpenCorePkg/releases/latest", allow_redirects=True, timeout=10)
        tag = response.url.split("/")[-1]
        if tag and tag != "latest":
            log(f"{GREEN}Fallback Inteligente ativado: Versão {tag} recuperada com sucesso!{NC}")
            return tag
    except Exception as fallback_e:
        log(f"{RED}O Fallback Inteligente também falhou: {fallback_e}{NC}")
    return "Desconhecida"

def download_oc(build_type="RELEASE", pre_release=False):
    """Baixa e extrai a versão Release ou Debug do OpenCore, com Fallback Inteligente."""
    log(f"{YELLOW}Baixando OpenCore versão {build_type}...{NC}")
    oc_url = None
    oc_sha256_url = None
    
    try:
        if pre_release:
            response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases")
            response.raise_for_status()
            releases = response.json()
            latest_pre_release = None
            for release in reversed(releases):
                if release["prerelease"]:
                    latest_pre_release = release
                    break

            if not latest_pre_release:
                log(f"{RED}Erro: Não foi possível encontrar uma versão pré-lançamento do OpenCore.{NC}")
                return False

            for asset in latest_pre_release["assets"]:
                if f"-{build_type}.zip" in asset["browser_download_url"]:
                    oc_url = asset["browser_download_url"]
                    oc_sha256_url = asset["browser_download_url"] + ".sha256"
                    break

            if not oc_url:
                log(f"{RED}Erro: Não foi possível obter o link da versão pré-lançamento {build_type}.{NC}")
                return False
                
            log(f"Link de download do OpenCore pré-lançamento {build_type} encontrado: {oc_url}")
        else:
            try:
                # Tenta API Primária
                response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest", timeout=10)
                response.raise_for_status()
                for asset in response.json()["assets"]:
                    if f"-{build_type}.zip" in asset["browser_download_url"]:
                        oc_url = asset["browser_download_url"]
                        oc_sha256_url = asset["browser_download_url"] + ".sha256"
                        break
                
                if not oc_url:
                    raise Exception("URL não localizada na payload oficial.")
                log(f"Link de download via API encontrado: {oc_url}")
                
            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 403:
                    log(f"{YELLOW}Aviso: Limite de requisições da API do GitHub (403 Rate Limit) atingido.{NC}")
                    raise e  # Joga para o fallback
                else:
                    raise e

    except Exception as e:
        # Iniciando o Fallback Inteligente em caso de falhas da API (principalmente 403 Rate Limit)
        log(f"{YELLOW}Iniciando mecanismo de Fallback Inteligente para download...{NC}")
        if not pre_release:  # Fallbacks para latest_release funcionam deduzindo o nome do ZIP
            tag = get_latest_opencore_version_fallback()
            if tag != "Desconhecida":
                oc_url = f"https://github.com/acidanthera/OpenCorePkg/releases/download/{tag}/OpenCore-{tag}-{build_type}.zip"
                oc_sha256_url = f"{oc_url}.sha256"
                log(f"Link gerado por Fallback Inteligente: {oc_url}")
            else:
                log(f"{RED}Erro crítico: Fallback falhou e a API oficial está bloqueada.{NC}")
                sys.exit(1)
        else:
            log(f"{RED}Erro crítico: Não existe Fallback Inteligente para versões pre-release ao sofrer Rate Limit. Tente mais tarde.{NC}")
            sys.exit(1)

    # Passando para a fase de Checksum
    try:
        sha256_response = requests.get(oc_sha256_url, timeout=10)
        sha256_response.raise_for_status()
        expected_checksum = sha256_response.text.strip().split()[0]
        verificar_checksum = True
    except requests.exceptions.RequestException as e:
        log(f"{YELLOW}Não foi possível obter o checksum SHA-256. A verificação será pulada. Erro: {e}{NC}")
        verificar_checksum = False
        expected_checksum = None

    # Baixa o arquivo ZIP do OpenCore
    try:
        response = requests.get(oc_url, stream=True, timeout=15)
        response.raise_for_status()
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        
        # Correção da barra de progresso caso tamanho não venha no cabeçalho
        if total_size_in_bytes == 0:
            log(f"{YELLOW}Tamanho não especificado pelo servidor, baixando...{NC}")
            progress_bar = tqdm(unit='iB', unit_scale=True, desc=f"Baixando OpenCore {build_type}")
        else:
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=f"Baixando OpenCore {build_type}")
            
        with open("OpenCore.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=block_size):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            log(f"{RED}Erro: Tamanho do download não corresponde. Arquivo pode estar corrompido.{NC}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        log(f"{RED}{get_translation('download_fail')}: {e}{NC}")
        sys.exit(1)

    if verificar_checksum:
        downloaded_checksum = calculate_sha256("OpenCore.zip")
        if downloaded_checksum != expected_checksum:
            log(f"{RED}Erro fatal: O Checksum SHA-256 do arquivo baixado ({downloaded_checksum}) não bate com o esperado ({expected_checksum}). O arquivo pode estar comprometido!{NC}")
            sys.exit(1)
        else:
            log(f"{GREEN}Checksum SHA-256 verificado com super sucesso.{NC}")

    if not os.path.isfile("OpenCore.zip"):
        log(f"{RED}{get_translation('download_fail_zip')}{NC}")
        sys.exit(1)

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
        
    log(f"{GREEN}OpenCore versão {build_type} baixado e extraído de forma 100% segura.{NC}")
    return True

def get_latest_opencore_version():
    """Obtém a versão mais recente do OpenCore via API ou via Fallback."""
    try:
        response = requests.get("https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest", timeout=5)
        response.raise_for_status()
        return response.json()["tag_name"]
    except Exception as e:
        log(f"{YELLOW}Falha ao checar visão via API (pode ser Limit Rate). Tentando método Fallback Inteligente...{NC}")
        return get_latest_opencore_version_fallback()