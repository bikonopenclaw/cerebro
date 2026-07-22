# QA, compliance e integridade da aprovação

Bloquear o release candidate até concluir todos os itens aplicáveis.

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

## Estratégia e texto — Robotnik

- [ ] Objetivo e KPI definidos.
- [ ] Pilar e funil claros.
- [ ] Hook corresponde à promessa.
- [ ] CTA é coerente.
- [ ] Fontes sustentam as alegações.
- [ ] Ortografia e gramática revisadas.
- [ ] Nomes, preços, datas e condições corretos.
- [ ] Alt text preparado.

## Marca — Kowalski

- [ ] Manual e brandpack vigentes registrados.
- [ ] Produto e embalagem correspondem às referências.
- [ ] Logo, paleta e tipografia estão corretos.
- [ ] Não existem marcas, símbolos ou textos inventados.
- [ ] Tom alinhado à empresa.
- [ ] Claims e avisos respeitam o manual.
- [ ] `brand-qa` registrado para a versão final.

## Visual

- [ ] Sem deformações, duplicações ou flicker.
- [ ] Mãos, rostos, reflexos e objetos coerentes.
- [ ] Movimento, gravidade e interações naturais.
- [ ] Continuidade preservada.
- [ ] Texto e CTA dentro das safe areas.
- [ ] Thumbnail representa a peça.

Usar modelo com visão como revisor auxiliar. Não substituir Kowalski ou o proprietário.

## Áudio

- [ ] Voz autorizada.
- [ ] Música licenciada.
- [ ] Locução inteligível.
- [ ] Sem clipping.
- [ ] Legendas sincronizadas.
- [ ] Origens e licenças registradas.

## Legal e privacidade

- [ ] Alegações possuem evidência.
- [ ] Avisos obrigatórios presentes.
- [ ] Direitos de pessoas, vozes, músicas e marcas confirmados.
- [ ] Sem dados pessoais ou confidenciais indevidos.
- [ ] Conteúdo respeita regras do setor.
- [ ] Uso de IA atende à política da empresa.
- [ ] Dados enviados externamente foram minimizados e aprovados.

Encaminhar ao jurídico quando o risco não puder ser resolvido por checklist.

## Acessibilidade

- [ ] Contraste adequado.
- [ ] Tamanho de texto adequado.
- [ ] Mensagem compreensível sem áudio quando necessário.
- [ ] Legendas incluídas.
- [ ] Alt text revisado.

## Integridade do Portão X

Antes de qualquer mutação externa:

- [ ] Campaign ID, asset ID e versão coincidem.
- [ ] Payload hash coincide.
- [ ] Ação e destino coincidem.
- [ ] Horário e fuso coincidem.
- [ ] Approval ID pertence ao proprietário.
- [ ] Autorização não foi revogada ou consumida.
- [ ] Nenhuma alteração ocorreu depois do OK.

Esse bloco não pode ser dispensado por `waiver` de agente.

## Decisão

Registrar:

- `pass`;
- `fail`;
- `conditional` com condições;
- `not-applicable`.

Somente o proprietário pode aceitar risco residual que implique ação externa. Não converter `fail` em `pass` automaticamente.


---

## Playbook consolidado: compliance

Conteúdo incorporado integralmente do playbook autônomo da candidata de 66 arquivos:

# Playbook: compliance

1. Verificar claims, fonte e data.
2. Verificar direitos de imagem, voz, música, marca e referência.
3. Minimizar dados pessoais e confidenciais.
4. Verificar avisos setoriais e política de IA.
5. Private pode apontar risco quando habilitado.
6. Risco jurídico ou regulatório não resolvido vai para especialista humano.
7. Somente o proprietário aceita risco residual ligado a ação externa.
