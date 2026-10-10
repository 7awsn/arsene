"""Contrato comum a todos os backends de busca."""

from abc import ABC, abstractmethod


class SearchBackend(ABC):
    """Interface implementada por cada fonte de dados."""

    Name = "base"

    @abstractmethod
    def Search(self, Criteria, Limit):
        """Recebe a lista de criterios e devolve uma lista de Record."""
        raise NotImplementedError

    def Describe(self):
        # Texto curto exibido no cabecalho da interface
        return self.Name
