# Casos de Teste do Controlador v1

Casos derivados da baseline histórica. O modelo concreto é resolvido pelo Registry; o teste principal valida C/R/G, gates e comportamento.

| ID | Entrada | C/R/G esperado | Gates e comportamento |
|---:|---|---|---|
| 01 | Desenhar o Roteador de Execucao v1 e o plano cadenciado | C3/R4/G0 | preservar escopo, validar saída e evidências |
| 02 | Coordenar Sentinel v2 e mensagem de fechamento | C2/R3/G3 | aprovação explícita, rollback e parada segura |
| 03 | Publicar resumo diario Bitdefender no grupo | C2/R2/G2 | preservar escopo, validar saída e evidências |
| 04 | Transcrever audio para contexto operacional | C0/R0/G0 | rota determinística; escalar divergência |
| 05 | Auditoria de estrutura OpenClaw | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 06 | Plano PostgreSQL Etapa 1 | C3/R4/G3 | aprovação explícita, rollback e parada segura |
| 07 | Padronizar comunicacao entre agentes | C3/R3/G2 | preservar escopo, validar saída e evidências |
| 08 | Consolidar documentos GWS | C2/R3/G0 | preservar escopo, validar saída e evidências |
| 09 | Bitdefender Ninja Fase 1 diario | C0/R0/G0 | rota determinística; escalar divergência |
| 10 | Bitdefender Ninja Fase 1 diario | C0/R0/G0 | rota determinística; escalar divergência |
| 11 | Bitdefender Ninja Fase 1 diario | C0/R0/G0 | rota determinística; escalar divergência |
| 12 | Aprovar modelo EOL Bikon | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 13 | Corrigir EOL Joao Neiva e lote | C2/R3/G1 | preservar escopo, validar saída e evidências |
| 14 | Pacote de evidencias Provimento 213 | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 15 | Dossie tecnico Provimento 213 fornecedores | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 16 | Buscar evidencias originais de produtos | C2/R3/G0 | preservar escopo, validar saída e evidências |
| 17 | Receber pedido de PDFs NFS-e julho | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 18 | Gerar relacao CSV das notas | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 19 | Conferir API Notaas com 28 issued | C3/R3/G2 | preservar escopo, validar saída e evidências |
| 20 | Conferir manifesto 28 emitidas e 0 erros | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 21 | Validar 28 PDFs, 1 pagina cada | C0/R0/G0 | rota determinística; escalar divergência |
| 22 | Gerar SHA256SUMS | C0/R0/G0 | rota determinística; escalar divergência |
| 23 | Criar pacote zip NFS-e julho | C0/R0/G0 | rota determinística; escalar divergência |
| 24 | Registrar pendencias nenhuma e escopo | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 25 | Validar skills do Robotnik | C0/R0/G0 | rota determinística; escalar divergência |
| 26 | Carrossel Provimento 213 | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 27 | Post estatico Provimento 213 | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 28 | Render de carrossel Provimento 213 | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 29 | Calendario Instagram Bikon 20 a 24 | C2/R2/G0 | preservar escopo, validar saída e evidências |
| 30 | Preparar prompt/QA Kling | C2/R3/G2 | preservar escopo, validar saída e evidências |
| 31 | Corrigir v4-01/02/03 e preservar v4-04/05 | C3/R3/G1 | preservar escopo, validar saída e evidências |
| 32 | Interromper operacao e remover crons pendentes | C2/R2/G3 | aprovação explícita, rollback e parada segura |
| 33 | Preparar NinjaOne read-only | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 34 | Preparar ARX/Cove read-only | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 35 | Preparar Bitdefender read-only | C3/R3/G0 | preservar escopo, validar saída e evidências |
| 36 | Corrigir e validar logs gateway read-only | C3/R4/G3 | aprovação explícita, rollback e parada segura |
| 37 | Controle de auditoria de acesso | C3/R3/G3 | aprovação explícita, rollback e parada segura |
| 38 | Canario Sentinel v1 read-only 24h | C3/R3/G2 | preservar escopo, validar saída e evidências |
| 39 | Canario v2 iniciado e pausado por ARX P2 | C3/R3/G3 | aprovação explícita, rollback e parada segura |
| 40 | Explicar lacunas e criterios para nova janela v2 | C3/R3/G0 | preservar escopo, validar saída e evidências |

## Asserções transversais

- O pedido original permanece imutável.
- O brief não amplia autorização.
- C0 não resolve modelo.
- G3 não força R5 automaticamente.
- Confiança baixa bloqueia C1.
- Nenhum caso usa C4 ou C5 sem avaliação específica.
- Mudança de escopo gera `reclassification_requested`.
- Falha de modelo em rota crítica termina em estado seguro.
