# LinkedIn Robotnik Publisher

```yaml
nome: LinkedIn Robotnik Publisher
status: gate_a_bloqueado_por_sessao_humana
responsavel: Puppet Master
inicio: 2026-09-17
fim:
prioridade: alta
ultima_revisao: 2026-09-18
tags: [linkedin, robotnik, bikon, api-oficial, publicacao, oauth, approval, pgl]
```

## Objetivo

Dar ao Robotnik uma capacidade governada de preparar publicações para a Página da Bikon no LinkedIn, mantendo Puppet Master como orquestrador e Hebert como gate humano de efeitos externos.

O Brain registra estado consolidado e guardrails. Código, testes, evidências e manifests autoritativos permanecem em `projects/linkedin-robotnik-publisher/`, fora do Brain/Git.

## Escopo do MVP

- API oficial REST versionada do LinkedIn, com versão configurável e default preparado `202609`.
- Publicação somente em `urn:li:organization:<id>` da Bikon e somente com `w_organization_social`.
- Texto e imagem única; modo mock obrigatório por padrão.
- Preview e SHA-256 determinísticos; aprovação one-shot vinculada ao conteúdo, alvo, versão e modo.
- Aprovação live assinada com Ed25519, alvo injetado pelo gateway e redaction de tokens.
- Sem endpoint público, callback OAuth implantado, perfil pessoal, comments, reactions, analytics, agendamento, edição ou exclusão no MVP.

## Estado validado

- Scaffold Node.js 22 ESM sem dependências de terceiros.
- Testes locais `12/12 PASS`, demo `mock_confirmed` sem rede, sintaxe/JSON/scan de segredo `PASS` e live fail-closed sem enable/credencial.
- O PGL canônico aceitou `PROJECT_GENESIS` na sequência `1`, hash `dfcbf3b02e55b97622104ac15c6d503052eea751150bd1df28c0edbbb2b68bc5`, sem retry de append nem ledger paralelo.
- O projeto está em `LINKEDIN_CREDENTIALING_GATE`. Hebert autorizou exclusivamente o Gate A: criar um app, associar/verificar a Página Bikon e solicitar Community Management API Development com apenas `w_organization_social`.
- A tentativa parou no último estado seguro, antes do LinkedIn Developer Portal, porque o Chrome autenticado do perfil `user` não estava aberto nem anexável. App criado, OAuth iniciado, segredo lido e post publicado: todos `false`.

## Gates seguintes

1. Abrir o Chrome autenticado no host, habilitar depuração remota e aprovar o attach; retomar o mesmo Goal e somente o Gate A.
2. Tratar em autorização separada o callback HTTPS `/oauth/linkedin/callback`, origem Bikon e binding do secret store.
3. Executar OAuth 3-legged somente depois do app/Page/produto e infraestrutura estarem comprovados.
4. Exigir aprovação específica por conteúdo antes de qualquer publicação live.
5. Em resposta externa ambígua, reconciliar antes de retry; não há idempotency key de criação de post comprovada no provedor.

## Guardrails

- Browser automation, ClawLink, plugin terceiro e API não oficial não são fallback.
- Robotnik não escolhe o target e não recebe autoridade de publicação por preparar a peça.
- Credenciamento não autoriza OAuth; OAuth não autoriza post; aceite artístico não autoriza publicação.
- Segredos, tokens e valores reais ficam fora do Brain, Git, logs e documentação.
- Store JSON é somente desenvolvimento; produção exige reserva compartilhada durável.

## Relações

- [[60-AGENTES/ROBOTNIK|Robotnik]]
- [[20-EMPRESAS/BIKON/README|Bikon]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK|Instagram Bikon Robotnik]]
