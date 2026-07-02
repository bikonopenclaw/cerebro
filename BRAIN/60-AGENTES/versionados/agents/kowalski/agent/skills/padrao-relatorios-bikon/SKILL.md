---
name: padrao-relatorios-bikon
description: Use para padronizar, revisar ou montar qualquer relatório/documento Bikon produzido pelo Kowalski, incluindo parecer técnico, relatório executivo, relatório operacional, relatório NinjaOne, ARX Backup, Bitdefender, EOL, inventário, evidências e documentos para cliente. Define estrutura visual/editorial Bikon, guardrails de autoria, checklist antes de PDF/envio e quando acionar skills específicas.
---

# Padrão de relatórios Bikon, Kowalski

## Decisão de arquitetura

Esta é a skill-mãe de padronização. Use para todo relatório Bikon.

Skills específicas continuam responsáveis pelos dados e regras de domínio:

- `ninjaone-relatorios`: coleta e análise NinjaOne/RMM.
- `arx-backup`: relatórios de backup ARX.
- `provimento-213-2026`: diagnóstico e evidências de cartórios.
- `enviar-email-arx-backup`: envio de e-mail ARX após aprovação.

Fluxo correto: skill específica gera o conteúdo técnico, esta skill padroniza apresentação, autoria, linguagem, validação e entrega.

Crie skill nova só quando o tipo de relatório tiver coleta própria, regra técnica própria ou script recorrente próprio. Não crie uma skill só para mudar capa, título ou ordem de seção.

## Modelo aprovado

Referências principais:

- Parecer técnico HTML: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/parecer-tecnico/modelo-padrao-parecer-tecnico-bikon.html`
- Parecer técnico PDF: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/parecer-tecnico/modelo-padrao-parecer-tecnico-bikon.pdf`
- Relatório EOL HTML: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/eol/modelo-padrao-relatorio-eol-bikon.html`
- Relatório EOL PDF: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/eol/modelo-padrao-relatorio-eol-bikon.pdf`
- Timbrado DOCX: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/Bikon_Timbrado.docx`

Para detalhes, leia `references/checklist-relatorio-bikon.md`.

## Estrutura padrão

Todo relatório deve ter, nessa ordem quando fizer sentido:

1. Capa Bikon com título, cliente, período/data e classificação.
2. Resumo executivo em português BR direto.
3. Status geral com badge: OK, Atenção, Crítico ou Informativo.
4. Principais achados, priorizados por impacto.
5. Evidências ou dados analisados, sem despejar tabela inútil.
6. Recomendações práticas, com dono sugerido quando aplicável.
7. Próximos passos.
8. Rodapé/assinatura Bikon.

## Linguagem

- Português BR profissional, direto e sem floreio.
- Falar como Bikon, não como ferramenta.
- Cliente precisa entender risco, impacto e ação.
- Não inventar métrica, data, evidência ou conclusão.
- Nunca usar travessão em material público. Use vírgula, ponto ou parênteses.

## Autoria e solicitante

Obrigatório:

- Não mencionar agente, bot, OpenClaw, Puppet Master, Kowalski, Darth Vader ou Robotnik em documento externo.
- Se o pedido veio do Hebert: solicitante/responsável `Hebert Mattedi`.
- Se o pedido veio do Felipe: solicitante/responsável `Hebert Mattedi e Felipe Nogueira`.
- Assinatura institucional: `Bikon Tecnologia`.

## Identidade visual

- Usar logo e paleta Bikon quando gerar HTML/PDF.
- Nunca entregar com cara genérica de ferramenta.
- Não expor nome de ferramenta interna quando o cliente não precisa ver. Exemplo: use `Bikon RMM` em vez de NinjaOne quando aplicável.
- Para parecer técnico externo, use o modelo aprovado de parecer técnico como base visual.
- Para relatório EOL, End of Life, fim de vida, substituição de equipamento ou obsolescência, use o modelo aprovado de EOL como base visual.

## Validação antes de entregar

Antes de considerar pronto:

```bash
python3 /data/.openclaw/agents/kowalski/agent/skills/padrao-relatorios-bikon/scripts/validar_relatorio_bikon.py CAMINHO_DO_ARQUIVO
```

A validação não substitui revisão humana. Ela pega sujeira operacional comum.

## Bloqueios

Marque como bloqueado antes de entregar se houver:

- caminho local ou `file://` no PDF/HTML/Markdown;
- nome de agente/bot no documento externo;
- dado sem fonte;
- relatório sem cliente, data ou escopo;
- PDF gerado com cabeçalho/rodapé automático do navegador;
- recomendação de compra, troca, cancelamento ou impacto externo sem aprovação quando exigida.

## Saída esperada para o Puppet Master

Quando terminar, responda em 3 linhas:

1. Arquivo gerado/revisado.
2. Resultado da validação.
3. Pendência ou próximo passo.
