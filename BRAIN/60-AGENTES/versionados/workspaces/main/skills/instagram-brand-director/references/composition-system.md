# Sistema de composição

Tratar saída Kling como bruto. Texto, logo, preço, CTA, legal e legendas entram no compositor.

## Creatomate

Usar somente `templates/template-map.yaml` com `production_enabled: true`, template_id real, versão, dimensões, campos, tipos, limites, safe areas, fontes, cores e assets.

Validar modifications. Rejeitar campo, fonte, template ou asset desconhecido. Fixar template e versão no request_hash. Arquivar render e manifesto de composição.

## Figma

Fonte de masters, componentes e revisão. Não é armazenamento dos brutos nem renderizador de lote.

Sem template real aprovado, marcar composição `blocked`. Não acionar handoff manual automaticamente.