# update_opencore
www.youtube.com/@HackintoshAndBeyond

discord.gg/5hvZ5u7QXQ

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
