# Library Project WEB
Site Biblioteca

## Bibliotecas Utilizadas
- Flask
- Flask-MySQL

## Como rodar esse projeto

### Instale as dependencias com o comando

```sh
pip install -r requirements.txt 
```

### Execute o projeto

```sh
export FLASK_APP=app:start_app
export FLASK_ENV=Development
export FLASK_DEBUG=True

flask run
```
ou
```sh
./run.sh
```