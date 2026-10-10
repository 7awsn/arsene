"""Carregamento da configuracao a partir do config.yaml."""

from pathlib import Path

import yaml


# Valores padrao usados quando o arquivo nao define uma secao
DefaultConfig = {
    "backend": "local",
    "local": {"dataset": "data/sample_records.json"},
    "elastic": {
        "host": "http://localhost:9200",
        "index": "arsene-records",
        "username": "",
        "password": "",
        "api_key": "",
        "verify_certs": False,
    },
    "api": {"endpoint": "", "token": "", "timeout": 15},
    "ui": {"max_results": 50, "mask_passwords": True},
}


def LoadConfig(ConfigPath="config.yaml"):
    """Le o config.yaml e aplica os padroes para chaves ausentes."""

    Path_ = Path(ConfigPath)
    if not Path_.exists():
        return dict(DefaultConfig)

    with Path_.open("r", encoding="utf-8") as Handle:
        Loaded = yaml.safe_load(Handle) or {}

    # Combina os padroes com o que foi definido pelo usuario
    Merged = dict(DefaultConfig)
    for Key, Value in Loaded.items():
        if isinstance(Value, dict) and isinstance(Merged.get(Key), dict):
            Section = dict(Merged[Key])
            Section.update(Value)
            Merged[Key] = Section
        else:
            Merged[Key] = Value
    return Merged
