---
name: emitir-nfse-boleto-remessa
description: Use quando o pedido envolver emissão ou preparação de NFS-e, boleto Cresol e arquivo de remessa bancária em um fluxo único, especialmente a partir de nota/boleto anterior. Orquestra emissão fiscal, geração de boleto, remessa CNAB400/CNAB240 e validações, com travas para não afirmar emissão real sem comprovante.
---

# Emitir NFS-e, boleto e remessa

Use esta skill para fluxos como:

- “emita a nota igual ao mês passado, gere boleto e remessa”
- “crie NFS-e, boleto Cresol e arquivo `.rem`”
- “teste emissão de nota/boleto/remessa para homologação”
- “repita a cobrança do cliente X com vencimento Y”
- “emita uma lista/lote de notas com boleto e remessa”

## Regra de ouro

Não afirmar que NFS-e ou boleto foram emitidos sem comprovante real.

Estados permitidos:

- `rascunho_preparado`: dados montados, nada emitido.
- `nfse_emitida`: somente com DANFSe/XML/chave retornada pelo emissor.
- `boleto_emitido_homologacao`: PDF/linha digitável/código de barras gerados pela skill para conferência.
- `boleto_emitido`: somente com PDF/linha digitável/nosso número confirmado pelo sistema/banco.
- `remessa_gerada_homologacao`: arquivo `.rem` para teste, não produção.
- `remessa_validada_homologacao`: arquivo `.rem` validado pelo ambiente de teste do banco.
- `remessa_pronta_producao`: só depois de homologação bancária aprovada pelo Hebert e ordem explícita para produção.

## Travas de segurança

- Emissão fiscal real é ação externa. Se não houver acesso/API/sessão do emissor, preparar o rascunho e parar.
- Boleto real pode gerar cobrança. Se não houver retorno do sistema/banco, tratar como boleto de homologação/conferência, mesmo que o PDF esteja correto.
- Remessa bancária pode registrar, alterar, baixar ou protestar títulos. Nunca subir no banco. O Hebert faz a validação ou autoriza explicitamente.
- Não usar valor de segunda via com multa/mora como valor base de nova cobrança. Para nova emissão, usar valor original da NFS-e, salvo ordem explícita.
- Não inventar número de NFS-e. Se o emissor ainda não retornou número/chave, usar `pendente`.

## Caminhos

- Workspace boleto/remessa: `/data/.openclaw/workspace-darth-vader/boletos`
- Cadastro mestre de clientes ativos: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.json`
- Cadastro tabular: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.csv`
- E-mails financeiros separados: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_emails_financeiro.csv`
- Banco SQLite do cadastro: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.sqlite`
- Inconsistências do cadastro: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/inconsistencias.md`
- Ferramenta de manutenção do cadastro: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/scripts/clientes_tool.py`
- Configuração de e-mail NFS-e Bikon: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/config/email.json`
- Template HTML padrão dos e-mails NFS-e Bikon: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/templates/email_nfse_bikon.html`
- Gerador de rascunho/envio controlado de e-mail NFS-e: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_email_cliente.py`
- Skill técnica Cresol: `/data/.openclaw/agents/darth-vader/agent/skills/boletos-cresol/SKILL.md`
- Gerador boleto HTML/PDF homologação: `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_boleto_cresol_html.py`
- Gerador CNAB400 homologação: `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_remessa_cnab400_cresol.py`
- Pacotes do fluxo: `/data/.openclaw/workspace-darth-vader/boletos/pacotes-emissao`

## Workflow obrigatório

1. Buscar tomador/pagador no cadastro mestre de clientes ativos antes de montar NFS-e/boleto.
2. Se o cadastro tiver inconsistência crítica para o cliente, parar e pedir correção ao Hebert antes de emitir.
3. Se o cliente tiver mais de um e-mail financeiro, preservar todos no job/rascunho/envio.
4. Extrair dados da NFS-e anterior e do boleto anterior quando aplicável.
5. Montar um job JSON do novo ciclo em `pacotes-emissao/YYYYMMDD-cliente/`.
6. Validar dados mínimos:
   - prestador
   - tomador
   - serviços/itens
   - valor original
   - vencimento
   - documento
   - nosso número ou regra para próximo número
   - pagador
   - conta/carteira/cooperativa Cresol
7. Separar o fluxo em 3 blocos:
   - NFS-e
   - boleto
   - remessa
8. Se não houver acesso ao emissor fiscal, marcar NFS-e como `rascunho_preparado` e listar exatamente o que falta para emitir.
9. Se não houver acesso ao sistema do boleto/banco, gerar apenas remessa de homologação e marcar boleto como `rascunho_preparado`.
10. Gerar boleto PDF limpo para conferência, com linha digitável, código de barras e nosso número calculados.
11. Gerar `.rem` somente com dados coerentes e validar linha de 400 caracteres, header/detalhe/trailer e CRLF.
12. Se Hebert informar que a remessa validou no banco, atualizar o pacote/status para `remessa_validada_homologacao`; não considerar produção automaticamente.
13. Preparar e-mail automático para o cliente quando a NFS-e real tiver PDF/XML baixados:
   - usar e-mails financeiros do cadastro mestre ou `tomador.email`/`email.to` do job
   - anexar DANFSe PDF, XML da NFS-e e boleto PDF quando houver
   - usar o template HTML padrão Bikon e fallback texto simples
   - gerar `email-nfse-cliente.eml` e `email-nfse-cliente.json` no pacote
   - envio real para cliente externo exige autorização explícita do Hebert e `job.email.aprovado_por_hebert=true`
   - se faltar e-mail financeiro, bloquear envio e marcar pendência cadastral
   - em teste controlado, enviar apenas para destinatário explícito, sem buscar cadastro do cliente
14. Entregar ao Hebert:
   - status da NFS-e
   - status do boleto
   - status da remessa
   - status do e-mail ao cliente
   - arquivos gerados
   - pendências objetivas

## Lote como padrão operacional

O padrão definido pelo Hebert é entregar uma lista de notas para emitir em lote. Quando receber lista/planilha/CSV:

1. Ler `references/lote-schema.md`.
2. Converter cada linha em job individual.
3. Rodar o script de lote.
4. Entregar `status-lote.md`, boletos/remessas gerados e pendências por linha.

Para processar CSV:

```bash
/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/scripts/preparar_lote_emissao.py --csv /caminho/lote.csv
```

## Script auxiliar

Para criar pacote operacional e remessa a partir de JSON:

```bash
/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/scripts/preparar_pacote_emissao.py --job /caminho/job.json
```

Leia `references/job-schema.md` quando precisar montar ou validar o JSON.
Leia `references/lote-schema.md` quando o Hebert entregar uma lista de notas para emitir em lote.
Leia `references/modelo-geral-validado.md` quando for repetir o fluxo completo ou alterar scripts. O caso Unus é golden case validado, mas o modelo é geral e parametrizado por job.

## Integração com boletos-cresol

Quando o pedido envolver Cresol/CNAB, use também a skill `boletos-cresol` para detalhes de layout, cálculo de DV, validação e restrições bancárias.

## Resposta padrão para o Hebert

Sempre responder em 3 linhas:

1. O que foi pedido.
2. O que foi entregue, separando NFS-e, boleto e remessa.
3. Próximo passo sugerido ou bloqueio real.
