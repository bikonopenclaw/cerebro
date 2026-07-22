# Papéis e limites das ferramentas

## Princípio

Atribuir um único responsável por cada decisão e um único executor por cada mutação. A pilha padrão deve funcionar sem assinaturas SaaS obrigatórias.

| Papel | Responsável | Limite |
|---|---|---|
| Orquestração | Puppet Master + OpenClaw | Não publicar nem substituir especialistas |
| Marketing e Instagram | Robotnik | Não aprovar a própria ação externa |
| Marca e brandpack | Kowalski | Não decidir estratégia nem publicar |
| Aprovação externa | Proprietário | Autoridade humana exclusiva |
| Pesquisa | Robotnik + Web Search/SearXNG | Consultas não públicas exigem OK |
| Estratégia e copy | Robotnik + playbook interno; BlackTwist opcional | Não publicar ou agendar |
| Direção criativa | Robotnik com restrições de Kowalski | Não consumir créditos sem OK |
| Geração de imagem e vídeo | Kling CLI | Não compor texto final nem publicar |
| Animação programática | Motion Canvas local | Não decidir estratégia |
| Composição e codificação | FFmpeg, ImageMagick e SVG | Não improvisar direção não aprovada |
| Masters manuais | Brandpack; Penpot auto-hospedado opcional | Não ser arquivo único dos brutos |
| Voz | Kokoro/Piper local ou locução humana | Não clonar voz sem direitos |
| QA técnico | FFmpeg/ffprobe + ImageMagick | Não aprovar marca ou jurídico |
| QA de marca | Kowalski | Não substituir o proprietário |
| Automação | n8n auto-hospedado, opcional | Executar somente ações já autorizadas |
| Estado | Manifesto + SQLite/Data Tables locais | Não guardar segredos |
| Arquivo | Filesystem local; MinIO auto-hospedado opcional | Não fazer upload externo sem OK |
| Publicação | Robotnik via Instagram Graph API ou handoff manual | Exigir Portão X |
| Métricas | Robotnik | Não reescrever a marca automaticamente |

## Pilha essencial

1. OpenClaw;
2. Puppet Master, Robotnik e Kowalski;
3. playbook editorial interno;
4. Kling CLI quando houver geração aprovada;
5. Motion Canvas, FFmpeg, ImageMagick e SVG;
6. brandpack de Kowalski;
7. Instagram Graph API ou finalização manual;
8. OK explícito do proprietário.

## Dependências opcionais

- BlackTwist para módulos editoriais e analíticos;
- Penpot auto-hospedado para masters e revisão;
- Kokoro ou Piper local para TTS;
- n8n auto-hospedado para execução determinística;
- MinIO auto-hospedado para armazenamento de objetos;
- SearXNG auto-hospedado para pesquisa.

Ausência de um componente opcional não autoriza trocar silenciosamente por um serviço pago.

## Separação de credenciais

- Puppet Master mantém estado e approvals, preferencialmente sem token de publicação.
- Robotnik ou executor restrito recebe somente credenciais necessárias à publicação.
- Kowalski não recebe credenciais de geração ou publicação.
- Kling e Instagram usam credenciais distintas.
- Segredos ficam em secret store ou variáveis de ambiente, nunca na skill.

## Evitar sobreposição

- Não permitir que BlackTwist publique ou agende.
- Não usar n8n como agente criativo.
- Não disponibilizar token de publicação a mais de um executor quando isso puder ser evitado.
- Não usar URLs temporárias como arquivo canônico.
- Não usar Penpot como armazenamento único dos brutos.
- Não executar geração ou publicação por dois caminhos em paralelo.
- Não habilitar fallback externo automático.

## Modelos do agente

Manter modelos e fallbacks fora desta skill. Usar somente modelos registrados no provedor do OpenClaw e validar permissões, custo e privacidade antes de enviar dados.


## Provider Layer 2.1

Ferramentas externas deixam de ser selecionadas diretamente. A operação declara kind e provider ID, e o registro decide se existe adapter habilitado. Image, Video, TTS, Storage, Publication e Search são categorias. O registro nasce deny by default.

Skipper, Rico e Private não são executores de provider.
