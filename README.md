<img src="http://www.bayer.com.br/themes/custom/bayer_cpa/logo.svg" alt="logo_bayer" width="80" height="80" />

## AuthServices API - Python - v1.9

#### Bayer - Sistema de Autenticacao de Usuarios

## Pre-Requisitos
* Instalar o Python 3.9
* Instalar o Editor (Visual Studio Code / PyCharm)
* Instalar o Microsoft C++ Build Tools - [download](https://visualstudio.microsoft.com/pt-br/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16#)

## Passo a passo para montar o ambiente:
1. Gerar token de acesso atraves da url
~~~git
https://github.platforms.engineering/settings/tokens
~~~
2. Abrir o terminal
3. Navegar ate a pasta do repositorio escolhido
4. Baixar o repositorio informando USUARIO e TOKEN
~~~git
git clone https://USUARIO:TOKEN@github.platforms.engineering/GDEVS/AuthServicesAPI.git
~~~
5. Entrar na pasta do projeto
6. Restaurar os pacotes do arquivo **requirements.txt**
~~~python
pip install -r requirements.txt
~~~
>caso nao queira utilizar o cache para instalar os pacotes, pode utilizar o comando.
```
pip --no-cache-dir install -r requirements.txt
```
7. Rodar a aplicacao
~~~
python AuthServices.py
~~~
## Comandos Python (Auxiliares):
Comando   | Descricao
--------- | ------
pip uninstall -r requirements.txt | Remover os pacotes instalados
pip freeze | Mostrar pacotes instalados
pip install --proxy http://CWID:SENHA@sap-proxy.la.bayer.cnb:80 NOME_PACOTE | Instalar um pacote informando o proxy

## Comandos GIT (Auxiliares):
~~~
REPOSITORIO_REMOTO:
https://USUARIO@github.platforms.engineering/GDEVS/AuthServicesAPI.git
Alterar a variavel USUARIO utilizado na URL acima 
~~~
Comando   | Descricao
--------- | ------
git pull REPOSITORIO_REMOTO | Atualiza o seu repositorio local com os dados do repositorio remoto
git add . | Adiciona os arquivos alterados na branch local
git commit -m 'minha mensagem' | Faz o commit das alteracoes no repositorio local
git push origin master | Envia as alteracoes do repositorio local para o repositorio online

## Ambientes:
Ambiente   | URL
--------- | ------
LOCAL | http://localhost:5000/
DEV | http://by0v0n:8033/
QA | http://authservicesapiqa.bayer.br.intranet/
PROD | http://by0rgy:8033/
