# Revisão pré-produção, NFS-e + boleto + remessa

Data: 2026-06-30
Pedido: revisar documentação/processo antes de emitir lote de NFS-e em produção.
Escopo: Notaas NFS-e, boleto Cresol, remessa CNAB400 Cresol, e-mail ao cliente.

## Veredito

Não está liberado para produção no automático.

Está liberado para produção assistida, desde que cada etapa tenha conferência humana e autorização explícita do Hebert antes de executar ação fiscal, bancária ou comunicação externa.

## Bloqueios operacionais para amanhã

1. Cadastro do tomador é o principal risco.
   - O incidente da NFS-e 189 mostrou que nome igual com endereços diferentes gera nota errada.
   - Regra: usar `cliente_id`/cadastro único, não só nome/documento solto.
   - Antes de emitir, conferir CPF/CNPJ, nome, cidade, UF, CEP e endereço completo.

2. Sequenciais não podem ser inferidos no chute.
   - `seq_remessa`, `numero_documento` e `nosso_numero` precisam vir da planilha/processo aprovado.
   - Se faltar qualquer um desses campos, não gerar boleto/remessa de produção.

3. E-mail externo não pode sair junto da emissão.
   - Preparar rascunhos e checklists.
   - Envio real só com aprovação explícita e `job.email.aprovado_por_hebert=true`.

4. Remessa `.rem` não deve ser enviada ao portal Cresol sem validação local e conferência do Hebert.
   - Arquivo precisa ter linhas de 400 posições, CRLF, header `0`, detalhes `1`, trailer `9`.
   - Pelo menos 1 detalhe.
   - Banco `133`, literal `REMESSA`, serviço `COBRANCA`.

## Pontos de atenção

1. PDF da Notaas pode atrasar ou falhar.
   - Em produção anterior houve HTTP 503 no download do PDF.
   - XML é o artefato técnico confiável imediato.
   - Não enviar e-mail ao cliente sem PDF + XML conferidos.

2. Competência retornada no XML precisa ser conferida.
   - No caso Celi, payload enviou `2026-06`, XML retornou `2026-06-26` em `dCompet`.
   - Amanhã conferir competência em cada XML, não só no payload.

3. Desconto/valor total.
   - No lote de homologação de 26 notas houve casos em que soma dos itens divergia do valor total.
   - Regra: valor total só pode ser soberano se Hebert confirmar isso para o lote.

4. Gerador de boleto e remessa não envia nada sozinho.
   - Ele gera arquivo local.
   - A etapa perigosa é upload/envio no banco e envio ao cliente.

## O que está OK

1. Notaas NFS-e tem dry-run e trava emissão real sem `--confirmar-emissao`.
2. Cancelamento também exige confirmação específica.
3. E-mail ao cliente tem checklist e bloqueio por aprovação.
4. Remessas de referência/homologação validadas têm estrutura CNAB400 correta.
5. Gerador CNAB400 atual suporta CPF e CNPJ no pagador.
6. Há mapa técnico de remessa real Cresol em produção para comparação.

## Checklist mínimo de amanhã

### Antes de emitir NFS-e

- [ ] Planilha/base do lote congelada.
- [ ] Cada linha com `cliente_id` ou identificador único.
- [ ] CPF/CNPJ válido.
- [ ] Endereço completo conferido, principalmente clientes com mesmo nome ou múltiplos cadastros.
- [ ] Serviço: `GERENCIAMENTO, CONTROLADORIA E MONITORAMENTO DE RECURSOS DE REDE`, salvo exceção explícita.
- [ ] Código serviço conferido.
- [ ] Valor total conferido.
- [ ] Competência conferida.
- [ ] Retenções marcadas como sim, não ou não se aplica.
- [ ] Hebert autorizou emissão real da NFS-e.

Frase de liberação esperada: `CONFIRMO EMISSÃO DA NOTA`

### Depois de emitir NFS-e

- [ ] Status Notaas `issued`.
- [ ] Invoice ID salvo.
- [ ] Número da NFS-e salvo.
- [ ] XML baixado.
- [ ] PDF baixado ou marcado como pendência se Notaas falhar.
- [ ] XML conferido: tomador, endereço, valor, serviço, competência.
- [ ] Qualquer divergência para o lote inteiro.

### Antes de gerar boleto/remessa

- [ ] Número documento definido.
- [ ] Nosso número definido e DV validado.
- [ ] Sequencial de remessa definido.
- [ ] Vencimento conferido.
- [ ] Valor do boleto igual ao valor autorizado.
- [ ] Multa/juros/desconto/abatimento conferidos.
- [ ] Hebert autorizou geração real.

Frase de liberação esperada: `CONFIRMO GERAÇÃO DO BOLETO/REMESSA`

### Antes de enviar ao portal Cresol

- [ ] Remessa local validada.
- [ ] Todas as linhas com 400 caracteres.
- [ ] Header/detalhe/trailer OK.
- [ ] Quantidade de títulos bate com o lote.
- [ ] Valor total bate com o lote.
- [ ] Nome do arquivo e sequencial conferidos.
- [ ] Hebert autorizou upload/envio.

Frase de liberação esperada: `CONFIRMO ENVIO AO PORTAL CRESOL`

### Antes de enviar e-mail ao cliente

- [ ] PDF da NFS-e anexado.
- [ ] XML anexado.
- [ ] Boleto PDF anexado quando houver boleto.
- [ ] Destinatário financeiro conferido.
- [ ] Checklist sem bloqueio.
- [ ] Aprovação explícita do Hebert.

## Evidências revisadas

- `/data/.openclaw/workspace-darth-vader/boletos/modelos/checklist-dados-emissao-nota-boleto.md`
- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/SKILL.md`
- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/emitir_nota.py`
- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/emitir_lote.py`
- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_email_cliente.py`
- `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_boleto_cresol_html.py`
- `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_remessa_cnab400_cresol.py`
- `/data/.openclaw/workspace-darth-vader/boletos/lotes-emissao/validacao-20260619-nfse-massa/status-final-homologacao.md`
- `/data/.openclaw/workspace-darth-vader/boletos/pacotes-emissao/20260626-celi-aracruz-nfse-producao/relatorio-emissao.md`
- `/data/.openclaw/workspace-darth-vader/boletos/pacotes-emissao/20260626-celi-joao-neiva-correcao/auditoria/incidente-nfse-189-celi.md`
- `/data/.openclaw/workspace-darth-vader/boletos/remessas/producao/mapa-tecnico-ultimo-arquivo-producao-20260626-1123.md`

## Validação executada

- `py_compile` nos scripts principais de NFS-e, boleto, remessa e e-mail: OK.
- Remessa homologação `remessa-090-190626-final-homologacao.rem`: 28 linhas, todas com 400 posições, registros `0/1/9`, CRLF: OK.
- Última remessa produção `ultimo-arquivo-producao-20260626-1123.rem`: 3 linhas, todas com 400 posições, registros `0/1/9`, CRLF: OK.

## Recomendação final

Amanhã fazer em modo assistido:

1. Dry-run do lote.
2. Conferência do relatório de pendências.
3. Aprovação do Hebert para emitir NFS-e.
4. Emissão NFS-e.
5. Conferência XML/PDF.
6. Só depois boleto/remessa.
7. Só depois envio ao cliente ou portal Cresol.

Não rodar NFS-e + boleto + remessa + e-mail como esteira única sem pausa. Foi exatamente assim que erro cadastral vira retrabalho fiscal.
