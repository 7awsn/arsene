"""Backend Elasticsearch, indicado para grandes volumes e respostas rapidas."""

from .base import SearchBackend
from ..models import Record


def BuildQuery(Criteria):
    """Monta o corpo de uma query booleana a partir dos criterios."""

    Must = []
    MustNot = []
    for Item in Criteria:
        if Item.IsRegex:
            Clause = {
                "regexp": {
                    Item.Field: {"value": Item.Value, "case_insensitive": True}
                }
            }
        else:
            # Wildcard permite correspondencia parcial no valor informado
            Clause = {
                "wildcard": {
                    Item.Field: {
                        "value": f"*{Item.Value}*",
                        "case_insensitive": True,
                    }
                }
            }
        if Item.Negate:
            MustNot.append(Clause)
        else:
            Must.append(Clause)

    return {"bool": {"must": Must, "must_not": MustNot}}


class ElasticBackend(SearchBackend):
    """Consulta um indice Elasticsearch previamente populado."""

    Name = "elastic"

    def __init__(self, Settings):
        self.Settings = Settings
        self.Index = Settings.get("index", "arsene-records")
        self.Client = self._Connect(Settings)

    def _Connect(self, Settings):
        # Importado aqui para nao exigir a dependencia quando nao for usada
        from elasticsearch import Elasticsearch

        Host = Settings.get("host", "http://localhost:9200")
        ApiKey = Settings.get("api_key") or None
        Username = Settings.get("username") or None
        Password = Settings.get("password") or None
        VerifyCerts = bool(Settings.get("verify_certs", False))

        if ApiKey:
            return Elasticsearch(Host, api_key=ApiKey, verify_certs=VerifyCerts)
        if Username and Password:
            return Elasticsearch(
                Host, basic_auth=(Username, Password), verify_certs=VerifyCerts
            )
        return Elasticsearch(Host, verify_certs=VerifyCerts)

    def Describe(self):
        return f"elastic ({self.Index})"

    def Search(self, Criteria, Limit):
        Body = BuildQuery(Criteria)
        Response = self.Client.search(
            index=self.Index, query=Body, size=Limit or 50
        )
        Hits = Response.get("hits", {}).get("hits", [])
        return [Record.FromDict(Hit.get("_source", {})) for Hit in Hits]
