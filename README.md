# Arsene

**English** | [Português](README.pt-br.md)

Arsene is a terminal based OSINT console. It lets you run combined lookups
across common identifiers (username, email, password, name, url and cpf)
through a small and expressive query language.

The project ships with a fictitious dataset for demonstration only. It does
not include and is not meant to handle any real personal data.

```
    _    ____  ____  _____ _   _ _____
   / \  |  _ \/ ___|| ____| \ | | ____|
  / _ \ | |_) \___ \|  _| |  \| |  _|
 / ___ \|  _ < ___) | |___| |\  | |___
/_/   \_\_| \_\____/|_____|_| \_|_____|
```

## Features

- Combined query language with inclusion and exclusion operators.
- Substring and regular expression matching on any field.
- Three pluggable backends: local JSON, Elasticsearch and HTTP API.
- Clean terminal interface with a results table and password masking.

## Query language

```
field:value + field:%value - field:value
```

- Fields: `username`, `email`, `password`, `name`, `url`, `cpf`.
- `+` marks a required term and is the default when the operator is omitted.
- `-` marks an exclusion term.
- A `%` at the start of the value switches a term from substring to regex matching.

Example:

```
url:google.com + email:%@uol.com - username:pedrotuto
```

Returns records whose url contains google.com, whose email matches the regex
`@uol.com` and whose username does not contain pedrotuto.

## Install

```bash
pip install -r requirements.txt
```

The `elasticsearch` and `requests` packages are only required for the
`elastic` and `api` backends.

## Run

```bash
python -m arsene
```

Inside the console:

- `:help` shows the query syntax.
- `:backend` switches the active backend.
- `:clear` clears the screen.
- `:exit` ends the session.

## Backends

Pick the active backend in `config.yaml` through the `backend` key.

| Backend  | When to use                                            |
|----------|--------------------------------------------------------|
| `local`  | Quick tests and demos using the bundled JSON dataset.  |
| `elastic`| Large datasets that need fast responses.               |
| `api`    | Your own search service exposed over HTTP.             |

Fill only the section that matches the backend you plan to use.

## Project layout

```
arsene/
  banner.py        banner and visual identity
  cli.py           interactive terminal interface
  config.py        configuration loading
  engine.py        backend factory and search orchestration
  models.py        record model and searchable fields
  query.py         query language parser
  backends/        local, elasticsearch and api backends
data/
  sample_records.json   fictitious dataset for demos
```
