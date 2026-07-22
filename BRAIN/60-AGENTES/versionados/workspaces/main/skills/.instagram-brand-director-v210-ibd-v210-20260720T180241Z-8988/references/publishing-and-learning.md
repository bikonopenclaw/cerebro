# Publicação e aprendizado

## Responsabilidade

Robotnik prepara e executa a operação do Instagram. Puppet Master controla o Portão X. Kowalski garante conformidade de marca. O proprietário é a única autoridade de publicação.

## Sistema de publicação

Usar:

1. pacote local de release candidate;
2. Instagram Graph API oficial, quando configurada e suportada;
3. finalização manual no aplicativo pelo proprietário quando houver recurso nativo não coberto pela API.

Não criar rascunho remoto, container de mídia, upload ou agendamento antes do OK específico, pois essas ações já transmitem conteúdo para fora do ambiente.

## Pacote local

Incluir:

- canal;
- formato;
- mídia;
- thumbnail;
- legenda;
- CTA;
- hashtags;
- alt text;
- primeiro comentário, quando aplicável;
- data e horário;
- fuso;
- modo de ação;
- campanha;
- ativo;
- versão;
- payload hash;
- brandpack hash;
- brand QA;
- custo residual;
- destino.

## Modos autorizáveis

- `publish_now`: publicar imediatamente a versão apresentada.
- `schedule_and_publish`: criar automação para publicar a versão apresentada na data e fuso exatos.
- `manual_handoff`: entregar o pacote ao proprietário para finalização manual.
- `edit_remote`: editar somente campos especificados.
- `delete_remote`: excluir somente o post identificado.

Não inferir um modo a partir de outro.

## Fluxo

1. Robotnik prepara o pacote local.
2. Kowalski registra `brand-qa: pass`.
3. Puppet Master apresenta preview, copy, destino, modo e horário.
4. Proprietário envia o OK explícito.
5. Registrar approval ID e payload hash.
6. Robotnik ou executor restrito executa uma vez.
7. Registrar IDs remotos, resposta e horário.
8. Marcar aprovação como consumida.
9. Em resultado incerto, consultar o post ou container antes de qualquer nova mutação.

## API

Antes da execução, verificar documentação oficial atual para:

- tipo de conta;
- permissões;
- mídia suportada;
- limites;
- requisitos de container;
- status de processamento;
- publicação e métricas.

Não fixar versão de endpoint nesta skill. Manter tokens fora do manifesto.

## Recursos nativos

Usar `manual_handoff` para música, stickers, enquetes, links ou recursos que exijam finalização no aplicativo. O handoff deve ser dirigido ao proprietário na conversa ativa, sem envio a terceiros.

## Segurança

- Usar idempotency key lógica.
- Não editar, excluir, reagendar ou substituir mídia sem novo OK.
- Não transformar autorização de geração em autorização de publicação.
- Não transformar autorização de preview em autorização de upload.
- Não repetir publicação depois de timeout sem consultar o estado remoto.
- Se a API falhar, manter o pacote local.

## Métricas

Coletar, conforme disponibilidade:

- alcance;
- impressões;
- visualizações;
- retenção;
- conclusão;
- salvamentos;
- compartilhamentos;
- comentários;
- cliques;
- conversão;
- crescimento;
- custo.

Registrar período, amostra e limitações.

## Análise

Robotnik:

1. compara resultado com KPI;
2. avalia hook, tema, formato, direção e CTA;
3. separa fato de hipótese;
4. registra padrões vencedores e rejeitados;
5. recomenda um experimento;
6. preserva histórico.

Puppet Master decide a prioridade do próximo ciclo. Kowalski não altera o manual automaticamente. Não extrapolar conclusões de amostras pequenas.
