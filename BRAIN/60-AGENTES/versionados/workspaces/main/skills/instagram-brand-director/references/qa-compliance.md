# QA e compliance

Bloquear a publicação até concluir todos os itens aplicáveis.

## QA técnico

Quando disponíveis, usar:

```bash
ffprobe -v error -show_format -show_streams -of json <video>
magick identify -verbose <imagem>
```

Verificar:

- dimensões;
- proporção;
- duração;
- codec;
- frame rate;
- presença de áudio;
- tamanho;
- integridade;
- orientação;
- perfil de cor quando relevante.

Não considerar uma peça aprovada apenas porque o arquivo abre.

## Estratégia

- [ ] Objetivo e KPI definidos.
- [ ] Pilar e funil claros.
- [ ] Hook corresponde à promessa.
- [ ] CTA é coerente.
- [ ] Fontes sustentam as alegações.

## Marca

- [ ] Produto e embalagem correspondem às referências.
- [ ] Logo, paleta e tipografia estão corretos.
- [ ] Não existem marcas, símbolos ou textos inventados.
- [ ] Tom alinhado à empresa.
- [ ] Uso de ativos respeita o sistema de marca.

## Visual

- [ ] Sem deformações, duplicações ou flicker.
- [ ] Mãos, rostos, reflexos e objetos coerentes.
- [ ] Movimento, gravidade e interações naturais.
- [ ] Continuidade preservada.
- [ ] Texto e CTA dentro das safe areas.
- [ ] Thumbnail representa a peça.

Usar modelo com visão como revisor auxiliar. Exigir revisão humana para marca e peças de maior risco.

## Texto

- [ ] Ortografia e gramática revisadas.
- [ ] Nomes, preços, datas e condições corretos.
- [ ] Legenda entrega a promessa.
- [ ] Texto em tela legível.
- [ ] CTA corresponde ao destino.
- [ ] Alt text preparado.

## Áudio

- [ ] Voz autorizada.
- [ ] Música licenciada.
- [ ] Locução inteligível.
- [ ] Sem clipping.
- [ ] Legendas sincronizadas.
- [ ] Origens registradas.

## Legal e privacidade

- [ ] Alegações possuem evidência.
- [ ] Avisos obrigatórios presentes.
- [ ] Direitos de pessoas, vozes, músicas e marcas confirmados.
- [ ] Sem dados pessoais ou confidenciais.
- [ ] Conteúdo respeita regras do setor.
- [ ] Uso de IA atende à política da empresa.

Encaminhar ao jurídico quando o risco não puder ser resolvido por checklist.

## Acessibilidade

- [ ] Contraste adequado.
- [ ] Tamanho de texto adequado.
- [ ] Mensagem compreensível sem áudio quando necessário.
- [ ] Legendas incluídas.
- [ ] Alt text revisado.

## Decisão

Registrar:

- `pass`;
- `fail`;
- `waived` com aprovador e justificativa;
- itens não aplicáveis.

Não converter `fail` em `pass` automaticamente. Retornar ao estágio responsável.
