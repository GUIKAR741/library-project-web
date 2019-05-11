# Library Project WEB
Site Biblioteca

## Bibliotecas Utilizadas
- Flask
- Flask-MySQL

## Como rodar esse projeto

### Instale as dependencias com o comando

```sh
pip install pipenv
pipenv install --dev
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

## Como rodar os testes
```sh
tox
```