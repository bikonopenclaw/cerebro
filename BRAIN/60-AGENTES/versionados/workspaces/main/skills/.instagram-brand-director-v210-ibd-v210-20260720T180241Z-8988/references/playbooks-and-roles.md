# Papéis e playbooks

## Canônicos

- Puppet Master: dono do fluxo, priorização, gates, aprovação registrada e consolidação.
- Robotnik: dono editorial e de produção.
- Kowalski: dono do brandpack, brand lock e brand QA.
- Proprietário: dono exclusivo de autorização externa e risco residual.

## Opcionais, desabilitados

- Skipper: coleta e organiza pesquisa pública sanitizada. Robotnik continua responsável pela conclusão editorial.
- Rico: executa checklist auxiliar e aponta falhas. Kowalski continua responsável por marca.
- Private: verifica privacidade, claims, direitos e políticas. Não presta parecer jurídico nem aceita risco.

Ativar agente opcional exige mudança separada em \`assets/agent-registry.yaml\` e \`templates/governance.yaml\`, testes e OK do proprietário.

## Playbooks

- intake-to-release: fluxo completo sem publicação;
- research: pesquisa com fontes e sensibilidade;
- qa: QA técnico, visual, texto, marca e acessibilidade;
- compliance: claims, direitos, privacidade e risco;
- external-action: Portão X, lifecycle e resultado.
