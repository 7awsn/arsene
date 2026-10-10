"""Interface de terminal do Arsene, construida sobre a biblioteca rich."""

import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

from . import Version
from .banner import BannerArt, Tagline
from .config import LoadConfig
from .engine import CreateBackend, RunSearch
from .query import ParseQuery, QueryError
from .models import SearchableFields


Theme = {
    "accent": "bold green",
    "dim": "grey50",
    "danger": "bold red",
    "field": "cyan",
    "value": "white",
}


def RenderBanner(ConsoleOut):
    # Desenha o cabecalho com o nome e a versao do projeto
    Art = Text(BannerArt, style=Theme["accent"])
    Subtitle = Text(f"  {Tagline}  ::  v{Version}", style=Theme["dim"])
    ConsoleOut.print(Art)
    ConsoleOut.print(Subtitle)
    ConsoleOut.print()


def RenderHelp(ConsoleOut):
    # Painel de ajuda com a sintaxe da linguagem de busca
    Fields = ", ".join(SearchableFields)
    Body = Text()
    Body.append("Sintaxe\n", style=Theme["accent"])
    Body.append("  campo:valor + campo:%valor - campo:valor\n\n", style=Theme["value"])
    Body.append("Campos\n", style=Theme["accent"])
    Body.append(f"  {Fields}\n\n", style=Theme["value"])
    Body.append("Operadores\n", style=Theme["accent"])
    Body.append("  +  termo obrigatorio (padrao)\n", style=Theme["value"])
    Body.append("  -  termo de exclusao\n", style=Theme["value"])
    Body.append("  %  no inicio do valor ativa busca por expressao regular\n\n", style=Theme["value"])
    Body.append("Exemplo\n", style=Theme["accent"])
    Body.append(
        "  url:google.com + email:%@uol.com - username:pedrotuto\n\n",
        style=Theme["field"],
    )
    Body.append("Comandos\n", style=Theme["accent"])
    Body.append("  :help    mostra esta ajuda\n", style=Theme["value"])
    Body.append("  :backend troca o backend ativo\n", style=Theme["value"])
    Body.append("  :clear   limpa a tela\n", style=Theme["value"])
    Body.append("  :exit    encerra a sessao", style=Theme["value"])
    ConsoleOut.print(Panel(Body, title="ajuda", border_style=Theme["dim"]))


def MaskPassword(Value):
    # Mantem apenas os dois primeiros caracteres visiveis
    if len(Value) <= 2:
        return "*" * len(Value)
    return Value[:2] + "*" * (len(Value) - 2)


def RenderResults(ConsoleOut, Results, Elapsed, MaskPasswords):
    if not Results:
        ConsoleOut.print(
            Panel("Nenhum registro encontrado.", border_style=Theme["danger"])
        )
        return

    ResultTable = Table(
        show_lines=False,
        header_style=Theme["accent"],
        border_style=Theme["dim"],
        expand=True,
    )
    for Column in ("username", "email", "password", "name", "url", "cpf", "source"):
        ResultTable.add_column(Column, overflow="fold")

    for Entry in Results:
        PasswordValue = MaskPassword(Entry.Password) if MaskPasswords else Entry.Password
        ResultTable.add_row(
            Entry.Username,
            Entry.Email,
            PasswordValue,
            Entry.Name,
            Entry.Url,
            Entry.Cpf,
            Entry.Source,
        )

    ConsoleOut.print(ResultTable)
    Summary = Text(
        f"{len(Results)} resultado(s) em {Elapsed * 1000:.0f} ms", style=Theme["dim"]
    )
    ConsoleOut.print(Summary)


def SwitchBackend(ConsoleOut, Config, Current):
    # Permite trocar o backend em tempo de execucao
    Choice = Prompt.ask(
        Text("backend", style=Theme["field"]),
        choices=["local", "elastic", "api"],
        default=Config.get("backend", "local"),
    )
    try:
        NewBackend = CreateBackend(Config, Override=Choice)
    except Exception as Error:
        ConsoleOut.print(Panel(str(Error), border_style=Theme["danger"]))
        return Current
    ConsoleOut.print(
        Text(f"backend ativo: {NewBackend.Describe()}", style=Theme["accent"])
    )
    return NewBackend


def HandleQuery(ConsoleOut, Backend, Config, Line):
    try:
        Criteria = ParseQuery(Line)
    except QueryError as Error:
        ConsoleOut.print(Panel(str(Error), border_style=Theme["danger"]))
        return

    MaxResults = Config.get("ui", {}).get("max_results", 50)
    MaskPasswords = Config.get("ui", {}).get("mask_passwords", True)

    Started = time.perf_counter()
    try:
        Results = RunSearch(Backend, Criteria, MaxResults)
    except Exception as Error:
        ConsoleOut.print(Panel(f"Falha na busca: {Error}", border_style=Theme["danger"]))
        return
    Elapsed = time.perf_counter() - Started

    RenderResults(ConsoleOut, Results, Elapsed, MaskPasswords)


def Run():
    """Ponto de entrada do console interativo."""

    ConsoleOut = Console()
    Config = LoadConfig()

    ConsoleOut.clear()
    RenderBanner(ConsoleOut)

    try:
        Backend = CreateBackend(Config)
    except Exception as Error:
        ConsoleOut.print(Panel(str(Error), border_style=Theme["danger"]))
        return

    ConsoleOut.print(
        Text(f"backend ativo: {Backend.Describe()}", style=Theme["accent"])
    )
    ConsoleOut.print(Text("digite :help para ver a sintaxe", style=Theme["dim"]))
    ConsoleOut.print()

    while True:
        try:
            Line = Prompt.ask(Text("arsene", style=Theme["accent"])).strip()
        except (EOFError, KeyboardInterrupt):
            ConsoleOut.print()
            break

        if not Line:
            continue

        Command = Line.lower()
        if Command in (":exit", ":quit", "exit", "quit"):
            break
        if Command == ":help":
            RenderHelp(ConsoleOut)
            continue
        if Command == ":clear":
            ConsoleOut.clear()
            RenderBanner(ConsoleOut)
            continue
        if Command == ":backend":
            Backend = SwitchBackend(ConsoleOut, Config, Backend)
            continue

        HandleQuery(ConsoleOut, Backend, Config, Line)

    ConsoleOut.print(Text("sessao encerrada.", style=Theme["dim"]))
