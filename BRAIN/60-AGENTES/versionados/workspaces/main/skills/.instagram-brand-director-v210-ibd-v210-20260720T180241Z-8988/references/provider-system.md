# Provider System

## Contrato

Cada provider declara:

- \`kind\`: image, video, tts, storage, publication ou search;
- \`provider_id\`;
- \`enabled\`;
- \`external\`;
- \`adapter_path\`;
- capacidades allowlist.

\`assets/provider-registry.yaml\` é declarativo. Não contém endpoint, token ou segredo.

## Regras

- Provider desconhecido ou desabilitado gera \`deny\`.
- Provider externo exige approval do proprietário e lifecycle de execução.
- Provider local não recebe dispensa automática: a operação ainda deve estar permitida ao ator.
- Não usar fallback entre providers.
- Não selecionar provider por disponibilidade sem nova decisão.
- Adapter não pode inventar flags ou aceitar shell livre.
- Publication inicia sem adapter.
- Search externo inicia desabilitado.
- Kling existe apenas como adapter legado controlado e nasce desabilitado no registro v2.1.
- Filesystem local é o único provider habilitado por padrão.

## Habilitação futura

Exige revisão separada de contrato, dados enviados, custo, credenciais, least privilege, idempotência, resultado persistido, testes e rollback. Habilitar um provider não habilita outro.
