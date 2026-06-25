# Provimento CNJ 213/2026, Kowalski

```yaml
nome: Provimento CNJ 213/2026 Kowalski
status: ativo
responsavel: Kowalski sob coordenação do Puppet Master
ultima_revisao: 2026-06-25
fonte: skill Kowalski e diagnóstico piloto Cartório Alzira
tags: [kowalski, provimento-213-2026, cartorios, diagnostico, evidencia]
```

## Objetivo

Registrar a skill e o fluxo operacional do Kowalski para diagnósticos técnicos de cartórios no contexto do Provimento CNJ 213/2026.

## Skill

- Caminho ativo: `/data/.openclaw/agents/kowalski/agent/skills/provimento-213-2026/SKILL.md`
- Snapshot Brain: `BRAIN/60-AGENTES/versionados/agents/kowalski/agent/skills/provimento-213-2026/`
- Workspace operacional: `/data/.openclaw/workspace-kowalski/provimento-213-2026/`
- Snapshot workspace: `BRAIN/60-AGENTES/versionados/workspaces/kowalski/provimento-213-2026/`

## Escopo

A skill cobre:

- diagnóstico técnico
- checklist por classe da serventia
- dossiê técnico
- relatório simplificado
- PCN/PRD
- política de segurança
- inventário
- backup
- logs
- MFA
- LGPD
- interoperabilidade
- parecer técnico no padrão Bikon/Kowalski

## Guardrails

- Apoio técnico, não parecer jurídico.
- Não declarar conformidade jurídica plena.
- Não enviar relatório para cliente externo sem aprovação explícita do Hebert/Puppet Master.
- Não expor senhas, tokens, chaves, credenciais ou dados pessoais desnecessários.

## Caso piloto

Em 2026-06-25, foi gerado diagnóstico piloto para Cartório Alzira usando ARX Backup, NinjaOne/Bikon RMM e Bitdefender GravityZone.

Resultado operacional: status Atenção, com controles técnicos existentes e lacunas documentais relevantes.

Lacunas principais observadas no piloto:

- classe da serventia não informada
- PCN/PRD
- teste de restauração
- MFA
- LGPD/PSI
- logs imutáveis
- portabilidade/reversibilidade
- endpoints não gerenciados no Bitdefender

## Versionamento

A skill está incluída na rotina `sync-agentes-versionados.py`, executada pela consolidação diária silenciosa do Brain.
