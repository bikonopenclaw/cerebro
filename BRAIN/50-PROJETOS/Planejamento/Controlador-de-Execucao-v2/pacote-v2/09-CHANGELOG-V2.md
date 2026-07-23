# Changelog da Arquitetura do Controlador

## v2.0 — 2026-07-23

### Breaking changes

- O sistema deixa de rotear diretamente por nome de modelo.
- O Controlador de Execução substitui o conceito limitado de Roteador de Modelos.
- Capacidade, esforço de raciocínio, risco, custo/latência e modo de execução tornam-se dimensões independentes.
- O executor não pode trocar o próprio modelo.
- O pedido original passa a ser preservado junto ao Contrato de Execução.

### Adicionado

- Gate D0 formal para execução sem LLM.
- Perfis C0–C5.
- Níveis lógicos R0–R5.
- Classes de risco G0–G3.
- Registro de Modelos versionado.
- Contrato de Execução estruturado.
- Política de reclassificação e parada segura.
- Etapa 0.5 para migrar a baseline.
- Métricas de subdimensionamento, superdimensionamento, custo, latência e retrabalho.

### Alterado

- “Spark”, “GPT-5.5” e “GPT-5.6-Sol” deixam de ser perfis permanentes e passam a ser candidatos resolvidos pelo Registry.
- Casos críticos passam a exigir gates por risco, sem assumir raciocínio máximo.
- Paralelismo passa a ser modo C5, não sinônimo de maior inteligência.

### Preservado

- Etapa 0 histórica e suas evidências.
- Gates de produção, root, gasto, envio externo, publicação e alteração real.
- Regra de não fazer fallback silencioso em tarefa crítica.
- Parada no último estado seguro.

### Não autorizado

- Troca automática de modelo.
- Alteração de agentes, cron, skill, gateway ou produção.
- Promoção de modelos sem avaliações.
