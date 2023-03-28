## **Setup**

Recomendado instalar o [Pyenv](https://github.com/pyenv-win/pyenv-win), para gerenciar as versões do python.
Para instalar a versão 3.8.10 necessária para o projeto, basta rodar o comando `pyenv install 3.8.10` no terminal.
Instalar o [Face Recognition](https://www.geeksforgeeks.org/how-to-install-face-recognition-in-python-on-windows/) (instalar depois de ativar o ambiente virtual)

Temos duas opções para configurar o ambiente:

- Rodando os comandos um por vez

```bash
access-control-project> python -m pip install virtualenv                       # Instala a biblioteca de ambiente virtual
access-control-project> virtualenv .venv                                       # Cria o ambiente virtual
access-control-project> .venv\Scripts\activate                                 # Ativa o ambiente virtual
(.venv) access-control-project> python -m pip install pip-tools                # Instala o pip-tools

Windows:
(.venv) access-control-project> pip-compile --upgrade --resolver=backtracking  # Gera o requirements.txt (Se for Windows)
(.venv) access-control-project> pip-sync                                       # Instala as dependências (Se for Windows)

Linux:
(.venv) access-control-project> pip-compile requirements_linux.in --upgrade --resolver=backtracking # Gera o requirements.txt (Se for Linux)
(.venv) access-control-project> pip-sync requirements_linux.txt                # Instala as dependências (Se for Linux)
```

Tudo junto, para facilitar:

```bash
# Windows CMD e Powershell
> python -m pip install virtualenv & virtualenv .venv & .venv\Scripts\activate & python -m pip install pip-tools & pip-compile --upgrade --resolver=backtracking & pip-sync
> python -m pip install virtualenv ; virtualenv .venv ; .venv\Scripts\activate ; python -m pip install pip-tools ; pip-compile --upgrade --resolver=backtracking ; pip-sync

# Windows Powershell e Linux
> python -m pip install virtualenv ; virtualenv .venv ; .venv\Scripts\activate ; python -m pip install pip-tools ; pip-compile requirements_linux.in --upgrade --resolver=backtracking ; pip-sync requirements_linux.txt
```

- Rodando o script `start.bat` com a opção Setup do ambiente

---

## **Requirements**

Temos duas opções para instalar as dependências:

- Rodando os comandos um por vez

```bash
access-control-project> .venv\Scripts\activate                                 # Ativa o ambiente virtual

Windows:
(.venv) access-control-project> pip-compile --upgrade --resolver=backtracking  # Gera o requirements.txt (Se for Windows)
(.venv) access-control-project> pip-sync                                       # Instala as dependências (Se for Windows)

Linux:
(.venv) access-control-project> pip-compile requirements_linux.in --upgrade --resolver=backtracking # Gera o requirements.txt (Se for Linux)
(.venv) access-control-project> pip-sync requirements_linux.txt                # Instala as dependências (Se for Linux)
```

Tudo junto, para facilitar:

```bash
# Windows CMD e Powershell
> .venv\Scripts\activate & pip-compile --upgrade --resolver=backtracking & pip-sync
> .venv\Scripts\activate ; pip-compile --upgrade --resolver=backtracking ; pip-sync

# Linux
> .venv\Scripts\activate ; pip-compile requirements_linux.in --upgrade --resolver=backtracking ; pip-sync requirements_linux.txt
```

- Rodando o script `start.bat` com a opção Atualizar dependencias

---

## **Observações**

Caso saia do ETL e queiram codar outra coisa, tem que rodar o comando `deactivate` no terminal para fechar o ambiente virtual.<br>
Fica bem visivel no terminal se você está com o ambiente aberto ou não, indicado pelo nome dela antes do caminho da pasta:
Ex:

```bash
(.venv) access-control-project>            # Ativo
(.venv) access-control-project> deactivate # Comando de desativar
access-control-project>                    # Não ativo
```

Outro ponto importante é verificar se o ambiente virtual está ativo antes de rodar os comandos de requerimento, caso não esteja, ele vai desinstalar/atualizar as dependências do seu ambiente global, o que pode causar problemas.

## **Verificações pre-commit**

Conseguimos verificar se o código está seguindo os padrões de código com o pre-commit. Ele é um framework que executa scripts antes de cada commit, e se algum deles falhar, o commit não é realizado.<br>
Para instalar o pre-commit, basta rodar o comando `pre-commit install` no terminal (dentro do ambiente virtual).<br>
Para rodar o pre-commit manualmente, basta rodar o comando `pre-commit run --all-files` no terminal.

## **Testes**

Para rodar os testes, basta rodar o comando `pytest` no terminal.
