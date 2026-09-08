---
name: "bikon-visual-review"
description: "Gate visual Bikon para revisar entregas"
---

# Bikon Visual Review

## Objetivo

Revisar pecas visuais da Bikon antes de chegarem ao Hebert ou irem para canal externo.

Esta skill nao define direção criativa. Para marketing Bikon, ler integralmente o contrato e abrir a referência vinculados em `/data/.openclaw/workspace-robotnik/skills/content-production-contract/SKILL.md`. Para relatórios, documentos administrativos e cadeias ARX, preservar a autoridade documental própria do Kowalski em `/data/.openclaw/workspace-kowalski/skills/padrao-relatorios-bikon/SKILL.md` e seus modelos aprovados. Os critérios documentais abaixo não substituem a direção fotográfica do marketing.

A funcao desta skill e dar veredito, apontar risco visual e travar entrega que pareca generica, amadora ou desalinhada com a Bikon.

## Quando Usar

Use para revisar:

- carrossel;
- post estatico;
- thumbnail;
- relatorio visual;
- PDF executivo;
- apresentacao;
- landing page;
- proposta comercial visual;
- material criado por Robotnik;
- documento criado por Kowalski com padrao Bikon.

Nao use para:

- texto puro sem arte;
- diagnostico tecnico sem entrega visual;
- codigo backend;
- comunicacao urgente onde o conteudo operacional importa mais que acabamento visual.

## Fluxo Obrigatorio

1. Identificar canal, publico, objetivo e status da peca.
2. Carregar a autoridade correspondente ao domínio: contrato criativo para marketing; contrato documental do Kowalski para relatórios.
3. Se for documento, relatorio, PDF ou apresentacao, exigir consistencia de Kowalski antes do envio ao Hebert.
4. Revisar reputacao, legibilidade, logo, tema, imagem, hierarquia, CTA e risco comercial.
5. Entregar veredito curto para Puppet Master.
6. Nao publicar, enviar a cliente ou disparar canal publico sem aprovacao explicita do Hebert.

## Posicao no Fluxo

1. Robotnik cria pauta, copy, roteiro, campanha ou arte.
2. Kowalski revisa formalmente toda arte Bikon, inclusive posts; relatórios conservam seu fluxo documental.
3. Bikon Visual Review faz o gate visual.
4. Para marketing, Robotnik entrega diretamente a Hebert após revisão formal; Puppet mantém coordenação quando necessária. O fluxo documental próprio permanece.
5. Hebert aprova, pede ajuste ou reprova quando houver publicacao, envio externo ou decisao sensivel.

## Criterios de Revisao

Responder objetivamente:

- A peca parece Bikon ou parece template generico?
- Está aderente à referência canônica de marketing ou ao modelo documental aprovado, conforme o domínio?
- A logo oficial esta correta e veio de asset oficial?
- O tema escuro foi respeitado quando for carrossel ou post tecnico?
- A imagem ou fundo enriquece o assunto?
- O texto e legivel em celular em 3 segundos?
- Ha uma ideia por slide, pagina ou bloco?
- O ciano destaca algo util ou virou enfeite?
- Existe risco de parecer amador, infantil, Canva, Paint, IA barata ou banco de imagem ruim?
- O CTA e claro, sobrio e compativel com a Bikon?

## Bloqueios documentais; para marketing aplicar todos os critérios do contrato criativo

Reprovar ou pedir refacao se houver:

- logo errada, recriada, aproximada ou gerada por IA;
- tema claro em carrossel tecnico sem aprovacao explicita;
- visual infantil, cartoon, Paint, Canva generico ou IA barata;
- estetica hacker, Matrix, cyberpunk ou medo barato;
- imagem aleatoria sem relacao operacional;
- texto espremido, fonte pequena ou baixa leitura;
- excesso de copy por slide;
- card dentro de card sem necessidade;
- promessa absoluta, como `seguranca garantida`;
- material publico ou externo sem aprovacao explicita do Hebert.

## Saida Esperada

Ao revisar, entregar no maximo:

```text
Veredito: aprovado | ajustar | reprovar
Risco principal: {{risco}}
Ajustes prioritarios:
1. {{ajuste}}
2. {{ajuste}}
3. {{ajuste}}
Proximo passo: {{acao}}
```

Se estiver aprovado, ainda informar se precisa aprovacao do Hebert antes de publicar, enviar para cliente ou disparar em canal externo.

## Travas

- Nao virar segunda fonte de identidade visual.
- Nao contradizer a autoridade canônica aplicável ao domínio.
- Nao publicar nada.
- Nao enviar para cliente.
- Nao suavizar problema visual grave para acelerar entrega.
- Se houver duvida entre aprovar e ajustar, ajustar.

## Regra Final

Esta skill existe para reduzir erro de gosto e proteger reputacao. Marketing usa somente o contrato criativo do Robotnik. Documentos mantêm sua autoridade no Kowalski. Para marketing, o revisor precisa abrir piloto e referência reais, inspecionar resolução integral e prévia reduzida, registrar hashes, anatomia, cena, overlays, logo e correspondência da legenda. Acesso negado bloqueia revisão; jamais inventar aprovação ou inspeção em celular físico.
