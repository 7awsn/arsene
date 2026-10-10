"""Parser da linguagem de busca combinada do Arsene.

Formato aceito:
    campo:valor + campo:%valor - campo:valor

Operadores:
    +  termo obrigatorio (padrao quando omitido)
    -  termo de exclusao

O prefixo % no valor ativa correspondencia por expressao regular.
"""

import re
from dataclasses import dataclass

from .models import SearchableFields


# Caractere que, no inicio do valor, ativa a busca por regex
RegexMarker = "%"

# Captura o operador opcional, o nome do campo e os dois pontos iniciais
FieldPattern = re.compile(r"([+\-])?\s*([a-zA-Z]+)\s*:")


class QueryError(Exception):
    """Erro de sintaxe ou campo invalido na consulta."""


@dataclass
class Criterion:
    """Um unico criterio de busca ja interpretado."""

    Field: str
    Value: str
    IsRegex: bool
    Negate: bool


def ParseQuery(Text):
    """Converte a string de consulta em uma lista de criterios."""

    Cleaned = (Text or "").strip()
    if not Cleaned:
        raise QueryError("Consulta vazia.")

    Matches = list(FieldPattern.finditer(Cleaned))
    if not Matches:
        raise QueryError("Nenhum campo valido encontrado. Use o formato campo:valor.")

    Criteria = []
    for Index, Match in enumerate(Matches):
        Operator = Match.group(1)
        Field = Match.group(2).lower()

        # O valor vai do fim deste campo ate o inicio do proximo termo
        Start = Match.end()
        End = Matches[Index + 1].start() if Index + 1 < len(Matches) else len(Cleaned)
        Value = Cleaned[Start:End].strip()

        if Field not in SearchableFields:
            raise QueryError(f"Campo desconhecido: '{Field}'.")
        if not Value:
            raise QueryError(f"O campo '{Field}' esta sem valor.")

        # Prefixo % indica que o restante do valor e uma expressao regular
        IsRegex = Value.startswith(RegexMarker)
        if IsRegex:
            Value = Value[len(RegexMarker):].strip()
            if not Value:
                raise QueryError(f"O campo '{Field}' esta com uma regex vazia.")
            try:
                re.compile(Value)
            except re.error as Error:
                raise QueryError(f"Regex invalida em '{Field}': {Error}")

        Criteria.append(
            Criterion(
                Field=Field,
                Value=Value,
                IsRegex=IsRegex,
                Negate=(Operator == "-"),
            )
        )

    return Criteria
