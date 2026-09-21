---
id: brain-2acb877be050e1fb027d
type: knowledge
title: Validação do runtime pós-migração
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:50:50.519705Z'
relationships:
- type: references
  target: BRAIN/50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/openclaw-crons/README-verificacao-crons.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W29.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md#relações
---

# Validação do runtime pós-migração

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W29
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [openclaw, migracao, runtime, scheduler, skills, readiness, rollback]
```

## Princípio

Arquivo restaurado não comprova carregamento, configuração válida nem execução. Uma migração só termina quando o runtime ativo descobre, executa e preserva os componentes esperados depois de restart controlado.

## Gate mínimo

1. Confirmar versão alinhada entre CLI e serviços.
2. Confirmar supervisor, unit e state dir realmente usados.
3. Validar rotas ativas de workspaces, skills e configurações.
4. Confirmar skills indexadas, não apenas presentes em disco.
5. Validar armazenamento do scheduler, jobs habilitados, `nextWake`, vencidos/em execução e erros consecutivos.
6. Executar provas read-only ou canários permitidos para confirmar funcionamento real.
7. Verificar canal, RPC, portas e exposição esperada.
8. Fazer restart controlado e repetir o readiness para provar persistência.

## Separação de mudanças

Upgrade, plugin, modelo/configuração, porta, restart e recuperação de backlog são categorias distintas. Não misturar para ganhar tempo. No primeiro erro de versão, migração, plugin ou supervisor, parar e restaurar o último estado conhecido antes de escolher outra rota.

## Backlog

Antes de reiniciar ou reabrir canais, inspecionar jobs vencidos, em execução e filas pendentes. Depois da recuperação, deduplicar por identificador e responder apenas ao pedido mais recente quando mensagens antigas já foram superadas.

## Relações

- [[50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw|Migração Hostinger VPS / OpenClaw]]
- [[70-AUTOMACOES/openclaw-crons/README-verificacao-crons|Verificação de segurança de crons]]
- [[01-DIARIO/Semanal/2026-W29|Semana 2026-W29, cobertura parcial até 2026-07-17]]

## Configuração, sessão e comunicação cruzada

Na recuperação histórica de 2026-06-13, os relatos distinguiram agentes cadastrados, visibilidade do histórico, permissão de comunicação e ferramentas já carregadas pela sessão. O teste individual de um agente também foi separado do teste em que um agente chama o outro.

Como critério de validação, conferir separadamente essas superfícies no runtime efetivo. Uma sessão com permissões carregadas antes da mudança pode exigir uma prova nova pelo caminho aprovado. Não concluir falha do gateway só por uma visão antiga da ferramenta, nem sucesso da comunicação cruzada só por um ping individual. Isso não recomenda abrir visibilidade ou permissões amplas; cada rota deve continuar limitada ao escopo necessário.

Fontes: trechos 28921, 28925, 28926, 28932, 28933, 28937 e 28938, identificados por hash e posição no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-round2-20260921.json`. São relatos históricos, não uma verificação da configuração atual.

## Complementos reconciliados — lote 5 de 2026-09-21

No ensaio de migração de 07/07/2026, foram conferidos versões, ownership e conteúdo restaurado, mas o gateway de destino foi mantido inativo/desabilitado até o corte para não disputar o mesmo bot. Um snapshot fresco foi feito porque mensagens/configuração mudaram após o primeiro restore. Contagens e login Telegram isolados não provam equivalência funcional: credenciais de integrações e perfil web precisavam validação própria. O owner legado u4s dessa tentativa foi removido no replanejamento posterior em favor de openclaw único. Fonte: unidades 31003, 31018, 31027, 31033.

No incidente Telegram de 07/07/2026, a investigação relatou múltiplos gateways em root/openclaw/u4s e um gateway que renascia ao abrir sessão SSH por script de login/profile. A validação de single-writer precisa inspecionar supervisor de sistema, serviços de usuário e inicialização de shell/login, não apenas uma unit conhecida. Conflito 409 indica consumidor concorrente, mas não identifica sozinho a máquina/processo; confirmar origem antes de terminar processos ou reiniciar o host. Fonte: unidades 31105, 31114, 31117, 31153.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 6 de 2026-09-21

No incidente de grupo Telegram, a lição foi consultar primeiro logs/status do canal para separar mensagem recebida, autorização, handler e poller preso; só depois alterar configuração ou reiniciar. Evidência da camada defeituosa evita tentativas amplas e restauração desnecessária de serviço. Fonte: unidades 31791.

No incidente histórico Kowalski, serviço/modelo/Telegram saudáveis não bastaram para encerrar manutenção. A aceitação incluiu resposta real do agente após reinicialização controlada para provar persistência. O número de restarts do episódio não é rotina universal: o teste deve comprovar o caminho funcional solicitado, sem reiniciar agentes desnecessariamente. Fonte: unidades 34443.

Nos testes históricos DRE, a aceitação falhou primeiro por código de saída divergente; depois um exitcode esperado acionou o ERRtrap do harness e outra fixture passou diretório onde o contrato esperava arquivo. Validar códigos de saída por cenário e sua interpretação pelo chamador, além do tipo/caminho dos argumentos. O caso ensina validação de contrato, sem restaurar DRE, repetir ordem ou promover testes antigos a aceite atual. Fonte: unidades 33930, 33987, 33993.

No teste histórico Robotnik/Puppet, bot próprio foi inicialmente implementado como canal no mesmo processo. Isso separa identidade/conversa, mas não falhas, reinícios ou disputa do runtime. Avaliar trabalho paralelo com evidência de contexto, latência e disponibilidade; gateway dedicado requer implantação própria, não pode ser inferido da existência do bot. Fonte: unidades 29557, 29560.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

Falhas históricas DRE: um launcher necessário estava ignorado pelo Git e teria ficado fora do commit; outro funcionava na árvore, mas resolvia caminho errado ao ser instalado em /usr/local/bin. Validar conjunto efetivamente versionado/empacotado e chamada pelo ponto de entrada instalado, sob ambiente mínimo. PASS pré-instalação não substitui aceitação do artefato entregue; não restaurar DRE pelo histórico. Fonte: unidades 29265, 29277.

No CPIW V4, Hebert distinguiu BLOCKED_PENDING_INDEPENDENT_VALIDATION de reprovação da candidata. Recuperar resultado já submetido; se transporte/sessão só ecoou briefing ou não produziu resultado, completar validação sobre os mesmos bytes conforme autorização vigente. Não reconstruir candidata nem trocar hash para resolver falta de evidência. Falha técnica exige gate/comando/esperado/observado reproduzíveis; falha do validador deve ser identificada como tal. Fonte: unidades 32622.

No desenho OCOT Runtime Maintenance, integração proposta era aditiva: novo comando despacha somente ao controlador congelado, sem lógica de limpeza no adaptador e sem segundo binário concorrente. Preservar comandos existentes, help, alvos, argumentos, códigos de saída e unknown-command; comparar inventário/regressão antes e depois. Homologar adaptador não significa instalar/ativar timer ou autorizar limpeza em produção. Fonte: unidades 37512.

No diagnóstico documental, PDFs comprovavam Chromium149, mas não origem Snap/Playwright/pacote/wrapper nem build exato. Cache posterior não prova a origem anterior, e instalar pacote atual não restaura por identidade uma rota histórica. A recomendação posterior revogou o comando apt/Snap proposto: preservar incerteza e obter origem autoritativa ou aprovar nova arquitetura, validando o comando efetivo no PATH. Não executar receita anterior por replay. Fonte: unidades 36663.

No ajuste histórico de modelo/reasoning do OpenClaw, default validado em configuração não alterou automaticamente sessões já abertas. A verificação precisa comparar configuração resolvida e sessão efetiva. Renovar apenas a sessão necessária não implica excluir crons ou histórico de atendimento; versões/modelos citados no episódio não são recomendação atual. Fonte: unidades 35452, 37471, 35449.

No episódio Claw3D, /office HTTP 200 e gateway saudável coexistiram com falha no navegador. A lista vazia resultava de escopo operator.read ausente ao rebaixar identidade do cliente; falhas posteriores vieram de instanceId/assinatura e metadata de plataforma incoerentes no proxy. Validar identidade, escopo, origem e WebSocket ponta a ponta, sem inferir ausência de agentes da UI. localhost no navegador aponta para a máquina do usuário, salvo túnel; correções históricas não dispensam autenticar versão/protocolo atual. Fonte: unidades 35359, 35434, 35356, 35350, 35347.

Em um protótipo de dashboard, foi proposta escuta em loopback com acesso mediado por proxy e allowlist; uma porta local respondendo não comprova publicação remota autorizada. Confirme host, rede, identidade e política de acesso no runtime escolhido antes de expor o painel. Fonte: unidades 29966.

No histórico Claw3D, HTTP 200 da interface não provava handshake do Gateway. Foram diferenciados upstream apontando ao próprio Claw3D, token desatualizado, divergência device/instanceId e metadata distinta entre teste Node e navegador Mac. Diagnóstico deve seguir browser -> proxy -> Gateway e reproduzir a identidade do cliente real; erro 1011/1012 sozinho não identifica a causa. Validar configuração atual e evitar copiar tokens para notas. Fonte: unidades 35348, 35354, 35357, 35360, 35432.

No kit financeiro Telegram antigo, serviço e execução manual simultâneos disputaram o mesmo token. Antes de iniciar uma segunda instância, verificar proprietário e exclusividade de polling; usar lock controlado. Conflito 409 isolado não prova duplicata local e não autoriza matar processos por padrão amplo. Fonte: unidades 35699.

No contrato histórico de manutenção, SQLite candidato exigia validação offline quick_check e checks semânticos antes de compactar/substituir/limpar. Corrupção ou handle ativo bloqueavam mutação e preservavam bytes; evidência identificava PID/processo/cgroup/path. Homologação devia provar equivalência dry-run/real, lock e idempotência. Isso era requisito de segurança, não autorização para ativar cleanup em produção. Fonte: unidades 37508.

No broker SERPRO histórico, uso de setdefault permitia variável herdada do shell prevalecer sobre o arquivo local. Ao diagnosticar configuração, verificar precedência e caminho efetivamente carregado sem expor valores secretos; limpar apenas o ambiente autorizado do processo, não aplicar unset indiscriminado no sistema. Fonte: unidades 38015.

No planejamento histórico Hermes, a inspeção do OpenAPI expôs superfícies MCP/perfis, sem provar a rota tasks antes suposta. A migração foi proposta em fases: conexão, modelo, saneamento, definição de agentes, dry-run e só então cutover. Descobrir contratos no backend real antes de desenhar integração; plano e papéis propostos não comprovam runtime implantado. Fonte: unidades 37439.

Em migração de agentes, um hardlink de banco financeiro visível com modo 0644 não prova isolamento somente leitura: proprietário, mounts e processo efetivo precisam ser conferidos. Compartilhamento entre perfis deve ser explícito; antes do corte, comparar o mesmo input nos runtimes e verificar contratos MCP/concorrência. Modelos e estado de autenticação daquele diagnóstico são históricos. Fonte: unidades 37475.

O payload SERPRO pode trazer dados como JSON serializado dentro de uma string. Decodificar e validar essa camada antes de montar o resumo: uma lista vazia do parser não prova ausência de parcelas/pagamentos na fonte. No incidente histórico, leitura correta recuperou meses pagos; estado atual requer consulta própria. Fonte: unidades 38057.

Verificar origem e dependências do navegador usado pelo executor: um pacote apt de Chromium pode encaminhar para Snap, e o Chromium empacotado pelo Playwright não necessariamente é o binário chromium no PATH. Versão aparente semelhante não prova equivalência de plataforma, serviços ou bibliotecas. Validar o executável concreto e seu ambiente antes de declarar renderização instalada. Fonte: unidades 36662.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

Validar tipo de arquivo por invariantes, não igualdade com a descrição textual stat %F: um arquivo regular vazio pode aparecer como regular empty file. Para transcript, conferir separadamente arquivo regular, ausência de symlink, proprietário/grupo, modo, links e tamanho esperado; um transcript inicial vazio e final não vazio têm critérios diferentes. O caso antigo não autoriza reexecutar o handoff. Fonte: unidades 37058.

Ao verificar checkout de outro usuário num wrapper privilegiado, separar falha de confiança/ownership do Git de divergência real de HEAD. Executar a inspeção com a identidade correta do proprietário, conforme autorização, antes de diagnosticar código alterado. Não ampliar safe.directory globalmente para esconder erro; validar novamente o artefato quando corrigir o wrapper. Fonte: unidades 37505.

Acesso via Tailscale Serve envolve três condições independentes: tailnet permite Serve, identidade local tem autoridade para configurar o daemon e proxy efetivamente aponta ao serviço em loopback. Tailscale conectado/JSON aplicado não comprova acesso remoto. Verificar de cliente autorizado; Serve privado e Funnel público têm exposições distintas. Fonte: unidades 32519.

Sugestão de instalação apresentada na interface Codex não foi entregue automaticamente ao usuário no Telegram. Antes de afirmar que há uma aprovação visível, conferir qual interface/canal realmente a recebe. No incidente Robotnik, corrigiu-se a alegação e o fluxo de integração; valores OAuth não devem compor memória cognitiva, nem a integração antiga deve ser reativada por esta nota. Fonte: unidades 36614.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 9 de 2026-09-21

Na revisão estática Portal213, Gunicorn master e workers compartilhavam listener; ss podia listar worker primeiro, provocando falso rollback. Verificar conjunto completo de PIDs, MainPID numérico não zero pertencente ao conjunto e identidade via /proc/MainPID; registrar início do processo, executável, hash/argc do comando e endereço exato. Repetir após start e restart. A especificação não demonstra instalação nem autoriza executar script root. Fonte: unidades 28887.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

No DRE, fixture usava path onde o contrato exigia relative_path; ausência da chave virou string vazia e foi corretamente rejeitada como UNSAFE_PATH. Conferir esquema efetivo antes de alterar o validador para acomodar teste inválido. Códigos de erro exatos e classes distintas não devem ser normalizados artificialmente apenas para fazer harness passar. Fonte: unidades 9800, 34019.

Para Gunicorn, master e workers podem compartilhar o listener; a ordem dos PIDs no ss não define dono canônico. Usar MainPID do serviço, exigir que esteja no conjunto de PIDs do socket, validar identidade por /proc/MainPID e registrar start-time/executável/hash de comando/endereço. Repetir a verificação após restart autorizado; não reverter serviço saudável porque worker apareceu primeiro. Fonte: unidades 28886.

Na recuperação histórica de instagram-brand-director, inventários com64arquivos coincidiam, mas frontmatter administrativo extra no SKILL.md alterava o hash da árvore. O pacote de evidências validado não continha a árvore candidata completa. Comparar conteúdo canônico/algoritmo de hash e distinguir bundle de evidências de backup restaurável de código antes de afirmar recuperação exata. Fonte: unidades 30718.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 12 de 2026-09-21

No canário histórico Gunicorn/Portal, validação de listener precisou considerar socket compartilhado e pertencimento do MainPID ao conjunto de processos do serviço. Múltiplas identidades de worker não significam necessariamente múltiplos serviços conflitantes. Validar antes/depois de restart e preservar separação entre revisão estática do script e instalação/canário efetivamente executados. Fonte: unidades 28888.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

No episódio da rotina instrucao-diaria-helpdesk-suporte-bikon, configuração exata foi copiada do SQLiteperfilKowalski para storeprincipal e listada única nesta última; legado permaneceu existente. Unicidade em uma store não prova ausência de execução poroutro scheduler. Verificar autoridade efetiva/instâncias antes de chamar globalmente único; horário07:59diasúteis e agenteKowalski são configuração histórica, não instrução atual. Fonte: unidades 9683.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 14 de 2026-09-21

Após a migração histórica de08/07/2026, o supervisor real era openclaw-gateway.service de usuário, com enabled e linger, e executável Node diferente do template sugerido. Não substituir unit saudável só para coincidir com nome/caminho esperado: conferir usuário, supervisor, executável e comportamento após reinício. Linger/enabled e Restart configurados precisam de prova no ambiente aplicável; caminhos e versões do relato não são receita atual. Fonte: unidades 30103.

Na tentativa SentinelA1 de26/07, postcheck detectou gatewayPID diferente, mas starttime do novoPID era anterior a technical_started_at. BASELINE_DIVERGENCE demonstrava baseline inválida, não restart causado pela auditoria. Gate OpenAPI falhou antes deautenticação/dados; zeroGETdedados não significazeroGETdedocumentação. Marker executor-controlled deconsumo era autoridade mesmo com approvalimutável consumed:false; adapter sintético e replay offline não substituíam contrato realSOURCE_SCHEMA_READY. Fonte: unidades 41540.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch14-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
