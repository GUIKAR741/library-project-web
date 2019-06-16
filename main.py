"""Executar Servidor Flask."""
import os


if __name__ == "__main__":
    os.environ["FLASK_APP"] = "app:start_app"
    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_DEBUG"] = "True"
    print(os.system("flask run"))
