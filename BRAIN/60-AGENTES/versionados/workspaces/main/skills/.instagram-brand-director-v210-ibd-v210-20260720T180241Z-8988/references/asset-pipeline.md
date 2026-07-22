# Asset Pipeline

Estágios:

\`source -> generated -> selected -> composed -> qa -> release-candidate -> archived\`

\`blocked\` pode ser alcançado de qualquer estágio por evento separado.

## Regras

- bruto é imutável;
- registrar caminho absoluto resolvido, tamanho, MIME e SHA-256;
- cada promoção exige checksum atual igual ao registrado;
- mudança de arquivo cria nova versão ou novo asset;
- lineage aponta para asset/version de origem e operação;
- não promover para release-candidate sem QA aplicável;
- não arquivar URL remota como fonte canônica;
- saída de provider entra em \`generated\` somente após resultado persistido;
- publicação não altera o asset local.

\`scripts/asset_pipeline.py\` oferece \`register\`, \`promote\`, \`status\` e \`verify\`.
