"""Modelo de registro e mapeamento de campos pesquisaveis."""

from dataclasses import dataclass, field


# Mapeia o nome do campo usado na busca para o atributo do registro
FieldMap = {
    "username": "Username",
    "email": "Email",
    "password": "Password",
    "name": "Name",
    "url": "Url",
    "cpf": "Cpf",
}

SearchableFields = tuple(FieldMap.keys())


@dataclass
class Record:
    """Representa uma entrada de dado retornada por qualquer backend."""

    Username: str = ""
    Email: str = ""
    Password: str = ""
    Name: str = ""
    Url: str = ""
    Cpf: str = ""
    Source: str = ""

    @classmethod
    def FromDict(cls, Raw):
        # Aceita chaves ausentes sem quebrar a leitura do dataset
        return cls(
            Username=Raw.get("Username", ""),
            Email=Raw.get("Email", ""),
            Password=Raw.get("Password", ""),
            Name=Raw.get("Name", ""),
            Url=Raw.get("Url", ""),
            Cpf=Raw.get("Cpf", ""),
            Source=Raw.get("Source", ""),
        )

    def Get(self, FieldName):
        # Retorna o valor de um campo pesquisavel pelo nome em minusculas
        Attribute = FieldMap.get(FieldName)
        if Attribute is None:
            return ""
        return getattr(self, Attribute, "")
