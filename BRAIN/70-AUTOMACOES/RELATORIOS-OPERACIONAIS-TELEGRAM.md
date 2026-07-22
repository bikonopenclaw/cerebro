# Relatórios Operacionais Telegram

```yaml
categoria: canal_operacional
fonte: decisão do Hebert em 2026-06-22
confiabilidade: alta
ultima_revisao: 2026-07-22
tags: [telegram, relatorios, kowalski, ninjaone, eol, operacao, gateway, identidade-visual]
```

## Finalidade

Registrar o canal Telegram `relatórios operacionais` como grupo de consulta e produção de relatórios do dia a dia da Bikon.

## Grupo

- Nome: `relatórios operacionais`
- Chat observado: `telegram:-5165906669`
- Agente responsável: Kowalski
- Tipo de uso: consulta, relatório e análise operacional.

## Roteamento Telegram em 2026-07-09

Hebert autorizou a evolução do grupo para canal isolado do Kowalski:

- Bot Kowalski: `@mattedi_02_bot`.
- Gateway dedicado: `openclaw-gateway-kowalski.service`.
- Porta dedicada: `18810`.
- Puppet Master continua no grupo, mas com `requireMention=true`.
- Kowalski fica com resposta direta para mensagens comuns dentro do escopo de relatórios operacionais.
- A coordenação agente-a-agente e decisões com impacto continuam sob Puppet Master.

Token, auth store e configuração sensível ficam fora do Brain/Git.

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

## Regra de identidade no grupo

Com bot próprio validado, mensagens comuns do grupo devem ser tratadas pelo Kowalski quando forem de relatório operacional. Puppet Master só deve responder quando mencionado nominalmente ou quando houver coordenação, mudança estrutural, produção, gasto, comunicação externa ou decisão estratégica.

## Padrão visual para relatórios externos

Em 2026-06-23, após revisão da versão premium do parecer do Cartório Capixaba, ficou registrado como padrão operacional para PDFs externos da Bikon:

- Usar identidade visual Bikon com acabamento corporativo e leitura séria.
- Evitar aparência de HTML impresso.
- Remover cabeçalhos e rodapés automáticos de navegador/documento, incluindo data técnica, caminho, URL, título repetido e paginação visualmente pobre.
- Manter apenas elementos institucionais quando fizerem parte natural do layout.
- Preservar conteúdo técnico, conclusões e estrutura quando a solicitação for apenas ajuste visual.
- Conferir visualmente o PDF renderizado antes de enviar ao Hebert ou ao grupo.

## Guardião visual Bikon

Em 2026-07-09, a responsabilidade visual do Kowalski foi ampliada para além de relatórios:

- revisar post, carrossel, PDF, apresentação, proposta, landing page, template e material público ou semi-público com logo/paleta/layout da Bikon;
- devolver veredito, três ajustes prioritários e risco visual principal;
- manter Robotnik como responsável por pauta, copy e campanha;
- evitar que estética hacker/cyberpunk, SaaS genérico, excesso de texto ou promessa exagerada chegue à peça final;
- não publicar, enviar, agendar ou aplicar mudança externa sem aprovação explícita.

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


## Ajuste visual ARX em 2026-07-02

Um PDF enviado no grupo precisou ser refeito com o conteúdo recebido encaixado dentro do layout ARX/Bikon. O caso reforça o padrão:

- preservar conteúdo técnico aprovado;
- aplicar identidade visual Bikon/ARX quando o pedido for formatação externa;
- remover vestígios de caminho local, metadados de impressão, nome de agente ou comentário operacional;
- validar o arquivo final antes do envio.

## Lista de clientes NinjaOne em 2026-07-07

Solicitação no grupo pediu lista simples de clientes cadastrados no NinjaOne. O registro relevante para o Brain é o padrão operacional: quando o pedido for apenas listagem em texto, responder de forma simples no próprio chat e evitar gerar artefato, PDF ou relatório final desnecessário.

## Modelo de Relatório EOL Bikon, 2026-07-13

Hebert aprovou como padrão oficial para próximos relatórios de EOL o `Modelo de Relatório EOL Bikon`.

Regras consolidadas:

- não nomear o modelo por cliente;
- usar PDF com identidade Bikon, capa limpa, cards de KPI, tabela com cabeçalho escuro e legendas/badges condensados;
- manter a lógica: software EOL vira ação interna Bikon; compra física entra apenas quando houver hardware classificado para substituição;
- validar capa, paginação, legenda em uma linha, ausência de termos internos e exportação final em PDF antes de enviar;
- manter PDFs finais e lotes gerados fora do Brain/Git.

## Correção do dossiê técnico em 2026-07-22

- A última saída correta do grupo foi identificada como o dossiê técnico Bikon originalmente publicado na mensagem `657` do grupo.
- O PDF foi regenerado do mesmo HTML sem cabeçalho e rodapé automáticos do navegador, preservando três páginas A4 e o miolo textual.
- O envio corrigido e válido para o usuário é a mensagem `9396`.
- A identificação e o envio anteriores do EOL do 1º Ofício de Presidente Kennedy foram tratados como erro e não devem ser usados como referência desta entrega.
- Regra reforçada: antes de refazer a “última saída”, resolver a última mensagem com anexo no histórico real do grupo e validar identidade, data e arquivo antes da geração e do envio.

## Relações

- Agente Kowalski: `BRAIN/60-AGENTES/KOWALSKI.md`
- Escopo de canais operacionais: `BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md`
- Bikon: `BRAIN/20-EMPRESAS/BIKON/README.md`
