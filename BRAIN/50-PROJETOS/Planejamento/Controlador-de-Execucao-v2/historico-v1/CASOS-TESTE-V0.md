# Casos de Teste v0

Casos derivados da baseline de 40 tarefas. Cada caso define entrada, perfil esperado e gates obrigatorios.

| ID | Entrada | Perfil esperado | Gates obrigatorios |
|---|---|---|---|
| 01 | Desenhar arquitetura e plano cadenciado do roteador | GPT-5.6-Sol high | read-only, separar proposta de implementação, preservar gates |
| 02 | Iniciar acompanhamento Sentinel v2 24h com comunicacao de fechamento | GPT-5.6-Sol max | aprovacao explicita, sem fallback silencioso, sem alterar contrato |
| 03 | Gerar resumo diario Bitdefender para grupo operacional | GPT-5.5 high | sem segredo, validar contagens, fonte local |
| 04 | Transcrever audio operacional | Deterministico, sem LLM | faster-whisper local small pt, sem fallback externo, escalar apenas interpretacao |
| 05 | Auditar estrutura OpenClaw em modo leitura | GPT-5.6-Sol high | leitura, fonte local, sem alteracao |
| 06 | Planejar implantacao PostgreSQL | GPT-5.6-Sol max | backup, rollback, aprovacao, validacao |
| 07 | Padronizar comunicacao entre agentes | GPT-5.6-Sol high | aprovacao, escopo exato, sem ampliar autoridade |
| 08 | Consolidar documentos GWS em relatorio | GPT-5.5 high | fonte local, validar PDF, sem envio externo |
| 09 | Executar coleta diaria Bitdefender Ninja | Deterministico, sem LLM | segredo fora, read-only, validar saida |
| 10 | Executar rotina Bitdefender com mesmo contrato | Deterministico, sem LLM | validar incidentes/quarentena, sem ticket real |
| 11 | Executar rotina Bitdefender recorrente | Deterministico, sem LLM | validar formato, nao alterar Ninja/GravityZone, escalar excecao |
| 12 | Revisar modelo EOL Bikon | GPT-5.5 high | marca Bikon, leitura mobile/PDF, fonte |
| 13 | Corrigir lote EOL com divergencia de layout | GPT-5.5 high | comparar modelo aprovado, revisar PDF, registrar retrabalho |
| 14 | Montar pacote de evidencias Provimento 213 | GPT-5.6-Sol high | fonte, escopo tecnico, sem parecer juridico |
| 15 | Fechar dossie tecnico Provimento 213 | GPT-5.6-Sol high | identidade Bikon, evidencia, revisao final |
| 16 | Buscar evidencias originais multi-produto | GPT-5.5 high | fonte local, declarar lacuna, nao inventar |
| 17 | Consolidar PDFs NFS-e de julho | GPT-5.5 high | read-only, sem emitir/cancelar/enviar |
| 18 | Gerar relacao fiscal CSV | GPT-5.5 high | conciliar numero, status, arquivo |
| 19 | Consultar status Notaas das notas | GPT-5.6-Sol high | nao emitir/cancelar, registrar ausencia |
| 20 | Validar manifesto fiscal | GPT-5.5 high | divergencia bloqueia entrega |
| 21 | Validar existencia e paginas dos PDFs | Deterministico, sem LLM | contagem, pagina, arquivo abrivel, bloquear divergencia |
| 22 | Gerar hashes SHA-256 do pacote | Deterministico, sem LLM | hash para todos os arquivos |
| 23 | Criar pacote zip financeiro | Deterministico, sem LLM | comparar zip com manifesto, bloquear divergencia |
| 24 | Fechar resumo executivo de pendencias fiscais | GPT-5.5 high | listar ausencias e escopo excluido |
| 25 | Validar skills sem alterar arquivos | Deterministico, sem LLM | nao alterar skill, registrar resultado, escalar falha para Spark |
| 26 | Gerar carrossel com texto, imagem e layout | GPT-5.6-Sol high | QA visual, sem publicar, preservar escopo |
| 27 | Gerar post estatico Bikon | GPT-5.5 high | brand QA, sem publicar, sem promessa absoluta |
| 28 | Renderizar carrossel multi-asset | GPT-5.6-Sol high | 1080x1350, leitura, manifesto |
| 29 | Criar calendario editorial semanal | GPT-5.5 high | tom Bikon, sem promessa absoluta |
| 30 | Preparar prompt/QA Kling | GPT-5.5 high | aprovacao de gasto, sem publicacao |
| 31 | Corrigir artes com colisao e preservar aprovadas | GPT-5.6-Sol high | QA Kowalski, preservar hashes aprovados |
| 32 | Cancelar operacao com crons pendentes | GPT-5.6-Sol max | alvo exato, confirmar estado, sem publicar |
| 33 | Preparar leitura NinjaOne | GPT-5.6-Sol high | read-only, sem ticket/producao |
| 34 | Preparar leitura ARX/Cove | GPT-5.6-Sol high | sem alterar jobs, evidenciar lacunas |
| 35 | Preparar leitura Bitdefender | GPT-5.6-Sol high | segredo fora, read-only |
| 36 | Diagnosticar logs de gateway | GPT-5.6-Sol max | backup, rollback, validacao, aprovacao |
| 37 | Ajustar governanca de auditoria de acesso | GPT-5.6-Sol max | trilha, sem segredo, aprovacao |
| 38 | Rodar canario Sentinel read-only | GPT-5.6-Sol high | PASS por ciclo, parar em P1/P2 |
| 39 | Tratar canario com ARX P2 | GPT-5.6-Sol max | parar, evidenciar P2, pedir aprovacao |
| 40 | Explicar lacunas e criterios v2 | GPT-5.6-Sol high | separar fato/hipotese, sem alterar canario |
