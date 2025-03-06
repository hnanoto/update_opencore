# update_opencore
www.youtube.com/@HackintoshAndBeyond

Video da ferramenta: https://youtu.be/dH-TH812sTQ

[discord.gg/5hvZ5u7QXQ](https://discord.gg/5hvZ5u7QXQ)

Update-OC-EFI Script
Este script foi desenvolvido para automatizar o processo de atualização do OpenCore, seus drivers e a mesclagem (merge) das novas chaves do Sample.plist com o seu config.plist em sistemas Hackintosh. Ele foi projetado para ser fácil de usar, seguro e eficiente, minimizando a intervenção manual do usuário.

Funcionalidades:

Interface de Menu Intuitiva: Um menu simples e direto ao ponto permite que o usuário escolha a operação desejada com facilidade.
Detecção Automática da Partição EFI: O script localiza e identifica automaticamente as partições EFI montadas no sistema.
Backup Automático da EFI: Antes de fazer qualquer modificação, o script cria um backup completo da pasta EFI em EFI-Backup-<data>-<hora> na própria partição EFI, permitindo reverter facilmente para uma configuração anterior em caso de problemas.
Download do OpenCore: Baixa a última versão RELEASE ou DEBUG do OpenCore diretamente do repositório oficial da Acidanthera no GitHub.
Atualização Inteligente de Arquivos:
Substitui os arquivos da pasta BOOT (BOOTx64.efi) e os arquivos da pasta OC (OpenCore.efi, .contentVisibility e .contentFlavour)
Mantém a pasta OC original, preservando seus arquivos config.plist, ACPI (SSDTs personalizados), Kexts (personalizadas) e Resources (temas, áudios, etc.).
Atualiza apenas os drivers habilitados no seu config.plist, evitando a substituição de drivers não utilizados.
Copia novos drivers da pasta Drivers do OpenCore baixado para a sua pasta EFI/OC/Drivers, caso você tenha algum driver novo listado no seu config.plist.
Mesclagem (Merge) de Novas Chaves: Adiciona automaticamente as novas chaves do Sample.plist (da versão baixada do OpenCore) ao seu config.plist, preservando as configurações existentes e adicionando quaisquer novas opções introduzidas em novas versões do OpenCore.
Validação do config.plist: Utiliza o ocvalidate (ferramenta oficial do OpenCore) para verificar a integridade do config.plist após as modificações, alertando sobre potenciais erros.
Limpeza de Arquivos Temporários: Remove os arquivos temporários baixados após a conclusão da atualização.
Log Detalhado: Gera um arquivo de log (update_opencore_<data>-<hora>.log) com informações detalhadas sobre cada etapa do processo, facilitando a identificação de problemas.
Como Usar:

Download: Baixe o script update_opencore.py do meu repositório do GitHub.
Descompacte o Arquivo ZIP: Descompacte o arquivo ZIP baixado para um local de fácil acesso, como a pasta Downloads.
Terminal: Abra o Terminal (Aplicativos -> Utilidades -> Terminal).
Navegue até o Diretório: Use o comando cd para navegar até o diretório onde você descompactou o arquivo, por exemplo:
cd /Users/seu_usuario/Downloads
Use code with caution.
Bash
Torne o Script Executável: Execute o seguinte comando para dar permissão de execução ao script:
chmod +x update_opencore.py
Use code with caution.
Bash
Execute o Script com Privilégios de Administrador: Execute o script com sudo:
sudo python3 update_opencore.py
Use code with caution.
Bash
Digite a sua senha de administrador quando solicitado.
Siga as Instruções do Menu: O script exibirá um menu com as seguintes opções:
1. Atualizar o OpenCore (RELEASE): Baixa e instala a última versão RELEASE do OpenCore.
2. Atualizar o OpenCore (DEBUG): Baixa e instala a última versão DEBUG do OpenCore.
3. Atualizar apenas drivers: Atualiza apenas os drivers na pasta EFI/OC/Drivers, mantendo a versão atual do OpenCore.
4. Adicionar novas chaves ao config.plist: Adiciona as novas chaves do Sample.plist ao seu config.plist, sem atualizar o OpenCore ou os drivers.
5. Sair: Sai do script.
Escolha a Opção Desejada: Digite o número correspondente à opção desejada e pressione Enter.
Selecione a Partição EFI: O script listará as partições EFI encontradas. Digite o número correspondente à partição EFI onde o OpenCore está instalado e pressione Enter.
Confirmação: O script exibirá um resumo das operações que serão realizadas. Confirme se deseja prosseguir ou abortar a operação.
Aguarde a Conclusão: O script executará as operações selecionadas. Aguarde a mensagem de conclusão.
Pré-requisitos:

Python 3: O script requer o Python 3 para ser executado. O macOS já vem com o Python 3 instalado por padrão.
Conexão com a Internet: O script precisa de uma conexão ativa com a internet para baixar as versões mais recentes do OpenCore.
curl: Utilizado para baixar arquivos. Já vem instalado por padrão no macOS.
unzip: Utilizado para descompactar arquivos. Já vem instalado por padrão no macOS.
PlistBuddy: Utilizado para manipular arquivos .plist. Já vem instalado por padrão no macOS.
ocvalidate: (Opcional, mas recomendado) Ferramenta oficial do OpenCore para validar o config.plist. O script verifica se o ocvalidate está presente no pacote do OpenCore baixado. Caso não encontre, a validação será pulada.
Instalação de dependências no macOS (caso necessário):

Python 3:
Instruções para instalar o Python 3 no macOS podem ser encontradas na internet. O Homebrew é um gerenciador de pacotes recomendado para facilitar a instalação (brew install python3).
Outras dependências: Como curl, unzip e PlistBuddy já vêm instalados por padrão no macOS, geralmente não é necessário instalá-los separadamente.
Possíveis Problemas e Soluções:

porque dá isso? henrique@iMac-Pro-de-Henrique ~ % sudo python3 /Volumes/UNTITLED/Linux/FerramentasTops/update_opencore/update_opencore/main.py
Traceback (most recent call last):
File "/Volumes/UNTITLED/Linux/FerramentasTops/update_opencore/update_opencore/main.py", line 6, in <module>
from downloads import download_oc, get_latest_opencore_version, download_hfs_driver
File "/Volumes/UNTITLED/Linux/FerramentasTops/update_opencore/update_opencore/downloads.py", line 6, in <module>
from tqdm import tqdm
ModuleNotFoundError: No module named 'tqdm'
henrique@iMac-Pro-de-Henrique ~ %
O erro "ModuleNotFoundError: No module named 'tqdm'" indica que o script Python está tentando usar um módulo chamado tqdm, mas ele não está instalado no seu sistema Python.

tqdm é uma biblioteca Python que fornece uma barra de progresso para loops e outras operações demoradas. É muito útil para mostrar o andamento de downloads, processamentos de dados, etc.

Para corrigir o problema, você precisa instalar o módulo tqdm.

Você pode fazer isso usando o pip, o gerenciador de pacotes do Python. Abra o Terminal (ou Prompt de Comando, se estiver no Windows) e execute o seguinte comando:

pip3 install tqdm
Use code with caution.
Bash
Explicação do comando:

pip3: Invoca o gerenciador de pacotes Python 3 (que você está usando, como indicado por python3 no seu comando original). Se você tiver apenas uma versão do Python instalada, pip pode ser suficiente.
install: Diz ao pip para instalar um pacote.
tqdm: O nome do pacote que você deseja instalar.
Depois de executar o comando, aguarde a instalação ser concluída. Você verá mensagens indicando o progresso da instalação.

Execute o script novamente:

Depois que o tqdm for instalado, tente executar o script novamente:

sudo python3 /Volumes/UNTITLED/Linux/FerramentasTops/update_opencore/update_opencore/main.py
Use code with caution.
Bash
Deverá funcionar sem o erro de ModuleNotFoundError.

Se o pip3 não for encontrado:

Se o comando pip3 não funcionar e você receber um erro dizendo que o comando não foi encontrado, pode ser que o pip não esteja instalado ou não esteja no seu PATH.

Verifique se o Python está instalado corretamente: Abra o Terminal e digite python3 --version. Se o Python não estiver instalado, você precisará instalá-lo.
Instale o pip: Se o Python estiver instalado, mas o pip não, tente instalar usando o seguinte comando:
sudo apt update  # (Se você estiver usando um sistema baseado em Debian/Ubuntu)
sudo apt install python3-pip
Use code with caution.
Bash
Ou, se você estiver em outro sistema operacional, consulte a documentação da sua distribuição Linux ou siga as instruções de instalação do Python para o seu sistema.
Resumo:

Erro: ModuleNotFoundError: No module named 'tqdm' significa que o módulo tqdm não está instalado.
Solução: Instale o tqdm usando pip3 install tqdm.
Verificação adicional: Se o pip3 não funcionar, verifique se o Python está instalado e, em seguida, instale o pip.
Depois de instalar o tqdm e executar o script novamente, ele deve funcionar corretamente. Se você ainda tiver problemas, forneça mais detalhes sobre o seu sistema operacional e quaisquer outros erros que você receber.



ModuleNotFoundError: No module named 'requests': Significa que o módulo requests do Python não está instalado.
Solução: Instale o módulo requests usando o pip:
sudo python3 -m pip install requests
Use code with caution.
Bash
Erros com ocvalidate: O ocvalidate é uma ferramenta essencial que está dentro do pacote do OpenCore na pasta Utilities, o script irá procurar por essa ferramenta dentro da pasta temporária onde o novo OpenCore é baixado, caso não encontre não fará a validação.
IndentationError: Indica um erro na indentação do código Python.
Solução: Verifique se a indentação do código está correta, usando 4 espaços para cada nível de indentação. Certifique-se de que você não está misturando espaços e tabulações.
No such file or directory: Significa que o script está tentando acessar um arquivo ou diretório que não existe.
Solução: Verifique se o caminho para o arquivo ou diretório está correto e se o arquivo ou diretório realmente existe no local especificado. Certifique-se de ter extraído o conteúdo do ZIP do OpenCore corretamente.
Permission denied: Significa que o script não tem permissão para acessar um arquivo ou diretório.
Solução: Certifique-se de que o script está sendo executado com privilégios de administrador (usando sudo). Verifique as permissões do arquivo ou diretório e, se necessário, altere-as usando o comando chmod.
[Errno 28] No space left on device: Significa que o script está tentando gravar dados em um dispositivo de armazenamento que está sem espaço.
Solução: O script foi modificado para criar os backups dentro da partição EFI, o que deve resolver o problema. Se por algum motivo você precisar de mais espaço na partição EFI, será necessário redimensioná-la, mas, isso não é recomendado fazer por este script, pois é um procedimento avançado.
Erros no config.plist: Se o ocvalidate reportar erros no seu config.plist, você precisará corrigi-los manualmente usando um editor de plist apropriado. Certifique-se de seguir as recomendações da documentação do OpenCore ao editar o config.plist.
Observações:

Este script foi desenvolvido e testado em um ambiente macOS.
É altamente recomendável fazer um backup completo da sua pasta EFI antes de executar qualquer script de atualização.
Sempre leia a documentação oficial do OpenCore antes de fazer qualquer atualização.
Disclaimer:

Este script é fornecido "como está", sem garantia de qualquer tipo. O autor não se responsabiliza por quaisquer danos causados pelo uso deste script. Use por sua conta e risco.

Contribuições:

Contribuições para melhorar este script são bem-vindas! Sinta-se à vontade para fazer um fork do repositório, fazer as suas modificações e enviar um pull request.
Em português 

-------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_opencore
www.youtube.com/@HackintoshAndBeyond

[discord.gg/5hvZ5u7QXQ](https://discord.gg/5hvZ5u7QXQ)

Update-OC-EFI Script
This script was developed to automate the process of updating OpenCore, its drivers, and merging the new keys from Sample.plist with your config.plist on Hackintosh systems. It's designed to be easy to use, safe, and efficient, minimizing manual user intervention.

Features:

Intuitive Menu Interface: A simple and straightforward menu allows the user to easily choose the desired operation.
Automatic EFI Partition Detection: The script automatically locates and identifies the EFI partitions mounted on the system.
Automatic EFI Backup: Before making any changes, the script creates a full backup of the EFI folder in EFI-Backup-<date>-<time> on the EFI partition itself, allowing for easy rollback to a previous configuration in case of problems.
OpenCore Download: Downloads the latest RELEASE or DEBUG version of OpenCore directly from the official Acidanthera repository on GitHub.
Smart File Update:
Replaces the files in the BOOT folder (BOOTx64.efi) and files in the OC folder (OpenCore.efi, .contentVisibility, and .contentFlavour).
Preserves the original OC folder, including your config.plist, ACPI (custom SSDTs), Kexts (custom kexts), and Resources (themes, audio, etc.).
Updates only the drivers enabled in your config.plist, avoiding overwriting unused drivers.
Copies new drivers from the Drivers folder of the downloaded OpenCore to your EFI/OC/Drivers folder if you have any new drivers listed in your config.plist.
Merging of New Keys: Automatically adds new keys from the Sample.plist (from the downloaded OpenCore version) to your config.plist, preserving existing settings and adding any new options introduced in newer OpenCore versions.
config.plist Validation: Uses ocvalidate (official OpenCore tool) to verify the integrity of the config.plist after modifications, alerting about potential errors.
Temporary File Cleanup: Removes downloaded temporary files after the update process is complete.
Detailed Logging: Generates a log file (update_opencore_<date>-<time>.log) with detailed information about each step of the process, making it easier to identify issues.
How to Use:

Download: Download the update_opencore.py script from your GitHub repository.
Unzip the ZIP file: Unzip the downloaded ZIP file to an easily accessible location, such as the Downloads folder.
Terminal: Open Terminal (Applications -> Utilities -> Terminal).
Navigate to the Directory: Use the cd command to navigate to the directory where you unzipped the file, for example:
cd /Users/your_username/Downloads
Use code with caution.
Bash
Make the Script Executable: Run the following command to give the script execute permission:
chmod +x update_opencore.py
Use code with caution.
Bash
Run the Script with Administrator Privileges: Run the script with sudo:
sudo python3 update_opencore.py
Use code with caution.
Bash
Enter your administrator password when prompted.
Follow the Menu Instructions: The script will display a menu with the following options:
1. Update OpenCore (RELEASE): Downloads and installs the latest RELEASE version of OpenCore.
2. Update OpenCore (DEBUG): Downloads and installs the latest DEBUG version of OpenCore.
3. Update drivers only: Updates only the drivers in the EFI/OC/Drivers folder, keeping the current OpenCore version.
4. Add new keys to config.plist: Adds new keys from Sample.plist to your config.plist without updating OpenCore or drivers.
5. Exit: Exits the script.
Choose the Desired Option: Enter the number corresponding to the desired option and press Enter.
Select the EFI Partition: The script will list the EFI partitions found. Enter the number corresponding to the EFI partition where OpenCore is installed and press Enter.
Confirmation: The script will display a summary of the operations to be performed. Confirm if you want to proceed or abort the operation.
Wait for Completion: The script will perform the selected operations. Wait for the completion message.
Prerequisites:

Python 3: The script requires Python 3 to run. macOS comes with Python 3 installed by default.
Internet Connection: The script requires an active internet connection to download the latest versions of OpenCore.
curl: Used to download files. It comes pre-installed on macOS.
unzip: Used to unzip files. It comes pre-installed on macOS.
PlistBuddy: Used to manipulate .plist files. It comes pre-installed on macOS.
ocvalidate: (Optional, but recommended) Official OpenCore tool to validate config.plist. The script checks if ocvalidate is present in the downloaded OpenCore package. If not found, validation will be skipped.
Installing dependencies on macOS (if necessary):

Python 3:
Instructions for installing Python 3 on macOS can be found on the internet. Homebrew is a recommended package manager for easy installation (brew install python3).
Other dependencies: Since curl, unzip, and PlistBuddy are already installed by default on macOS, you usually don't need to install them separately.
Possible Issues and Solutions:

ModuleNotFoundError: No module named 'requests': This means that the requests module for Python is not installed.
Solution: Install the requests module using pip:
sudo python3 -m pip install requests
Use code with caution.
Bash
ocvalidate errors: The ocvalidate is an essential tool that comes inside the package of the OpenCore on the Utilities folder, the script will look for this tool inside the temporary folder where the new OpenCore is downloaded, if it doesn't find it, it will skip the validation.
IndentationError: Indicates an error in the Python code indentation.
Solution: Check that the code indentation is correct, using 4 spaces for each indentation level. Make sure you are not mixing spaces and tabs.
No such file or directory: Means the script is trying to access a file or directory that does not exist.
Solution: Check that the path to the file or directory is correct and that the file or directory actually exists in the specified location. Make sure you have extracted the contents of the OpenCore ZIP file correctly.
Permission denied: Means the script does not have permission to access a file or directory.
Solution: Make sure the script is being run with administrator privileges (using sudo). Check the permissions of the file or directory and, if necessary, change them using the chmod command.
[Errno 28] No space left on device: Means the script is trying to write data to a storage device that is out of space.
Solution: The script has been modified to create backups inside the EFI partition, which should solve the problem. If for some reason you need more space on the EFI partition, you will need to resize it, but this is not recommended to do with this script, as it is an advanced procedure.
Errors in config.plist: If ocvalidate reports errors in your config.plist, you will need to fix them manually using a suitable plist editor. Be sure to follow the recommendations in the OpenCore documentation when editing config.plist.
Notes:

This script was developed and tested in a macOS environment.
It is highly recommended to make a full backup of your EFI folder before running any update script.
Always read the official OpenCore documentation before making any updates.
Disclaimer:

This script is provided "as is", without warranty of any kind. The author is not responsible for any damage caused by the use of this script. Use at your own risk.

Contributions:

Contributions to improve this script are welcome! Feel free to fork the repository, make your modifications, and submit a pull request.
