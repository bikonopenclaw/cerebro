---
name: "robotnik-image-cost-routing"
description: "Robotnik roteia imagem e custo Bikon"
---

# Robotnik Image Cost Routing

## Objetivo

Roteia a geracao visual Bikon para o agente certo, usando a ferramenta ja paga/disponivel antes de qualquer alternativa com custo adicional.

Esta skill nao e a fonte canonica do padrao visual Bikon. Para padrao visual, usar:

`/data/.openclaw/workspace/skills/bikon-social-visual-hard-blocks/SKILL.md`

## Responsabilidade operacional

- Robotnik e o executor principal de conteudo, imagens, posts, carrosseis, captions, campanhas, e-mail marketing e criativo.
- Puppet Master atua como CEO/orquestrador: define criterio, cobra, revisa e bloqueia qualidade ruim.
- Kowalski atua como gate de consistencia visual Bikon quando a entrega envolver documento, relatorio, PDF, apresentacao ou material que precise padrao visual formal.

## Regra de custo

1. Antes de propor ferramenta paga adicional, verificar provider/modelo habilitado, plano ativo e ferramenta ja contratada.
2. Priorizar a ferramenta de imagem ja paga/disponivel pelo Hebert.
3. So propor custo adicional se a ferramenta atual falhar tecnicamente ou nao atingir qualidade minima.
4. Qualquer gasto acima de R$ 1 exige aprovacao explicita do Hebert.
5. Nao esconder custo em teste, geracao, assinatura, credito, API ou provider alternativo.

## Regra visual obrigatoria

Antes de qualquer imagem Bikon, Robotnik deve ler e seguir a skill canonica:

`/data/.openclaw/workspace/skills/bikon-social-visual-hard-blocks/SKILL.md`

Ela contem as regras ativas para:

- logo oficial Bikon;
- tema escuro;
- modelo premium aprovado;
- formato 4:5 / 1080x1350;
- imagens/fundos realistas;
- bloqueio de visual infantil, Canva generico, Paint, logo inventada e tema claro;
- criterios de aprovacao antes de enviar ao Hebert.

Se houver conflito entre esta skill e `bikon-social-visual-hard-blocks`, a skill canonica visual vence.

## Processo operacional

1. Receber tema, objetivo comercial, canal e publico alvo.
2. Confirmar se a entrega e rascunho interno, proposta para Hebert ou publicacao externa.
3. Acionar `bikon-social-visual-hard-blocks` antes de briefing visual, geracao ou revisao.
4. Definir copy e roteiro visual por slide ou peca.
5. Escolher ferramenta ja paga/disponivel.
6. Gerar imagens ou orientar geracao somente dentro do padrao visual canonico.
7. Aplicar asset oficial da logo Bikon quando a peca exigir marca.
8. Validar qualidade, leitura, tema escuro, logo correta e ausencia de visual amador.
9. Quando houver documento, relatorio, PDF ou apresentacao, chamar Kowalski para gate visual Bikon.
10. Entregar para Puppet Master revisar antes de mostrar ao Hebert.

## Bloqueios

Nao enviar para Hebert, publicar ou encaminhar como pronto se houver:

- logo errada, recriada, aproximada ou gerada por IA;
- tema claro em carrossel tecnico Bikon sem aprovacao explicita;
- visual infantil, Paint, Canva generico, desenho amador ou IA barata;
- imagem aleatoria que nao explica o assunto;
- excesso de texto ou baixa leitura no celular;
- dependencia de ferramenta nova paga sem aprovacao;
- publicacao real em canal publico sem aprovacao do Hebert;
- uso de rosto, preco, verba, canal publico ou base de contatos sem aprovacao.

## Saida esperada

Para Puppet Master ou Hebert, entregar curto:

1. Peca/canal.
2. Ferramenta usada ou recomendada.
3. Custo: `sem custo adicional`, `custo bloqueado` ou `precisa aprovacao`.
4. Status visual: `pronto para revisao`, `ajustar` ou `bloqueado`.
5. Proximo passo.

## Funcionalidade preservada

Ficam preservadas as regras aprovadas em 2026-07-10:

- geracao visual deve ser delegada a Robotnik/Kowalski quando aplicavel;
- Puppet Master nao deve virar operador manual de imagem;
- usar ferramenta ja paga antes de sugerir custo;
- nao recriar logo;
- bloquear tema claro, visual infantil/amador e imagem aleatoria;
- permitir imagens/fundos criados ou compostos quando enriquecerem o assunto e parecerem profissionais;
- exigir validacao de qualidade antes de enviar ao Hebert.
