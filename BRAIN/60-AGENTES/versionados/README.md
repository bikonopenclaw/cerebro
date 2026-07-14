# Agentes versionados no Brain

Este diretório guarda snapshots controlados do código-fonte operacional dos agentes Kowalski, Darth Vader e Robotnik.

## Objetivo

- Trazer skills, scripts, documentação operacional e configuração não sensível dos agentes para o Git do Brain.
- Permitir auditoria, diff e rollback básico das mudanças importantes.
- Evitar depender apenas dos workspaces vivos dos agentes, que não são repositórios Git próprios.

## O que entra

- `agents/<agente>/agent`: definição e skills instaladas do agente.
- `workspaces/<agente>/`: arquivos operacionais de código, skills, scripts, docs, templates e exemplos não sensíveis.
- `workspaces/main/skills`: skills globais aprovadas do workspace principal.
- Manifesto com data, origem e regras de exclusão.

## O que não entra

- `.env`, `.env.*`, tokens OAuth, credenciais, segredos, senhas e chaves.
- Sessões, caches, `__pycache__`, `.openclaw`, logs, locks e artefatos temporários.
- Relatórios finais de clientes, PDFs, imagens, documentos binários e pacotes gerados.
- Dados brutos sensíveis de clientes ou respostas completas de APIs.

## Regra

Se um arquivo for necessário para entender ou reconstruir uma automação, ele deve entrar sanitizado ou como `.example`.
Se expõe segredo, cliente ou artefato operacional final, fica fora do Git.
