# Papéis e limites das ferramentas

## Princípio

Atribuir um único responsável por cada ação que altera estado. Permitir colaboração na análise, mas impedir sobreposição em geração paga, composição e publicação.

| Papel | Responsável | Limite |
|---|---|---|
| Entrada e aprovações | Telegram + OpenClaw | Não publicar pelo chat sem passar pelos portões |
| Orquestração | OpenClaw + `instagram-brand-director` | Não substituir ferramentas especializadas |
| Pesquisa | Web Search do OpenClaw; Exa preferencial | Não copiar concorrentes nem tratar tendência como fato |
| Extração de páginas | Firecrawl, quando necessário | Não usar se a busca já fornecer evidência suficiente |
| Estratégia e copy | BlackTwist + sistema editorial | Não publicar ou agendar |
| Direção criativa | Esta skill + sistema de marca | Não consumir créditos |
| Geração de mídia | Kling CLI | Não compor texto final nem publicar |
| Composição automatizada | Creatomate | Não decidir estratégia |
| Masters editáveis | Figma | Não ser o renderizador em lote |
| Voz e dublagem | ElevenLabs, opcional | Não clonar voz sem autorização e direitos |
| QA técnico | FFmpeg/ffprobe + ImageMagick | Não aprovar marca ou jurídico |
| QA semântico | Modelo com visão | Não substituir aprovação humana |
| Automação | n8n, opcional | Não tomar decisões criativas |
| Estado operacional | campaign.json + events.jsonl append-only | Não guardar segredos |
| Arquivo de mídia | Cloudflare R2, opcional | Não tornar bucket público por padrão |
| Rascunho/agendamento/publicação | Buffer | Ser o único escritor do estado de publicação |
| Métricas | Buffer + analisadores BlackTwist | Não reescrever a marca automaticamente |
| Auditor independente | Hermes, opcional | Não operar o mesmo bot ou credenciais de publicação |
| Aprovação final | Pessoa autorizada | Ser indispensável para publicação |

## Pilha essencial

Usar como base:

1. OpenClaw;
2. BlackTwist ou playbook editorial interno;
3. Kling CLI;
4. Creatomate;
5. Figma;
6. Buffer;
7. aprovação humana.

Adicionar n8n e R2 quando houver volume, integrações ou necessidade de auditoria operacional. Adicionar ElevenLabs somente quando a produção exigir voz.

## Evitar sobreposição

- Desabilitar ou não invocar publicação e agendamento do BlackTwist.
- Não chamar Instagram diretamente se o Buffer for o sistema escolhido.
- Não usar Canva ou CapCut como uma terceira fonte automática de layout.
- Usar DaVinci Resolve ou outro editor manual apenas para peças especiais, fora do fluxo em lote.
- Não usar n8n como agente criativo.
- Não implementar retries paralelos. O executor aprovado é o único responsável por retries seguros e idempotentes.
- Não usar Figma como armazenamento canônico dos brutos.
- Não depender de URLs temporárias de provedores; arquivar a mídia em armazenamento controlado.

## OpenClaw e Hermes

Manter um único orquestrador de produção.

Usar OpenClaw em produção porque controla o Telegram, a sessão da campanha e os portões. Usar Hermes, se desejado, como:

- revisor crítico;
- segunda leitura de copy;
- teste adversarial de briefing;
- avaliação de coerência entre marca e peça;
- laboratório da skill sem credenciais de produção.

Não conectar os dois ao mesmo token de bot em modo polling. Não disponibilizar ao Hermes as credenciais do Buffer ou da Kling quando sua função for somente auditoria.

## Modelos do agente

Manter modelos e fallbacks fora desta skill. Usar somente modelos registrados no provedor do OpenClaw e validar o fallback antes de depender dele.

Não escrever IDs de modelo do agente no `SKILL.md`; a configuração do gateway é a fonte canônica.
