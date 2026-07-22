# Sistema de composição local

## Princípio

Transformar ativos brutos em peças determinísticas, reproduzíveis e alinhadas ao brandpack, sem depender de assinatura de composição.

## Arquitetura

Usar três camadas:

1. **Motion Canvas local** para animações, cenas, transições e layouts programáticos;
2. **SVG + ImageMagick** para peças estáticas, carrosséis, capas e thumbnails;
3. **FFmpeg** para codificação, concatenação, crop, áudio, legendas e overlays.

Manter templates em repositório versionado. Cada layout aprovado deve possuir:

- `template_id`;
- versão ou commit;
- schema de propriedades;
- dimensões;
- safe areas;
- fontes e licenças;
- saída esperada;
- responsável pela aprovação visual.

## Contrato de propriedades

Exemplo:

```json
{
  "campaignId": "campanha-001",
  "assetId": "reel-01",
  "version": 1,
  "headline": "Texto aprovado",
  "body": "Texto aprovado",
  "cta": "Saiba mais",
  "logoSrc": "assets/brand/logo.svg",
  "backgroundSrc": "generated/background.mp4",
  "subtitleSrc": "audio/subtitles.srt",
  "legal": "",
  "pageNumber": 1,
  "brandpackHash": "sha256:..."
}
```

Validar propriedades antes de renderizar. Escapar texto e não interpolar entrada não confiável diretamente em shell, SVG ou filtros FFmpeg.

## Motion Canvas

Usar para:

- animação de tipografia;
- keyframes de layout;
- transições;
- motion graphics;
- sincronização com áudio;
- composição de cenas;
- exportação de frames para codificação.

O repositório de composição deve expor um script controlado, por exemplo `render:asset`, que recebe um manifesto validado. Não inventar flags de CLI nem executar comando construído a partir de texto livre.

Fixar versões de dependências e revisar licença antes de atualizações de produção.

## SVG e ImageMagick

Usar para:

- feed;
- carrossel;
- thumbnail;
- capa;
- rodapé;
- paginação;
- aplicações de logo e CTA.

Manter templates SVG sem scripts externos. Converter para PNG/JPEG somente depois de validar fontes, medidas, contraste e conteúdo.

## FFmpeg

Usar para:

- redimensionamento e crop;
- concatenação de cenas;
- áudio e mixagem;
- legendas;
- overlays;
- geração de thumbnail;
- codec e container final;
- QA técnico com ffprobe.

Não usar filtergraph improvisado para substituir direção visual não aprovada.

## Masters e Penpot

O brandpack de Kowalski é a fonte canônica. Penpot auto-hospedado pode ser usado para:

- masters;
- componentes;
- tokens;
- safe areas;
- revisão humana;
- handoff.

Exportar templates aprovados para o repositório local. Não depender da API do editor para renderização em lote.

## Render

Antes do render:

1. validar schema;
2. confirmar caminhos dos ativos;
3. verificar hash do brandpack;
4. carregar somente fontes licenciadas;
5. verificar duração, FPS, resolução e codec;
6. gerar preview;
7. registrar comando controlado, commit e hash das propriedades.

## Fallback

Se Motion Canvas estiver indisponível:

- usar SVG/ImageMagick para estáticos;
- usar FFmpeg apenas para composição simples já especificada;
- ou gerar handoff manual.

Registrar `composition_mode: motion-canvas|svg-imagemagick|ffmpeg-fallback|manual` e submeter ao mesmo QA.

## Saídas

Separar:

```text
generated/          → ativos brutos
renders/            → peças compostas
release-candidate/  → versão pronta para Portão X
```

Não sobrescrever bruto. Registrar:

- template ID;
- commit;
- hash das propriedades;
- duração;
- FPS;
- resolução;
- codec;
- caminho de saída;
- versão do brandpack.
