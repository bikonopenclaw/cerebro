# Arquitetura 2.1

A v2.1 organiza a produção em seis camadas:

1. Orquestração: Puppet Master mantém objetivo, ordem, gates e decisão humana.
2. Trabalho editorial: Robotnik produz; Kowalski governa marca; agentes opcionais assistem.
3. Governance Engine: decide \`allow|deny\` sem efeito externo.
4. Event Store: registra comando, decisão, transição e resultado em stream append-only com hash chain.
5. Asset Pipeline: preserva bruto, lineage, checksum, versões e promoção entre estágios.
6. Provider Layer: descreve Image, Video, TTS, Storage, Publication e Search sem acoplar a um fornecedor.

Princípios:

- local-first;
- deny by default;
- nenhuma credencial na skill;
- provider externo desabilitado até janela aprovada;
- evento é fonte da verdade; manifestos são projeções portáteis;
- payload, approval, provider e resultado compartilham correlation ID;
- resultado incerto nunca autoriza repetição;
- Puppet Master, Robotnik e Kowalski permanecem canônicos.

## Diretório operacional

\`\`\`text
content-production/
  campaigns/<campaign-id>/
    campaign.json
    events.jsonl
    assets/
    approvals/
    requests/
    governance-decisions/
    external-actions/
    playbooks/
\`\`\`

Estado operacional fica fora da skill. A skill contém contratos, políticas, schemas, scripts determinísticos e playbooks.
