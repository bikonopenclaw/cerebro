---
name: "instagram-brand-director"
description: "Produção governada de conteúdo Instagram com provedores, eventos, assets, QA e aprovação humana."
---

# Instagram Brand Director 2.1.0

Plataforma local-first para conduzir conteúdo do briefing ao aprendizado, com IA assistiva, trilha auditável e ação externa bloqueada por padrão.

## Autoridade

- Puppet Master coordena estado, gates, decisões e handoffs.
- Robotnik conduz estratégia, copy, criação, produção e métricas.
- Kowalski fornece brandpack, brand lock e brand QA.
- Proprietário é a única autoridade para qualquer mutação ou transmissão externa.
- Skipper auxilia pesquisa, Rico auxilia QA e Private auxilia compliance. Os três iniciam desabilitados e não substituem os responsáveis canônicos.
- Nenhum agente aprova a própria ação externa.

Ler `{baseDir}/references/agent-governance.md` e `{baseDir}/references/governance-engine.md` antes de delegar ou preparar ação externa.

## Regra inviolável

Não gerar externamente, enviar, fazer upload, arquivar URL remota, criar rascunho remoto, publicar, agendar, editar, excluir, disparar webhook ou transmitir conteúdo não público sem OK explícito do proprietário para:

- campanha, ativo e versão;
- ação e destino;
- provedor;
- payload e hash;
- mídia, copy e parâmetros;
- horário, custo e dados enviados, quando aplicável.

Silêncio, OK anterior, aprovação de agente, prazo ou intenção presumida não autorizam. Mudança de payload invalida o OK. Não existe retry automático de mutação externa.

## Arquitetura

Carregar apenas o necessário:

- visão geral: `{baseDir}/references/architecture-v2.1.md`;
- provedores: `{baseDir}/references/provider-system.md`;
- Event Sourcing: `{baseDir}/references/event-sourcing.md`;
- Asset Pipeline: `{baseDir}/references/asset-pipeline.md`;
- Governance Engine: `{baseDir}/references/governance-engine.md`;
- papéis e playbooks: `{baseDir}/references/playbooks-and-roles.md`;
- runtime e approvals: `{baseDir}/references/runtime-control.md`;
- aceite: `{baseDir}/references/acceptance-matrix.md`;
- compatibilidade: `{baseDir}/references/compatibility-report.md`;
- migração: `{baseDir}/references/migration-v2.0.1-to-v2.1.0.md`.

A arquitetura expõe seis tipos de provedor: Image, Video, TTS, Storage, Publication e Search. Todos os provedores externos iniciam `enabled: false`. Não configurar credencial, endpoint ou adapter dentro da skill.

## Enforcement técnico

Usar somente os controles versionados:

- `scripts/event_store.py`: eventos append-only, hash chain, verificação e replay;
- `scripts/campaignctl.py`: comandos compatíveis de campanha e projeção;
- `scripts/approvalctl.py`: registro, verificação, reserva, execução e conclusão do OK;
- `scripts/governance_engine.py`: decisão fail-closed de ator, provedor, política e aprovação;
- `scripts/providerctl.py`: inventário e preflight de provedores, sem implementação externa ativa;
- `scripts/asset_pipeline.py`: registro, checksum, lineage e promoção de assets;
- `scripts/kling_exec.py`: argv tipado, `shell=False`, lifecycle de approval e resultado persistido;
- `scripts/assetctl.py`: HTTPS, allowlist, limite, hash, lifecycle e resultado persistido;
- `scripts/preflight.py`: estrutura, runtime, composição e produção;
- `scripts/qa_media.py`: hash e QA técnico local.

Toda mutação externa exige `operation-request.json` canônico, Governance Engine em `allow`, provider habilitado, approval válido e event store íntegro.

## Lifecycle de ação externa

Usar estados explícitos:

`approved -> reserved -> executing -> succeeded|failed|indeterminate`

- `reserved` vincula approval e execution ID antes da chamada.
- `executing` registra que a tentativa começou.
- `succeeded`, `failed` e `indeterminate` encerram o approval para nova mutação.
- Cada mudança gera evento append-only.
- Resultado externo é persistido antes de ser apresentado.
- `indeterminate` exige consulta do mesmo remote ID. Nunca repetir a mutação.

O comando legado `consume` permanece por compatibilidade, mas adapters v2.1 devem usar o lifecycle acima.

## Fluxo

1. Puppet Master cria a campanha e o correlation ID.
2. Robotnik prepara briefing. Proprietário aprova o Portão A.
3. Kowalski entrega brandpack e brand lock. Portão K.
4. Pesquisa e estratégia. Skipper só participa se habilitado. Proprietário aprova Portão B.
5. Robotnik prepara roteiro, copy, prompts e plano de produção.
6. Cada asset entra no pipeline em `source` e avança sem sobrescrever o bruto.
7. Geração externa exige Portão C, provider habilitado e OK específico.
8. Composição local exige preflight de produção.
9. Rico e Private podem auxiliar se habilitados. Kowalski continua responsável por brand QA.
10. Release candidate exige QA técnico, visual, textual, marca, acessibilidade e compliance.
11. Portão X apresenta payload final ao proprietário.
12. Adapter aprovado executa uma vez e persiste o resultado.
13. Robotnik mede; Puppet Master prioriza o próximo experimento.

Playbooks:

- `{baseDir}/references/playbooks/intake-to-release.md`;
- `{baseDir}/references/research-system.md`;
- `{baseDir}/references/playbooks/qa.md`;
- `{baseDir}/references/qa-compliance.md`;
- `{baseDir}/references/playbooks/external-action.md`.

## Compatibilidade

Preservar:

- comandos `campaignctl init|transition|status`;
- comandos `approvalctl record|verify|consume|revoke`;
- request canônico, hashes e owner binding;
- `kling_exec.py`, `assetctl.py`, `qa_media.py` e `preflight.py`;
- Puppet Master, Robotnik e Kowalski como papéis canônicos;
- publicação bloqueada sem adapter aprovado;
- gates de composição e ferramentas locais.

Campos e comandos novos são aditivos. Migração de estado só ocorre em janela aprovada.

## Fail-closed

- Provider ausente, desconhecido, desabilitado ou sem contrato: bloquear.
- Agente opcional desabilitado: não delegar e manter o responsável canônico.
- Event stream inválido: bloquear projeção e ação.
- Approval ausente, divergente, expirado, revogado ou já reservado: bloquear.
- Resultado incerto: registrar `indeterminate` e consultar. Não repetir.
- Pesquisa indisponível: usar somente fontes fornecidas e registrar lacuna.
- Kowalski indisponível: bloquear produção visual final.
- QA ou compliance falha: não criar release candidate.
- Publicação sem adapter: manter pacote local.
- Rota falhou: parar no último estado seguro. Não trocar fonte, ferramenta, provedor ou sequência.

## Entrega por marco

Informar campanha, ativo, versão, estado, responsável, providers usados, eventos, hashes, QA, approvals, custos, caminhos e próxima decisão do proprietário. Nunca registrar segredo.
