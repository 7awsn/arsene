"""Backend local baseado em arquivo JSON, usado para testes e demonstracao."""

import json
import re
from pathlib import Path

from .base import SearchBackend
from ..models import Record


class LocalBackend(SearchBackend):
    """Carrega um dataset local e filtra os registros em memoria."""

    Name = "local"

    def __init__(self, Settings):
        DatasetPath = Settings.get("dataset", "data/sample_records.json")
        self.DatasetPath = Path(DatasetPath)
        self.Records = self._LoadDataset()

    def _LoadDataset(self):
        # Le o dataset do disco e converte cada item em Record
        if not self.DatasetPath.exists():
            raise FileNotFoundError(f"Dataset nao encontrado: {self.DatasetPath}")
        with self.DatasetPath.open("r", encoding="utf-8") as Handle:
            RawItems = json.load(Handle)
        return [Record.FromDict(Item) for Item in RawItems]

    def Describe(self):
        return f"local ({len(self.Records)} registros)"

    def Search(self, Criteria, Limit):
        Results = []
        for Entry in self.Records:
            if self._Matches(Entry, Criteria):
                Results.append(Entry)
                if Limit and len(Results) >= Limit:
                    break
        return Results

    def _Matches(self, Entry, Criteria):
        # Todos os criterios precisam ser satisfeitos (semantica AND)
        for Item in Criteria:
            FieldValue = Entry.Get(Item.Field)
            Hit = self._CheckField(FieldValue, Item)
            if Item.Negate and Hit:
                return False
            if not Item.Negate and not Hit:
                return False
        return True

    def _CheckField(self, FieldValue, Item):
        if Item.IsRegex:
            return re.search(Item.Value, FieldValue, re.IGNORECASE) is not None
        # Busca simples por substring, ignorando maiusculas e minusculas
        return Item.Value.lower() in FieldValue.lower()
