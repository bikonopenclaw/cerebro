# Sistema de marca e protocolo de Kowalski

## Fonte canônica

Kowalski detém o manual da marca e o brandpack. Esta skill não deve inventar, substituir ou manter uma cópia divergente dessas fontes.

Antes de produzir uma rota visual final, solicitar a Kowalski:

- versão do manual;
- versão, commit ou hash do brandpack;
- data da última revisão;
- validade do handoff;
- caminhos locais dos ativos aprovados;
- logo e usos proibidos;
- paleta e tokens;
- tipografia e licenças;
- estilo fotográfico e de vídeo;
- tratamento de produto, pessoas e ambientes;
- tom de voz e vocabulário;
- alegações permitidas e proibidas;
- avisos legais;
- política de IA, música, voz e direitos de imagem;
- restrições específicas da campanha.

## Handoff de marca

Registrar em `brand-handoff.yaml`:

```yaml
handoff_id: ""
source_agent: "Kowalski"
campaign_id: ""
manual_version: ""
brandpack_version: ""
brandpack_hash: ""
issued_at: null
valid_until: null
approved_assets: []
mandatory_rules: []
forbidden_rules: []
copy_tone: []
legal_requirements: []
open_questions: []
brand_lock: "pending"
```

Não copiar chaves, tokens ou ativos confidenciais para o handoff. Registrar caminhos controlados e hashes.

## Brand lock

Kowalski emite:

- `pass`: contexto suficiente e coerente para produzir;
- `fail`: conflito ou ausência de informação obrigatória;
- `conditional`: permitido somente com condições registradas.

`conditional` exige que cada condição apareça no briefing e no QA. Puppet Master bloqueia produção visual final quando o lock estiver ausente, vencido ou `fail`.

## Brand QA

No render final, Kowalski verifica:

- identidade do produto e embalagem;
- logo, respiro e contraste;
- paleta e tipografia;
- consistência de imagem e movimento;
- tom e vocabulário;
- claims, preços, datas e avisos;
- direitos e política de IA;
- coerência com a versão do brandpack usada.

Registrar `brand-qa: pass|fail` com observações e versão revisada.

## Governança

- Kowalski pode bloquear uma peça por não conformidade de marca.
- Kowalski não autoriza postagem ou envio externo.
- O proprietário pode pedir exceção; registrar a exceção e seu escopo.
- Métricas geram propostas separadas, nunca alteração automática do manual.
- Se o brandpack mudar durante a produção, criar nova versão do ativo e repetir brand lock e QA.
