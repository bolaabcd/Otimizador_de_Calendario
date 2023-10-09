## Setup

Necessário python 3.10

pipenv:
```
pip3 install pipenv
```

Instalar pacotes
```
pipenv install
```

Instalar GLPK
```
sudo apt install glpk-utils
```

Entrar no venv:
```
pipenv shell
```

Executar server:
```
python3 manage.py runserver
```

## Convenções

Declaração de variáveis e funções: Camel case, primeira letra minúscula
Declaração de tipos: Camel case, primeira letra maiúscula

Identação: 4 espaços


## Instalação e setup do Banco de Dados

É necessário antes instalar o mysql:
```
sudo apt install libmysqlclient-dev
```

Pode ser preciso também:
```
sudo apt install mysql-client-core-8.0
```

Para instalar o servidor mysql pode ser preciso:
```
sudo apt-get install mysql-server
```

## CASO WSL

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

necessário rodar os seguintes códigos toda vez que reiniciar a wsl:

1.
```
ls ~/.ssh
```

2.
```
eval $(ssh-agent -s)
```

3.
```
ssh-add ~/.ssh/id_ed25519
```

4.
```
ssh-add -l
```

Siga para README-MYSQL