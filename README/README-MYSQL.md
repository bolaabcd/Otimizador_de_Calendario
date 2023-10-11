If everything goes well, you will be able to access MySQL. You may need to use "sudo."
```
mysql -u root -p
```

As you enter the correct password, you should have access to the MySQL terminal.


From this terminal, create a new database, create a new user, and grant permissions to that user.

For configuring MySQL with Django, you may follow this video: https://www.youtube.com/watch?v=ZGGiBGTv9do

1. `CREATE DATABASE otimizador_db CHARACTER SET = utf8 COLLATE utf8_general_ci;`

2. `CREATE USER 'usuario'@'localhost' IDENTIFIED WITH mysql_native_password BY 'engsoft@123';`

3. `GRANT ALL PRIVILEGES ON otimizador_db.* TO 'usuario'@'localhost' WITH GRANT OPTION;`


After making changes related to the database:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
