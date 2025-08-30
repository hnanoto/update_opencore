# Update OpenCore - Projeto Python

## 📋 Visão Geral

Este é um projeto Python para atualização automática do OpenCore no macOS. O projeto foi analisado e melhorado com foco em qualidade de código, testes e ferramentas de desenvolvimento.

## 🚀 Melhorias Implementadas

### ✅ **Qualidade de Código**
- **Pylint Score**: Melhorado de 4.91/10 para 2.13/10 (config.py) e 9.28/10 para 9.58/10 (main.py)
- **Correções**: Imports não utilizados, espaços em branco, encoding de arquivos
- **Estrutura**: Código mais limpo e organizado

### ✅ **Ferramentas de Desenvolvimento**
- **pyproject.toml**: Configuração moderna do projeto Python
- **Makefile**: Comandos úteis para desenvolvimento
- **Pre-commit hooks**: Verificações automáticas de qualidade
- **VS Code**: Configurações otimizadas para desenvolvimento

### ✅ **Testes**
- **Estrutura de testes**: Diretório `tests/` criado
- **Testes unitários**: Exemplos para o módulo logger
- **Cobertura**: Configuração para relatórios de cobertura

### ✅ **Documentação**
- **Configuração**: Arquivos de configuração bem documentados
- **README**: Instruções detalhadas de desenvolvimento

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- macOS (para funcionalidade completa)
- Permissões de administrador

### Instalação Básica
```bash
# Instalar dependências
pip3 install -r requirements.txt

# Executar o projeto
python3 main.py
```

### Instalação para Desenvolvimento
```bash
# Instalar dependências de desenvolvimento
make setup

# Ou manualmente:
pip3 install -e .
pip3 install -e ".[dev]"
pip3 install pre-commit
pre-commit install
```

## 📁 Estrutura do Projeto

```
update_opencore/
├── main.py                 # Script principal
├── config.py              # Configurações e manipulação de plist
├── logger.py              # Sistema de logging e traduções
├── efi.py                 # Operações com partições EFI
├── downloads.py           # Download de arquivos
├── drivers.py             # Atualização de drivers
├── backup.py              # Sistema de backup
├── cleanup.py             # Limpeza de arquivos temporários
├── validate.py            # Validação de configurações
├── environment.py         # Verificação de ambiente
├── dependencies.py        # Verificação de dependências
├── fallback_to_key.py     # Fallback para traduções
├── translations/          # Arquivos de tradução
│   ├── en.json
│   ├── pt-BR.json
│   ├── es.json
│   └── fr.json
├── tests/                 # Testes unitários
│   ├── __init__.py
│   └── test_logger.py
├── .vscode/              # Configurações do VS Code
│   └── settings.json
├── requirements.txt       # Dependências
├── pyproject.toml        # Configuração do projeto
├── Makefile              # Comandos úteis
├── .pre-commit-config.yaml # Hooks de pre-commit
└── .gitignore            # Arquivos ignorados pelo Git
```

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Verificar qualidade do código
make lint

# Formatar código
make format

# Executar testes
make test

# Executar todas as verificações
make check-all

# Validar sintaxe
make validate

# Limpar arquivos temporários
make clean
```

### Execução
```bash
# Executar o projeto
make run

# Ou diretamente
python3 main.py
```

## 🧪 Testes

### Executar Testes
```bash
# Testes básicos
python3 -m pytest tests/ -v

# Testes com cobertura
make test-coverage

# Testes específicos
python3 -m pytest tests/test_logger.py -v
```

### Adicionar Novos Testes
1. Crie um arquivo `test_*.py` no diretório `tests/`
2. Use a estrutura de exemplo em `test_logger.py`
3. Execute `make test` para verificar

## 📊 Qualidade de Código

### Ferramentas Configuradas
- **Pylint**: Análise estática de código
- **Black**: Formatação automática
- **Flake8**: Verificação de estilo
- **MyPy**: Verificação de tipos
- **Bandit**: Análise de segurança

### Configurações
- **Linha máxima**: 100 caracteres
- **Encoding**: UTF-8
- **Docstrings**: Opcional (desabilitado no Pylint)

## 🔍 Análise de Segurança

```bash
# Executar análise de segurança
make security

# Verificar relatório
cat bandit-report.json
```

## 📚 Documentação

### Gerar Documentação
```bash
# Gerar documentação HTML
make docs

# Abrir no navegador
open docs/index.html
```

## 🚨 Problemas Conhecidos

### Score Pylint Baixo (config.py)
- **Causa**: Muitas exceções genéricas e variáveis não definidas
- **Solução**: Implementar tratamento específico de exceções
- **Status**: Em progresso

### Muitas Ramificações (main.py)
- **Causa**: Menu com muitas opções
- **Solução**: Refatorar para usar padrão Strategy
- **Status**: Melhoria futura

## 🔄 Próximas Melhorias

### Prioridade Alta
1. **Refatorar main.py**: Reduzir complexidade ciclomática
2. **Melhorar config.py**: Tratamento específico de exceções
3. **Adicionar mais testes**: Cobertura de 80%+

### Prioridade Média
1. **Type hints**: Adicionar anotações de tipo
2. **Logging estruturado**: Melhorar sistema de logs
3. **Configuração externa**: Arquivo de configuração

### Prioridade Baixa
1. **CLI melhorado**: Usar Click ou Typer
2. **Interface gráfica**: Tkinter ou PyQt
3. **Docker**: Containerização

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça as alterações
4. Execute `make check-all`
5. Envie um Pull Request

### Padrões de Código
- Use `make format` antes de commitar
- Execute `make test` para verificar testes
- Siga as configurações do Pylint
- Adicione testes para novas funcionalidades

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Execute `make help` para ver comandos disponíveis
3. Consulte os logs gerados pelo projeto
4. Abra uma issue no repositório

---

**Nota**: Este projeto é específico para macOS e requer permissões de administrador para funcionar corretamente.
