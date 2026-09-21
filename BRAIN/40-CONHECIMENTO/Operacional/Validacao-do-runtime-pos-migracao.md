---
id: brain-2acb877be050e1fb027d
type: knowledge
title: Validação do runtime pós-migração
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T21:16:57.672344Z'
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

## Complementos reconciliados — lote 15 de 2026-09-21

Na investigação histórica da instrução Helpdesk às 07:59 BRT em dias úteis, a busca no state principal não encontrou a rotina; ela existia no SQLite do perfil Kowalski. Um storePath anunciado para JSON não provava arquivo ativo quando storage era SQLite. Conferir identidade do processo, perfil e banco efetivamente consumido antes de declarar ausência ou criar/editar job; registro em banco alternativo também precisa de prova de uso pelo scheduler ativo. Não editar rotinas vizinhas por proximidade de horário, nem reativar IDs antigos pelo histórico. Fonte: unidades 9682.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

Em 17/07/2026, após a incerteza sobre a origem do Chromium anterior, foi instalada uma rota nova e fixada: cópia do runtime Playwright para /opt/bikon/chromium-149.0.7827.55, seguida de root ownership e link global. cp -a havia preservado o dono openclaw; conferir propriedade dos bytes, não apenas do diretório pai. O binário headless gerou PDF de teste, e Poppler foi instalado para concluir metadados; esse checkpoint ainda não comprovava relatório real nem equivalência com a origem antiga. É registro histórico, não recomendação de versão ou receita de reinstalação atual. Fonte: unidades 36685.

No diagnóstico histórico Praxis/Drive em 27/07, Gmail/Drive/Calendar passaram via API, mas a auditoria autorizada pelo visualizador continuou parada: Chromium/CDP respondia e a página chegava ao login, sem sessão Google utilizável. Restauração do navegador não comprova autenticação nem leitura do documento. Autenticação interativa foi a opção aprovada; não ampliar a permissão da pasta nem substituir pela API silenciosamente. Inventário de 1.000 itens não prova leitura do conteúdo; não preservar callbacks, códigos ou tokens no Brain. Fonte: unidades 32654.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 18 de 2026-09-21

Após a instalação histórica da rota Chromium em 17/07, o PDF reproduziu metadados HeadlessChrome 149/Skia m149 e página A4, mas o gate visual falhou de forma repetível: logo PNG omitido e cabeçalho deslocado. Metadados compatíveis não provam equivalência visual. Hebert autorizou adaptar o template usando o brand pack já salvo; a fonte termina nessa autorização e não comprova correção aplicada ou relatório real entregue. Não retomar a sugestão Snap anteriormente revogada. Fonte: unidades 36687.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch18-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 20 de 2026-09-21

Na implementação histórica EP-02, a primeira clean room passou os inventários e correções de tipo/null, mas terminou com 22 testes aprovados e um erro: o teste de isolamento precisava do documento canônico EP-02, que o harness não havia incluído entre os insumos de leitura. Definir separadamente inventário de código extraído e dependências documentais de validação; autenticar ambos antes da suíte. Não enfraquecer o teste nem declarar defeito produtivo para compensar fixture incompleta. O checkpoint foi anterior à homologação posterior e não descreve bloqueio atual. Fonte: unidades 31709.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch20-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 21 de 2026-09-21

Na correção histórica do harness DRE v4, FIXTURE_ROOT era diretório e FIXTURE_MANIFEST arquivo regular: --package devia receber o manifest, enquanto operações sobre a árvore usavam a raiz. O preflight direto com manifest passou sem instalar ou alterar o core. Revisar semanticamente os argumentos da rota real e testar o helper de códigos de saída; preparar/validar um instalador não prova instalação ou aceite black-box. O freeze dos mesmos 12 caminhos entre commits não dispensa validar o wiring externo. Fonte: unidades 30785, 30788.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch21-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 23 de 2026-09-21

Após concluir historicamente as 27 NFS-e e obter os 54 PDFs/XMLs da remessa 093, a preparação de boletos encontrou reportlab ausente no Python chamado e depois PIL._imaging quebrado: a pasta .pydeps-pdf sombreava dependências funcionais de .venv-pdf. Verificar o interpretador, sys.path e a origem efetiva do módulo antes de reinstalar dependências ou alterar o Python global. Essa falha era da etapa PDF/boletos, não prova de falha das NFS-e já emitidas; emissão, remessa e envio externo têm comprovação própria e sucessiva. Fonte: unidades 3410.

Na continuação da homologação EP-02, duas clean rooms passaram 23/23 testes após incluir o documento normativo exigido: eram 55 arquivos técnicos e um documento adicional de validação. Isso supera a primeira tentativa com 22 PASS e um erro de isolamento. O commit posterior tinha os 55 caminhos técnicos esperados; diferença de ordem no git diff não mudava o conjunto. O manifesto, porém, devia respeitar a ordem contratual da Seção 12 e o newline final, pois seus bytes participavam do hash. Separar contagem de código, dependências de validação, igualdade de conjuntos e serialização. Fonte: unidades 8861.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch23-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 25 de 2026-09-21

Na apuração de 17/07/2026, a consulta apenas repetiu banner da migração realizada em 16/07: 31 arquivos legados originaram 199 entradas, e os pares de run logs eram byte a byte iguais. Não houve nova migração na janela investigada nem backup novo; o comando histórico exato não pôde ser recuperado. SQLite/WAL/SHM mudavam por operação normal, e store_key podia manter caminho JSON já inexistente sem ser a fonte operacional. Rollback sem snapshot prévio poderia perder estado posterior ou duplicar jobs, portanto não foi indicado para o falso incidente. Separar leitura, reconciliação e autorização de mudanças. Na mesma conversa, o usuário pediu progresso nativo das ferramentas no Telegram, sem mensagens artificiais de progresso; configuração via documento temporário exigia excluir o documento após validação, sem copiar segredo para memória. Fonte: unidades 9436.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch25-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 26 de 2026-09-21

Na consolidação documental de 17/07, praxis-gws era camada de acesso/transporte, sem substituir geradores, fórmulas, templates ou periodicidade. O gate técnico da cópia local e do scanner de segredos não comprovava autenticação nem operação externa. O relatório executivo de fechamento parou ao importar docx no Python de sistema, antes de criar DOCX/PDF/render; um DOCX de proposta anterior era outro artefato. Localizar e validar o interpretador e a rota Bikon já existentes antes de instalar pacote ou trocar ferramenta. Preservar modelos canônicos e confirmar conteúdo, renderização e hashes na rota efetivamente autorizada; não converter uma falha de ambiente em permissão para remover a integração duplicada. Fonte: unidades 9453.

Na consolidação histórica Praxis GWS para Kowalski, a cópia autorizada de 19 arquivos foi seguida por checagem sintática de 14 arquivos JavaScript, sem chamadas externas, OAuth ou restart. Isso não comprovava operação das APIs. Uma primeira busca de padrões de segredo falhou por interpretar o padrão como opção; somente a execução corrigida podia sustentar resultado negativo. O gog instalado/desativado permaneceu intocado. A tentativa de produzir relatório DOCX/PDF de fechamento falhou por ausência de python-docx no interpretador usado; descobrir outro ambiente virtual ainda não provava geração. Relatório proposto anterior não substitui artefato final recebido, e falha histórica não descreve dependências atuais. Fonte: unidades 9458.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch26-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
