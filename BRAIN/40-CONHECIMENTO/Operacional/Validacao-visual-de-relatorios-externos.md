---
id: brain-452159666a22bea34c4e
type: knowledge
title: Validação visual de relatórios externos
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:50:50.519705Z'
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

## Complementos reconciliados — lote 4 de 2026-09-21

Um teste histórico encontrou a sequência UTC dentro de uma imagem codificada e gerou falso positivo de texto visível. Validar restrições editoriais na camada textual/renderizada pertinente; validação dos bytes/segredos e validação do conteúdo visível são controles distintos. Isso não dispensa inspeção visual nem permite ignorar um vazamento real. Fonte: unidades 32154.

No fluxo histórico ARX, o transporte foi condicionado à identidade do modelo aprovado e a regras de marca do produto. Um marcador no HTML pode detectar template errado, mas não comprova sozinho conteúdo, renderização, completude ou autorização de envio; esses gates precisam permanecer separados e ligados ao mesmo artefato. Fonte: unidades 36288, 31371.

No modelo diário ARX, a seção Seleção protegida foi removida quando não podia listar as pastas de modo explícito. Evitar cabeçalho que prometa escopo de proteção que a evidência não demonstra; métricas agregadas de seleção não provam caminhos de arquivos/pastas. Não inventar lista a partir da fonte de backup ou de contagens. Fonte: unidades 36575, 36359.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.

## Complementos reconciliados — lote 5 de 2026-09-21

Em 15/06/2026, Hebert descartou um layout anterior e aprovou um modelo próprio ARX Backup para relatórios daquela skill, com contato backup@arxcore.com.br e sem branding Cove/Bikon no documento externo. O pedido de report para cliente também retirava a seção de recomendações do modelo. Registrar identidade e estrutura como contrato histórico de apresentação, sem interpretar como autorização para omitir falhas, inventar sucesso ou alterar fontes técnicas internas; reutilização exige identificar a versão aprovada aplicável. Fonte: unidades 32110, 32119, 32143, 32146.

Em 02/07/2026, a organização proposta foi uma base padrao-relatorios-bikon no Kowalski, com regras especializadas apenas quando necessárias; o layout EOL aprovado foi ligado à base e a ninjaone-relatorios. A evidência histórica relata promoção do template, mas nome do arquivo, validade de PDF e HTML vizinho não substituem inspeção visual dos bytes atuais. Fonte: unidades 35671, 35683.

Na construção ARX de 16/06/2026, modelos diário e mensal foram tratados separadamente, com diretórios de modelos em validação e modelos aprovados. A promoção do diário foi relatada após revisão, mantendo referência própria. Ao reutilizar um template, identificar tipo, versão e aprovação aplicável; aprovação mensal não deve ser herdada automaticamente pelo diário. Fonte: unidades 36352, 36370.

Em 16/06/2026, Hebert confirmou validação dos PDFs de Catuaí e Grupo Unus após a correção de severidade e barra ARX de 28 dias. O aceite alcançava aqueles documentos apresentados; não autorizava reaproveitar barra hardcoded nem provar dados atuais. O registro complementa a correção causal dos campos da API descrita nas unidades36331/36340. Fonte: unidades 36343.

No relatório de acompanhamento ARX, Hebert pediu usar o nome público ARX Backup e retirar referências ao fornecedor Cove, reservando recomendações operacionais para a superfície adequada. O formato de acompanhamento não autoriza ocultar falhas, maquiar severidade ou omitir limitações de fonte; preservar evidência e distinguir relatório ao cliente de diagnóstico interno. Fonte: unidades 32111.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

A proposta histórica de consolidação documental separava geradores de negócio (boleto/NFS-e/ARX) de motores finais de PDF/DOCX/XLSX/imagem. Não apagar processo fiscal ao retirar conversor legado; PDF oficial de API permanece intocado. Migração exige mapa de dependências, fonte comum quando aplicável, regressão de layout/conteúdo/abertura e versão identificada. WeasyPrint69/python-docx/openpyxl/Pillow eram a proposta daquele contexto, não requisito universal nem prova de instalação vigente. Fonte: unidades 29565.

Manter um padrão editorial/visual Bikon comum e reservar skills específicas a coleta, regra técnica ou automação próprias. Variação de layout isolada não precisa criar outra skill; validação externa verifica autoria humana, marca correta e ausência de caminhos ou segredos. Fonte: unidades 35675.

No feed-base histórico, composição final 4:5 exigia elementos essenciais dentro da área segura de recorte da fonte 3:4; margem 80px de template quadrado não era transferível. Manter papéis e painéis abstratos/ilegíveis, sem dados reais, e owner presente como supervisor. Sem template aprovado, não inventar safe area em pixels. Fonte: unidades 39416.

Ao fechar um par de registros cujo segundo referencia o primeiro, congele primeiro os bytes do registro-base e faça o segundo referenciar seu hash; não exija hashes finais mutuamente embutidos, pois isso cria dependência circular. Validação independente deve conferir o par efetivamente gerado antes do freeze; o histórico não autoriza regenerar o par atual. Fonte: unidades 41669.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

Na peça histórica E2 sobre transferência de responsabilidade, melhorar estética não bastava: folio único, vão e gesto de entrega deveriam ser compreendidos em thumbnail com headline, sem legenda auxiliar. Reservar área tipográfica e testar o significado pretendido na escala de uso. Esse critério pertence à peça/briefing, sem tornar o objeto específico obrigatório em outras campanhas. Fonte: unidades 9646.

No desenho histórico de entrada única bikon-docs, documento nativo Google deveria usar exportação oficial da origem; documento local usaria motor local apropriado. Unificar interface não significa trocar o conteúdo por conversão menos fiel. O teste da rota Google estava bloqueado por dependência ausente e nenhuma alteração havia sido aplicada. Limites de formato/tamanho citados na época precisam ser revalidados; arquivo acima do limite não autoriza fallback improvisado ou apagar o gerador de negócio. Fonte: unidades 29566.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

No carrossel Provimento de 16/07, os três ajustes de wordmark, respiro do CTA e cor de SEGMENTAÇÃO foram relatados como aplicados antes de chegar novamente o veredito antigo “ajustar”. Timeout/killed da sessão revisora não valida nem reprova os novos PNGs. Vincular QA à versão/hash dos bytes efetivamente vistos e revalidar após reexportação; não repetir correções já presentes nem reutilizar parecer da versão anterior. Comparação posterior de Kling deveria preservar copy, identidade, composição local, custos, QA e autorização de publicação, sem inferir adoção a partir do estudo. Fonte: unidades 39624.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
