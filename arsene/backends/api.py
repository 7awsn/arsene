"""Backend de API externa, para quem prefere uma fonte propria via HTTP."""

from .base import SearchBackend
from ..models import Record


class ApiBackend(SearchBackend):
    """Envia os criterios para um endpoint HTTP e le os registros da resposta."""

    Name = "api"

    def __init__(self, Settings):
        self.Endpoint = Settings.get("endpoint", "")
        self.Token = Settings.get("token", "")
        self.Timeout = Settings.get("timeout", 15)
        if not self.Endpoint:
            raise ValueError(
                "Endpoint da API nao configurado. Preencha 'api.endpoint' no config.yaml."
            )

    def Describe(self):
        return f"api ({self.Endpoint})"

    def Search(self, Criteria, Limit):
        # Importado aqui para manter a dependencia opcional
        import requests

        Payload = {
            "criteria": [
                {
                    "field": Item.Field,
                    "value": Item.Value,
                    "regex": Item.IsRegex,
                    "negate": Item.Negate,
                }
                for Item in Criteria
            ],
            "limit": Limit,
        }
        Headers = {"Content-Type": "application/json"}
        if self.Token:
            Headers["Authorization"] = f"Bearer {self.Token}"

        Response = requests.post(
            self.Endpoint, json=Payload, headers=Headers, timeout=self.Timeout
        )
        Response.raise_for_status()

        # Espera uma lista de registros em 'results' ou na raiz da resposta
        Data = Response.json()
        RawItems = Data.get("results", Data) if isinstance(Data, dict) else Data
        return [Record.FromDict(Item) for Item in RawItems]
