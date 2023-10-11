## Setup

Python 3.10 needs to be installed.

## pipenv:
```
pip3 install pipenv
```

## Install packages:
```
pipenv install
```

## Install GLPK:
```
sudo apt install glpk-utils
```

## Enter venv:
```
pipenv shell
```

## Execute server:
```
python3 manage.py runserver
```

## Conventions

Variable and function declaration: Camel case, starting with a lowercase letter.
Type declaration: Camel case, starting with an uppercase letter.

Indentation: 4 spaces.

## Installation and Database Setup

Before proceeding, it is necessary to install MySQL:
```
sudo apt install libmysqlclient-dev
```

It may also be necessary to:
```
sudo apt install mysql-client-core-8.0
```

To install the MySQL server, you may need to:
```
sudo apt-get install mysql-server
```

## WSL case

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

It is necessary to run the following commands every time you restart the WSL:

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

Proceed to README-MYSQL