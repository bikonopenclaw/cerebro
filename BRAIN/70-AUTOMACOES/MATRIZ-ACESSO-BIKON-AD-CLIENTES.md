# Matriz de acesso Bikon x clientes AD local

```yaml
categoria: governanca_acesso
fonte: conversa operacional com Hebert em 2026-06-23
confiabilidade: alta
ultima_revisao: 2026-06-24
tags: [bikon, entra-id, ad-local, rmm, governanca-acesso, auditoria]
```

## Finalidade

Governar quais usuários aprovados da Bikon, identificados no Entra ID, podem existir ou acessar servidores de clientes em AD local.

A matriz deve servir primeiro como base de auditoria e, somente depois de validação humana, como referência para automações futuras.

## Estado atual

- Fase atual: desenho e preenchimento da matriz.
- Entregável criado: planilha modelo em Google Sheets.
- Link registrado: `https://docs.google.com/spreadsheets/d/1DshZOW-iun4SsuZ39c7bZYS7tMgXgYs8L6rsbBRWWIM/edit?usp=drivesdk`
- Próximo passo recomendado: preencher `Usuarios_Bikon`, `Clientes`, `Servidores` e depois `Matriz_Acesso`.

## Estrutura da planilha modelo

- `README`: objetivo, fase atual e regra de segurança.
- `Usuarios_Bikon`: usuários internos aprovados, e-mail Entra ID, UPN, status, perfil e MFA.
- `Clientes`: clientes, domínio AD local, responsável e criticidade.
- `Servidores`: servidores/FQDN, IP, função, tipo AD, RMM/Ninja ID e autorização de acesso via RMM.
- `Matriz_Acesso`: vínculo usuário ↔ cliente ↔ servidor, nível de acesso, grupo autorizado, conta esperada, aprovação e validade.
- `Regras_Acao`: comportamento por condição encontrada na auditoria.
- `Auditoria_Modelo`: formato esperado para relatório de divergências.

## Decisões operacionais

- Fase 1 deve ser somente auditoria, sem criação, alteração ou desativação automática de contas.
- O primeiro script futuro deve coletar usuários/grupos dos ADs locais dos clientes via RMM e comparar com a lista aprovada da Bikon.
- Divergências devem ser reportadas, não corrigidas automaticamente na fase inicial.
- Usuário ativo no Entra ID Bikon e aprovado na matriz, mas ausente no AD local: reportar como possível criação futura.
- Usuário presente no AD local sem aprovação na matriz: reportar como acesso não autorizado ou divergência.
- Usuário Bikon inativo no Entra ID, mas ainda presente no AD local: reportar como risco crítico.
- Excesso de grupo/privilégio no AD local deve ser destacado antes de qualquer ajuste.

## Guardrails

- Não executar criação, desativação, remoção de grupo ou alteração de privilégio sem aprovação explícita.
- Não mexer automaticamente em contas que não estejam marcadas como gerenciadas pela Bikon.
- Não registrar senhas, hashes, tokens, dumps de AD, listas sensíveis completas ou inventários brutos no Brain.
- Relatórios futuros devem evitar dados desnecessários e preservar apenas evidências suficientes para decisão.

## Relações

- Empresa: `BRAIN/20-EMPRESAS/BIKON/README.md`
- Possível executor técnico futuro: Kowalski, se autorizado e restrito a relatório/auditoria.
- Conhecimento relacionado: confirmação antes de ações com impacto e segredos fora do Brain/Git.
