"""Fabrica de backends e orquestracao da busca."""

from .backends.local import LocalBackend
from .backends.elastic import ElasticBackend
from .backends.api import ApiBackend


BackendRegistry = {
    "local": LocalBackend,
    "elastic": ElasticBackend,
    "api": ApiBackend,
}


def CreateBackend(Config, Override=None):
    """Instancia o backend definido na configuracao ou no parametro Override."""

    Name = (Override or Config.get("backend", "local")).lower()
    BackendClass = BackendRegistry.get(Name)
    if BackendClass is None:
        Available = ", ".join(BackendRegistry.keys())
        raise ValueError(f"Backend desconhecido: '{Name}'. Opcoes: {Available}.")

    Settings = Config.get(Name, {})
    return BackendClass(Settings)


def RunSearch(Backend, Criteria, Limit):
    """Executa a busca no backend informado e devolve os registros."""

    return Backend.Search(Criteria, Limit)
