# Provimento CNJ 213/2026, Kowalski

```yaml
nome: Provimento CNJ 213/2026 Kowalski
status: ativo
responsavel: Kowalski sob coordenação do Puppet Master
ultima_revisao: 2026-07-15
fonte: skills Provimento 213/2026 e consulta CNS, carteira oficial e diagnóstico piloto Cartório Alzira
tags: [kowalski, provimento-213-2026, cartorios, cns, cnj, diagnostico, evidencia]
```

## Objetivo

Registrar a skill e o fluxo operacional do Kowalski para diagnósticos técnicos de cartórios no contexto do Provimento CNJ 213/2026.

## Skill

- Caminho ativo: `/data/.openclaw/workspace-kowalski/skills/provimento-213-2026/SKILL.md`
- Snapshot Brain: `BRAIN/60-AGENTES/versionados/workspaces/kowalski/skills/provimento-213-2026/`
- Workspace operacional: `/data/.openclaw/workspace-kowalski/provimento-213-2026/`
- Snapshot workspace: `BRAIN/60-AGENTES/versionados/workspaces/kowalski/provimento-213-2026/`
- Skill complementar de onboarding por CNS: `/data/.openclaw/workspace/skills/consulta-cns-cartorio/SKILL.md`.

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

## Consulta oficial por CNS

Em 2026-07-14/15, o fluxo passou a exigir consulta oficial por CNS no onboarding e na preparação de evidências de cartórios:

- o CNS deve vir do humano responsável ou de fonte oficial confirmada; nunca inferir por nome, município, titular, CNPJ ou semelhança;
- com CNS confirmado, a referência principal é a API pública CNJ Justiça Aberta em `/v1/api/serventias/{cns}`, preservando zeros à esquerda e removendo pontuação;
- CNS localizado apenas por Corregedoria/TJ sem confirmação humana permanece como candidato, não como fato fechado;
- serventia com situação jurídica `VAGO` exige consulta dos responsáveis ativos e distinção explícita de interino;
- classificação regulatória pelo Provimento 213/2026 exige norma/tabela oficial vigente, período de arrecadação e critério de semestre documentados;
- resposta bruta e fonte devem compor evidência preparada, sem gravação automática em CRM, banco, planilha ou relatório final.

A carteira oficial de cartórios/CNS foi atualizada em 2026-07-14 como referência operacional versionada no snapshot do Kowalski, sem substituir a confirmação do CNS de cada caso.

## Guardrails

- Apoio técnico, não parecer jurídico.
- Não declarar conformidade jurídica plena.
- Não enviar relatório para cliente externo sem aprovação explícita do Hebert/Puppet Master.
- Não expor senhas, tokens, chaves, credenciais ou dados pessoais desnecessários.
- Não inferir CNS nem transformar CNS candidato em confirmado.
- Não classificar serventia sem fonte normativa vigente e evidência do período usado.

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
