# Otimizador de Calendário (em desenvolvimento)

## Escopo do sistema (objetivo e principais features):
Este projeto consiste em uma interface para otimizar uma escolha de atividades a serem realizadas, de acordo com as preferências do usuário e restrições fornecidas. O usuário especifica as atividades dentre as quais gostaria de escolher e os horários que pode fazê-las, além de outras possíveis restrições (ter ao menos 1h de tempo livre por dia, não fazer duas atividades ao mesmo tempo). Além disso, é possível associar um valor subjetivo a cada atividade, e este programa computará qual escolha de atividades maximiza a soma dos valores sem violar as restrições dadas.

Com isso, é possível por exemplo, escolher dentre vários cursos com horários conflitantes, um conjunto de cursos sem conflito de horário cujo preço total fica o mais barato possível. Um exemplo mais complexo: o usuário pode ser o departamento de uma faculdade, que gostaria de maximizar a quantidade de disciplinas ofertadas num semestre sem conflito de sala e de horários, e sem que nenhum professor trabalhe por mais que 8 horas por dia.

Este projeto está sendo desenvolvido como trabalho prático para a disciplina de Engenharia de Software, da Universidade Federal de Minas Gerais (UFMG).


## Membros da equipe e papel:
Ana Luiza - Backend 

Artur Gaspar - Fullstack 

Denilson Martins - Backend 

Vinicius Bonfim - Front End 

## Tecnologias (linguagem, frameworks e BD)
Backend: Python (Django)

Banco de Dados: MySQL

Resolvedor de Programação Inteira: GLPK

Frontend: Python (Django)


## Backlog do produto:


1) Como usuário, gostaria de CRUD (Create, Read, Update, Delete) atividades no sistema (horário, local, pessoa envolvida, valor associado).

2) Como usuário, gostaria de poder especificar alternativas de horários, locais e Indivíduos para cada atividade, além das minhas preferências de valor de cada atividade.

3) Como usuário, gostaria de descobrir a escolha ótima de atividades possíveis de fazer segundo minhas preferências e restrições.

4) Como usuário, gostaria de poder exportar e importar os dados das minhas atividades e de escolhas ótimas.

5) Como usuário, gostaria de dar acesso às minhas atividades e escolhas ótimas para outros usuários (leitura e/ou edição).

6) Como admin, gostaria de poder limitar a quantidade de recursos disponíveis para cada usuário.

7) Como admin, gostaria de poder banir e readicionar usuários.

8) Como usuário, gostaria de visualizar minhas atividades em formato de calendário.

9) Como usuário, gostaria de exportar minhas atividades para o Google Calendar.

10) Como usuário, gostaria de configurar atividades de escopo semanal, mensal ou anual.



## Backlog da sprint:

Histórias 1, 2, 3 e 4 do Backlog do produto.


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

Se der tudo certo, será possível acessar o mysql. Talvez seja necessário sudo:
```
mysql -u root -p
```

A partir deste terminal crie um um novo banco de dados, crie um novo usuário e dê permissões à ele.
```sql
CREATE DATABASE nome_do_seu_banco_de_dados;
CREATE USER 'seu_usuario'@'localhost' IDENTIFIED BY 'sua_senha';
GRANT ALL PRIVILEGES ON nome_do_seu_banco_de_dados.* TO 'seu_usuario'@'localhost';
```

Pode ser necessário:
```sql
CREATE DATABASE nome_do_seu_banco_de_dados CHARACTER SET = utf8 COLLATE utf8_general_ci;
```

No caso para o exemplo de crud básico:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teste',  # substituir em nome_do_seu_banco_de_dados
        'USER': 'teste',  # substituir em seu_usuario
        'PASSWORD': '00000000',  # substituir em sua_senha
        'HOST': 'localhost',
        'PORT': ''
    }
}
```

E para o database principal:
```python
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'otimizador_db',
        'USER': 'usuario',
        'PASSWORD': 'engsoft@123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
```

Assim é possível entrar no mysql com outro usuário:
```
mysql -u teste -p
```
Ao digitar a senha corretamente, é esperado que você tenha acesso ao terminal do mysql.


Após serem feitas alterações relacionadas ao banco de dados:
```
python manage.py makemigrations
python manage.py migrate
```
