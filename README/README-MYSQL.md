Se der tudo certo, será possível acessar o mysql. Talvez seja necessário sudo:
```
mysql -u root -p
```

Assim é possível entrar no mysql com outro usuário:
```
mysql -u teste -p
```
Ao digitar a senha corretamente, é esperado que você tenha acesso ao terminal do mysql.


A partir deste terminal crie um um novo banco de dados, crie um novo usuário e dê permissões à ele.

Para a configuração do mysql com django, segui esse vídeo https://www.youtube.com/watch?v=ZGGiBGTv9do

1.
CREATE DATABASE otimizador_db CHARACTER SET = utf8mb4 COLLATE utf8mb4_unicode_ci;
2.
CREATE USER 'usuario'@'localhost' IDENTIFIED WITH mysql_native_password BY 'engsoft@123';
3.
GRANT ALL PRIVILEGES ON otimizador_db.* TO 'usuario'@'localhost' WITH GRANT OPTION;


Após serem feitas alterações relacionadas ao banco de dados:
```
python manage.py makemigrations
python manage.py migrate
```
