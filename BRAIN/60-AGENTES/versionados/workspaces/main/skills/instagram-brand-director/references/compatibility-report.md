# Compatibilidade 2.0.1 para 2.1.0

## Mantido

- frontmatter \`name\` e \`description\`;
- Puppet Master, Robotnik e Kowalski;
- owner binding;
- request hash canônico;
- approvals revogáveis, expirantes e single-use;
- campaignctl init, transition e status;
- approvalctl record, verify, consume e revoke;
- Kling com argv tipado e shell desativado;
- assetctl com HTTPS, allowlist, limite e hash;
- qa_media;
- preflight build e production;
- publicação bloqueada;
- composição local e seus gates;
- estrutura de campanha fora da skill.

## Aditivo

- provider registry;
- agent registry;
- event hash chain e replay;
- asset pipeline;
- Governance Engine;
- lifecycle reserved/executing/outcome;
- resultado de adapter persistido;
- novos schemas, testes e playbooks.

## Mudança comportamental

Adapters v2.1 devem usar reserve/start/finish. \`consume\` continua disponível para compatibilidade, mas não é o caminho recomendado. Providers externos ficam desabilitados, inclusive Kling, até configuração separada.

## Sem compatibilidade prometida

- approvals em estado intermediário criados por protótipos;
- streams editados manualmente;
- scripts que dependam de stdout como único registro de resultado;
- automação que bypassa os wrappers.
