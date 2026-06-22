---
name: boletos-cresol
description: Use para trabalhar com boletos Cresol banco 133, CNAB400/CNAB240, remessa .rem, retorno .ret, malote bancário, validação de layout, cálculo de nosso número, linha digitável e código de barras. Não gera arquivo real de cobrança sem validação explícita/homologação.
---

# Boletos Cresol, remessa e retorno

Use esta skill quando o pedido envolver boleto Cresol, Banco 133, CNAB400, CNAB240, remessa, retorno, malote, arquivo `.rem`, arquivo `.ret`, nosso número, linha digitável ou código de barras.

## Regra de segurança

Arquivo de remessa bancária real pode gerar cobrança, baixa, protesto ou alteração de título.

Nunca enviar, protocolar, subir em banco, homologar em ambiente externo ou marcar como pronto para produção sem aprovação explícita do Hebert/Puppet Master.

Até validação final, tratar qualquer `.rem` gerado como **rascunho técnico**.

## Workspace

- Workspace: `/data/.openclaw/workspace-darth-vader/boletos`
- Exemplos de boleto: `/data/.openclaw/workspace-darth-vader/boletos/exemplos`
- Modelos de entrada: `/data/.openclaw/workspace-darth-vader/boletos/modelos`
- Layout oficial Cresol/FastReport: `/data/.openclaw/workspace-darth-vader/boletos/modelos/modelo-boleto-cresol-oficial.fr3.xml`
- Gerador visual do boleto: `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_boleto_cresol_html.py`
- Manuais Cresol: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol`
- Remessas: `/data/.openclaw/workspace-darth-vader/boletos/remessas`
- Retornos: `/data/.openclaw/workspace-darth-vader/boletos/retornos`

## Documentos recebidos e status

Documentos novos recebidos em 2026-06-15:

- Boleto exemplo: `/data/.openclaw/workspace-darth-vader/boletos/exemplos/Boleto_exemplo_6_1.pdf`
- Especificações técnicas boleto/código de barras/linha digitável: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/Especificacoes_tecnicas_5_1.pdf`
- Remessa CNAB400 Cresol 133: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/Padrao_Remessa_CNAB400_Cresol_133_5_1.pdf`
- Remessa e retorno CNAB240 Cresol 133: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/Padrao_Remessa_e_Retorno_CNAB240_Cresol_133_5_1.pdf`
- Retorno CNAB400 Cresol 133: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/Padrao_Retorno_CNAB400_Cresol_133_5_1_1.pdf`

Textos extraídos ficam no mesmo diretório com extensão `.txt`.

## Referências estruturadas

- Catálogo: `references/catalogo-documentos-cresol.md`
- Mapa remessa CNAB400: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/mapa-remessa-cnab400-cresol-133-v5_1.json`
- Mapa retorno CNAB400 antigo/novo: `/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/mapa-retorno-cnab400-cresol-133.json`
- Exemplo válido antigo de remessa CNAB400: `/data/.openclaw/workspace-darth-vader/boletos/remessas/exemplos/exemplo-malote-20260614-015740.rem`
- Exemplos reais recentes/golden files:
  - `/data/.openclaw/workspace-darth-vader/boletos/remessas/exemplos/cb010601.rem`, multi-título, 25 detalhes, total R$ 84.713,06, seq remessa `0000083`.
  - `/data/.openclaw/workspace-darth-vader/boletos/remessas/exemplos/cb110501.rem`, unitário, 1 detalhe, total R$ 585,00, seq remessa `0000082`.
- Análise dos golden files: `/data/.openclaw/workspace-darth-vader/boletos/remessas/exemplos/analise-malotes-reais-cb010601-cb110501.md`
- JSON comparativo dos golden files: `/data/.openclaw/workspace-darth-vader/boletos/remessas/exemplos/analise-comparativa-cb010601-cb110501.json`
- Exemplo inválido/template negativo: `/data/.openclaw/workspace-darth-vader/boletos/remessas/exemplos/exemplo-malote-20260614-0223-133_CNAB400_1008_27846.rem`

## Decisão CNAB400 vs CNAB240

- CNAB400 agora tem PDF de remessa e retorno, então pode avançar para implementação com validação forte.
- CNAB240 também tem manual completo, mas só usar se Hebert confirmar que a conta Cresol aceita CNAB240.
- Não misturar layouts. CNAB400 usa registros de 400 posições: `0`, `1`, `9`. CNAB240 usa registros de 240 posições com segmentos.


## Fluxo completo com NFS-e

Quando o pedido envolver emissão/preparação de **NFS-e + boleto + remessa** no mesmo fluxo, use primeiro a skill orquestradora:

`/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/SKILL.md`

Esta skill `boletos-cresol` fica como apoio técnico para layout bancário, DV, CNAB, validação e golden files.

## Workflow seguro para remessa CNAB400

1. Ler dados de entrada de CSV/JSON aprovado.
2. Validar campos obrigatórios: beneficiário, carteira, cooperativa, conta, nosso número, documento, vencimento, valor, pagador, CPF/CNPJ, endereço, espécie, ocorrência.
3. Calcular ou validar DV do nosso número usando especificação técnica.
4. Montar linhas de 400 caracteres.
5. Validar estrutura: header `0`, detalhes `1`, trailer `9`, sequencial correto, tamanho exato 400 por linha.
6. Comparar com os golden files `cb010601.rem` e `cb110501.rem` quando aplicável.
7. Salvar como rascunho em pasta de homologação/local.
8. Pedir aprovação antes de qualquer uso externo.

## Validações obrigatórias

- Toda linha CNAB400 deve ter 400 caracteres antes do CRLF.
- Arquivo CNAB400 deve ter ao menos 3 linhas: header, 1 detalhe, trailer.
- Header deve começar com `0`.
- Detalhe deve começar com `1`.
- Trailer deve começar com `9`.
- Rejeitar arquivos com apenas registros `0` e `0`, como o exemplo negativo recebido.
- Rejeitar remessa real se campos 150-400 ainda não tiverem sido conferidos contra o PDF renderizado/manual e contra os golden files reais.

## Campos confirmados previamente da conta/exemplo

- Banco: `133`
- Carteira: `009`
- Cooperativa: `01008`
- Conta: `0027846-7`
- Sequencial remessa exemplo: `0000032`
- Ocorrência de entrada: `01`
- Condição emissão papeleta: `2`
- Multa exemplo: `2,00%`
- Nosso número base exemplo: `00000000826`, DV `8`
- Documento exemplo: `33601`
- Vencimento exemplo: `24/10/2024`
- Valor exemplo: `R$ 5.230,93`
- Espécie exemplo: `02`, duplicata mercantil

## Layout visual do boleto

- Modelo padrão aprovado por Hebert em 2026-06-17: `BIKON_APPROVED_CRESOL_BOLETO_LAYOUT_OFICIAL_20260617`.
- Para gerar HTML/PDF de boleto, usar o layout oficial Cresol salvo em `modelos/modelo-boleto-cresol-oficial.fr3.xml`.
- Cópia aprovada do modelo fica em `modelos/aprovados/modelo-padrao-boleto-cresol-oficial.fr3.xml`.
- PDF vazio aprovado para referência fica em `modelos/aprovados/modelo-padrao-boleto-cresol-vazio-aprovado.pdf`.
- O gerador `scripts/gerar_boleto_cresol_html.py` renderiza o XML FastReport por coordenadas absolutas para preservar o visual: comprovante de entrega, recibo do pagador e ficha de compensação.
- Código de barras aprovado na escala final: `barHeight=23.4mm`, `barWidth=0.624mm`, imagem renderizada em `494px x 68px`.
- Este é o ÚNICO layout/modelo visual permitido para emissão de boleto Cresol da Bikon.
- Modelos antigos, templates extraídos, gerador PDF legado e versões de validação foram removidos em 2026-06-17 para evitar uso acidental.
- Não voltar ao layout genérico em grid/CSS, não reduzir escala do código de barras e não trocar o layout padrão sem aprovação do Hebert/Puppet Master.
- Se encontrar outro arquivo dizendo ser modelo/layout de boleto Cresol, ignorar e avisar o Puppet Master antes de usar.
- Antes de aprovar qualquer mudança visual futura, gerar PDF de teste e conferir se linha digitável, nosso número, agência/conta, pagador, instruções e código de barras continuam aparecendo.

## Linguagem

Relatórios internos em português BR, diretos e técnicos. Para banco, zero criatividade: seguir manual.
