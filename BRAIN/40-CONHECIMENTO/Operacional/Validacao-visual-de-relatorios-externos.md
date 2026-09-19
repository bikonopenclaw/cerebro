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

- `BRAIN/70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md`
- `BRAIN/60-AGENTES/KOWALSKI.md`
- `BRAIN/60-AGENTES/ROBOTNIK.md`
- `BRAIN/20-EMPRESAS/BIKON/README.md`
