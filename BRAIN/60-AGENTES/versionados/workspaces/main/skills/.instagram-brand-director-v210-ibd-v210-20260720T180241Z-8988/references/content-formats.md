# Formatos de conteúdo

Validar requisitos atuais do Instagram e da Instagram Graph API antes da exportação ou publicação. Usar os valores abaixo como defaults de produção, não como substitutos da validação atual.

## Feed 4:5

- Trabalhar em 1080 × 1350.
- Comunicar uma mensagem central.
- Manter um foco visual.
- Aplicar hook no compositor local.
- Gerar a cena sem parágrafos, logo ou texto legal dentro da mídia generativa.
- Preparar legenda, CTA e alt text.

## Feed 1:1

- Trabalhar em 1080 × 1080 somente quando a campanha justificar.
- Preservar área segura e legibilidade em telas menores.

## Carrossel

Manter todos os slides na mesma proporção. Usar como ponto de partida:

1. capa com hook;
2. contexto ou tensão;
3. desenvolvimento;
4. evidência ou exemplo;
5. síntese;
6. CTA.

Variar a quantidade conforme a narrativa. Não alongar artificialmente.

Gerar imagens-base ou série visual na Kling quando aprovado. Aplicar texto, paginação e consistência em SVG/ImageMagick ou Motion Canvas.

## Reel 9:16

- Trabalhar em 1080 × 1920.
- Definir hook inicial, duração, shot list, ritmo, movimento, áudio, texto em tela, CTA e thumbnail.
- Manter elementos importantes nas safe areas do template aprovado por Kowalski.
- Preferir:

```text
keyframe aprovado → Kling image_to_video → composição local → áudio → legendas
```

- Usar `text_to_video` quando a exploração tiver sido aprovada ou não houver keyframe apropriado.
- Kling também pode criar o vídeo completo quando o roteiro, parâmetros e custo forem aprovados.

## Stories 9:16

- Trabalhar em 1080 × 1920.
- Usar uma função por tela: contexto, interação, prova ou CTA.
- Reservar espaço para elementos nativos.
- Finalizar manualmente quando a peça exigir enquete, link, música ou sticker não suportado pela API.

## Série

Definir antes de gerar:

- regra de continuidade;
- personagens;
- produto;
- paleta;
- câmera;
- luz;
- materiais;
- elementos fixos;
- variações permitidas.

Registrar keyframe mestre, referências, versão do brandpack e aprovação de cada ativo.
