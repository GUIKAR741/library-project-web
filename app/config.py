"""Arquivo de Configurações."""


class Config:
    """Classe Base das Configurações."""

    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = 'guilherme'
    MYSQL_DATABASE_PASSWORD = 'qwe123'
    MYSQL_DATABASE_DB = 'syml'
    MYSQL_DATABASE_CHARSET = 'utf8'


class development(Config):
    """Configurações de Desenvolvimento."""

    DEBUG = True


class production(Config):
    """Configurações de Produção."""

    DEBUG = False
