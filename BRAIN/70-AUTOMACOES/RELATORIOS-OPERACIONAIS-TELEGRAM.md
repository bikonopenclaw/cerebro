# Relatórios Operacionais Telegram

```yaml
categoria: canal_operacional
fonte: decisão do Hebert em 2026-06-22
confiabilidade: alta
ultima_revisao: 2026-06-23
tags: [telegram, relatorios, kowalski, ninjaone, operacao]
```

## Finalidade

Registrar o canal Telegram `relatórios operacionais` como grupo de consulta e produção de relatórios do dia a dia da Bikon.

## Grupo

- Nome: `relatórios operacionais`
- Chat observado: `telegram:-5165906669`
- Agente responsável: Kowalski
- Tipo de uso: consulta, relatório e análise operacional.

## Escopo permitido

- Relatórios operacionais para clientes.
- Consulta a dados NinjaOne quando houver acesso/fonte disponível.
- Relatórios por dispositivo, alertas, inventário, disponibilidade, backup e evidências técnicas.
- Pareceres técnicos em linguagem Bikon quando aprovados pelo fluxo.

## Fora de escopo

- Alterar estrutura operacional do Kowalski.
- Alterar skills, arquivos, configurações ou processos do Kowalski a partir do grupo.
- Acionar Puppet Master/main de forma independente pelo grupo.
- Acionar Darth Vader ou outro agente sem coordenação de Puppet Master.
- Comunicação externa para cliente sem aprovação explícita.
- Mudança em produção, faturamento, cobrança, site, checkout ou integração.

## Regra de identidade visual

Hebert decidiu não criar bot Telegram separado para Kowalski neste momento.

Padrão visual:

- Respostas no grupo devem começar com `Kowalski:` ou identificação textual equivalente.
- A identidade visual no Telegram continua sendo o bot atual.
- A clareza de autoria deve vir do texto, não de bot separado.

## Padrão visual para relatórios externos

Em 2026-06-23, após revisão da versão premium do parecer do Cartório Capixaba, ficou registrado como padrão operacional para PDFs externos da Bikon:

- Usar identidade visual Bikon com acabamento corporativo e leitura séria.
- Evitar aparência de HTML impresso.
- Remover cabeçalhos e rodapés automáticos de navegador/documento, incluindo data técnica, caminho, URL, título repetido e paginação visualmente pobre.
- Manter apenas elementos institucionais quando fizerem parte natural do layout.
- Preservar conteúdo técnico, conclusões e estrutura quando a solicitação for apenas ajuste visual.
- Conferir visualmente o PDF renderizado antes de enviar ao Hebert ou ao grupo.

## Guardrails

- Se o NinjaOne ou outra fonte não tiver histórico granular de CPU, RAM, disco ou eventos, registrar a limitação sem inventar métrica.
- Não incluir caminho interno de arquivo em relatório final para cliente.
- Relatório externo deve sair limpo, profissional e sem comentário operacional.
- Usuários adicionados por Hebert podem consultar dentro do grupo, mas não ganham permissão para acionar outros agentes.

## Caso de uso inicial

Em 2026-06-22, o grupo foi usado para solicitar parecer técnico do Cartório Capixaba:

- Incluir embasamento no Provimento CNJ 213/2026.
- Remover referência a local/caminho de arquivo no relatório.
- Tentar usar dados históricos por dispositivo.
- Evidenciar CPU, memória, disco, alertas e gargalos quando auditáveis.
- Gerar PDF para cliente externo.

Resultado: Kowalski gerou e enviou PDF no grupo, com ressalva explícita sobre limitações de histórico granular quando a fonte não retornou séries contínuas.

## Relações

- Agente Kowalski: `BRAIN/60-AGENTES/KOWALSKI.md`
- Escopo de canais operacionais: `BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md`
- Bikon: `BRAIN/20-EMPRESAS/BIKON/README.md`
