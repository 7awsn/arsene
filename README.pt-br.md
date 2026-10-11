# Arsene

[English](README.md) | **Português**

Arsene e um console de OSINT para terminal. Ele permite fazer buscas
combinadas sobre identificadores comuns (username, email, senha, nome, url e
cpf) atraves de uma linguagem de consulta pequena e expressiva.

O projeto acompanha um dataset ficticio apenas para demonstracao. Ele nao
inclui e nao deve ser usado com dados pessoais reais.

```
    _    ____  ____  _____ _   _ _____
   / \  |  _ \/ ___|| ____| \ | | ____|
  / _ \ | |_) \___ \|  _| |  \| |  _|
 / ___ \|  _ < ___) | |___| |\  | |___
/_/   \_\_| \_\____/|_____|_| \_|_____|
```

## Recursos

- Linguagem de consulta combinada com operadores de inclusao e exclusao.
- Correspondencia por substring e por expressao regular em qualquer campo.
- Tres backends plugaveis: JSON local, Elasticsearch e API HTTP.
- Interface de terminal limpa, com tabela de resultados e mascaramento de senha.

## Linguagem de consulta

```
campo:valor + campo:%valor - campo:valor
```

- Campos: `username`, `email`, `password`, `name`, `url`, `cpf`.
- `+` marca um termo obrigatorio e e o padrao quando o operador e omitido.
- `-` marca um termo de exclusao.
- Um `%` no inicio do valor troca o termo de substring para regex.

Exemplo:

```
url:google.com + email:%@uol.com - username:pedrotuto
```

Retorna registros cuja url contem google.com, cujo email casa com a regex
`@uol.com` e cujo username nao contem pedrotuto.

## Instalacao

```bash
pip install -r requirements.txt
```

Os pacotes `elasticsearch` e `requests` so sao necessarios para os backends
`elastic` e `api`.

## Execucao

```bash
python -m arsene
```

Dentro do console:

- `:help` mostra a sintaxe da consulta.
- `:backend` troca o backend ativo.
- `:clear` limpa a tela.
- `:exit` encerra a sessao.

## Backends

Escolha o backend ativo no `config.yaml` pela chave `backend`.

| Backend  | Quando usar                                             |
|----------|--------------------------------------------------------|
| `local`  | Testes rapidos e demos com o dataset JSON incluido.    |
| `elastic`| Grandes volumes que precisam de respostas rapidas.     |
| `api`    | Seu proprio servico de busca exposto por HTTP.         |

Preencha apenas a secao correspondente ao backend que pretende usar.

## Estrutura do projeto

```
arsene/
  banner.py        banner e identidade visual
  cli.py           interface interativa de terminal
  config.py        carregamento da configuracao
  engine.py        fabrica de backends e orquestracao da busca
  models.py        modelo de registro e campos pesquisaveis
  query.py         parser da linguagem de consulta
  backends/        backends local, elasticsearch e api
data/
  sample_records.json   dataset ficticio para demos
```
