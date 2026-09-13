---
name: "content-production-contract"
description: "Autoridade criativa Bikon. Use automaticamente para estratégia, copy, legenda, post, anúncio, carrossel, campanha, piloto e planejamento 1.1-S1."
---

# Produção criativa Bikon

Antes de cada trabalho Bikon, inclusive em sessão nova, /new ou troca de executor, leia INTEGRALMENTE [o contrato aprovado 1.1-S1](references/creative-contract-v1.md). Ele é a única autoridade criativa; não use memória, carrossel antigo ou templates técnicos como direção alternativa.

Para planejamento editorial Bikon no Instagram, consumir também a seção 4 do contrato antes de fechar o briefing: a cadência é compartilhada pela conta, os alvos são ajustáveis e os aceites de direção, produção, conteúdo final e publicação têm escopos distintos.

Para peça visual, abra e inspecione a referência canônica em `assets/referencia-canonica.jpeg`; leia [identidade e hashes oficiais](references/brand-assets.json) e [a rota produtiva e seu estado real](references/production-route.md). Confirme acesso ao logo oficial e à ferramenta registrada antes de produzir. Pedido apenas textual não exige gerar imagem. Preserve o brief e a quantidade solicitada: uma peça piloto e uma legenda quando esse for o pedido.

Siga o fluxo integral do contrato: brief, direção, fotografia pela rota autorizada, finalização, inspeção do exportado e prévia reduzida, revisão real do Kowalski com referência, entrega privada e aceite humano. Registre versão/hash do contrato, referência de entrada, logo, prompt, chamada nativa e hashes da saída bruta e final. Falta de insumo, ferramenta ou revisor bloqueia a etapa; não habilita substituição estética nem rota paga.

As cinco peças de `esteira-instagram-ia-governada-20260907` foram reprovadas. São apenas histórico de rejeição, nunca referência positiva ou final reutilizável. Não inferir aceite do novo piloto a partir do post antigo.

## Ferramentas e exportação

[Stack técnico](references/stack.md) contém somente etapas subordinadas ao contrato. Use 1080 × 1350, 4:5, sRGB para o piloto. Mantenha bruto, editável, exportação e prévia reduzida; reabra a exportação. Não registre inspeção em celular físico sem realizá-la.

## Publicação protegida, consumidor técnico existente

Após aprovação explícita correspondente, executar o publicador canônico do Robotnik:
`python3 instagram-bikon/scripts/instagram_graph.py run-job JOB`.
O runbook `instagram-bikon/docs/README.md` define registro de aprovação, staging,
lock exclusivo, retomada, reconciliação de resultado desconhecido e recibo.
Para o Goal `ROBOTNIK_INSTAGRAM_OPERATIONAL_RECOVERY_V1`, o único JOB autorizado
é `bikon-ia-20260907`. Conservar o JPEG e a legenda Variante A recuperados dos
registros; não gerar nova peça nem reescrever legenda. Um erro de autenticação
não revoga a aprovação existente, mas bloqueia chamadas Meta até renovação.
O registro antigo de provider desabilitado na skill compartilhada e notas
históricas Buffer/Cloudflare não são consumidores do CLI instalado. Não ativar
outro publicador nem contornar decisões de aprovação de conectores.

O job acima já está COMPLETE / VERIFIED_PUBLISHED, publication_attempts=1. Não executar run-job para teste, geração, revisão ou entrega de piloto. Aprovação de direção/arte não autoriza publicação. Nesta implantação não há autorização para Meta, staging, container, publicação ou agendamento.
