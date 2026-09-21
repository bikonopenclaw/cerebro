---
id: brain-452159666a22bea34c4e
type: knowledge
title: Validação visual de relatórios externos
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T18:55:38.578515Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md#relações
- type: references
  target: BRAIN/60-AGENTES/KOWALSKI.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md#relações
- type: references
  target: BRAIN/60-AGENTES/ROBOTNIK.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md#relações
- type: references
  target: BRAIN/20-EMPRESAS/BIKON/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md#relações
---

# Validação visual de relatórios externos

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26; revisão visual Bikon em 2026-07-09; bloqueio de transporte em 2026-09-07; reparo causal Capixaba em 2026-09-18/19
confiabilidade: alta
ultima_revisao: 2026-09-19
tags: [relatorios, pdf, bikon, kowalski, robotnik, qualidade, identidade-visual, integridade, transporte]
```

## Princípio

Relatórios externos precisam ser tecnicamente auditáveis e visualmente profissionais. Conteúdo correto não basta quando o PDF parece HTML impresso, contém metadados de navegador, paginação ruim ou cabeçalhos/rodapés automáticos.

O mesmo princípio vale para materiais públicos ou semi-públicos da Bikon: post, carrossel, apresentação, proposta, landing page, template e qualquer peça com logo, paleta, layout ou identidade visual.

## Aplicação prática

- Renderizar e revisar visualmente antes de entregar PDF externo.
- Remover cabeçalhos, rodapés, caminhos internos, datas de navegador e paginação automática indesejada.
- Preservar identidade visual BIKON, acabamento corporativo e clareza de leitura.
- Em ajustes de design, alterar apenas o acabamento solicitado, preservando base técnica aprovada.
- Transformar padrões aprovados em template reutilizável quando houver recorrência.
- Para peças de marketing, Robotnik mantém pauta, copy e campanha; Kowalski atua como guardião visual antes da peça final quando houver logo, paleta, layout ou destino externo.
- A revisão visual deve ser curta e decisória: veredito, três ajustes prioritários e principal risco visual.
- Evitar estética hacker/cyberpunk, SaaS genérico, excesso de texto, promessa exagerada, medo barato e elementos que pareçam fora do padrão Bikon.
- Recorte visual preferido para Bikon: confiança operacional, clareza direta, hierarquia forte, paleta navy/ciano controlada e tipografia limpa.
- Revisao formal exige acesso aos mesmos bytes da versao apresentada. Caminho Markdown, hash declarado, screenshot parcial ou relato do produtor nao substitui abertura dos arquivos pelo revisor.
- Se a rota entre workspaces nao expuser o asset, fechar como `FAIL_CLOSED` e preservar o rascunho; nao aprovar por declaracao, trocar de rota por improviso, alterar o asset, fazer upload, agendar ou publicar.
- O contrato entre controller e veredito visual deve transportar referencias canonicas simples (`path` e `sha256`) separadas dos metadados de QA. Metadado que menciona um PDF nao e o proprio artefato e nao deve ser aceito como referencia visual.
- Transcript espelhado pode omitir chamadas nativas de imagem. Ausencia no espelho nao prova ausencia de inspecao; a validacao deve conferir rollout nativo, payloads de imagem, hashes e identidade do runtime vivo.
- Prova visual precisa ser executavel no momento do gate. Identificador publicado apenas depois do terminal nao pode ser exigido de uma sessao ainda viva sem uma regra autenticada equivalente.
- Recuperacao de QA visual exige causa precisa, contrato ou evidencia alterados e nova execucao limitada. Nao reutilizar inspecao antiga nem repetir o mesmo input depois do inicio de efeitos.

## Relações

- [[70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM|Relatórios Operacionais Telegram]]
- [[60-AGENTES/KOWALSKI|Kowalski]]
- [[60-AGENTES/ROBOTNIK|Robotnik]]
- [[20-EMPRESAS/BIKON/README|BIKON]]

## Identidade do cliente e nomenclatura pública — caso de 2026-07-08

O resumo histórico dos relatórios EOL de Rio Novo do Sul e Presidente Kennedy registra um PDF por cliente, estrutura de referência João Neiva e identidade Corpus quando solicitada. Registra também a decisão de apresentar `BikonRMM` no lugar de `NinjaOne` em conteúdo visível ao destinatário, inclusive na indicação de fonte.

O escopo de padronização Corpus/modelo João Neiva listado nessa fonte foi: cadastros 2000, 2002, 2004, 2005, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019 e 2020. A identidade específica aprovada para cliente ou produto deve ser conciliada com o padrão corporativo, não substituída indiscriminadamente pela marca Bikon. Nomenclatura pública não implica renomear identificadores internos, integrações ou a evidência técnica de origem.

A fonte relata alteração de skill e entrega de PDFs; esta revisão preserva a decisão e seu escopo, sem atestar a implantação atual nem a disponibilidade desses artefatos. Para reutilização, conferir o contrato visual vigente e eventual decisão posterior. Os caminhos temporários de geração e os estados de progresso do episódio não são requisitos permanentes.

Fonte: unidade 41674, SHA-256 `75707d3e8b1fdab384841d1350d0b24a4499ce5f0615a0fed7ebc2847300f864`, recuperada de resumo de compactação em três cópias de índice de sessões; recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-metadata-20260921.json`.

## Conhecimento recuperado dos históricos — revisão 2026-09-21

No caso histórico do relatório ARX de 15/06/2026, Hebert pediu apresentar os horários em GMT-3. O template deve declarar o fuso usado e converter timestamps de forma consistente com o contrato aprovado do relatório; não basta renomear o rótulo de UTC. A preferência daquele documento não altera automaticamente todos os agendamentos da plataforma. Fonte: unidades 32113, 32114.

Caso histórico de 01/07/2026: o usuário detectou computadores repetidos e pediu condensação no relatório. A montagem deve reconciliar múltiplas ocorrências do mesmo ativo por identidade estável antes de apresentar inventário e contagens, preservando os eventos distintos necessários à análise. Sem identidade suficiente, declarar ambiguidade em vez de fundir por nome. Isso evita transformar duplicação de apresentação em duplicação da população. Fonte: unidades 29089.

No episódio do relatório de João Neiva solicitado no modelo Ferreira Rocha, a marca foi corrigida para ARX Backup. Este caso sustenta conferir identidade do produto/cliente antes da entrega, sem inferir aprovação de conteúdo ou envio pela frase de correção. Fonte: unidades 37928.

Caso histórico de relatório mensal ARX/Stcoop: a legenda/barra estava fixa em verde apesar de dado crítico. A apresentação de severidade deve derivar da evidência da fonte e do período correspondente, nunca de cor hardcoded. No diagnóstico histórico foram citados campos TB/FB/SB/QB/HB/WB e 28 dias; esses detalhes não comprovam o schema atual do provider nem permitem substituir o contrato vigente de coleta/render. Fonte: unidades 36332.

Na mesma revisão histórica de ARX Backup, o contato indicado para a identidade do serviço foi backup@arxcore.com.br. Registrar como escolha histórica de contato público, restrita a ARX; reconfirmar antes de adotá-la em template atual, sem alterar destinatários/remetentes de automações. Fonte: unidades 32141.

Caso histórico ARX Backup: Hebert determinou identidade própria nos materiais ARX, retirando logo, assinatura e referências Bikon. A identidade do serviço/cliente aprovada deve prevalecer sobre o template corporativo genérico; validar contrato visual vigente antes de reutilizar. Fonte: unidades 32135.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.
