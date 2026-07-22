# Deploy atômico de skills com hash canônico

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: implantação Instagram Brand Director v2.1.0 em 2026-07-20
confiabilidade: alta
ultima_revisao: 2026-07-20
tags: [skills, deploy, atomicidade, hash, backup, rollback, auditoria]
```

## Princípio

Uma skill só deve ser considerada implantada quando conteúdo, algoritmo de hash, plano, backup, troca, validação e evidência formarem um único protocolo verificável. Copiar arquivos sobre a árvore ativa não oferece atomicidade nem rollback confiável.

## Plano imutável

Antes da janela, congelar um plano com:

1. caminho ativo e staging irmão no mesmo filesystem;
2. inventário e hash esperados da árvore ativa e da candidata;
3. nome e versão do algoritmo canônico de hash;
4. correlation ID único;
5. aprovação vinculada ao plano e aos hashes;
6. validators pré-corte e pós-corte;
7. caminhos de backup, evidência e rollback;
8. regra de parada no primeiro desvio.

Hash sem algoritmo nomeado é ambíguo. Ordenação, normalização de caminho e bytes incluídos devem fazer parte da convenção. Se uma evidência histórica usar outro algoritmo, preservar os dois valores e produzir manifesto de equivalência antes de pedir nova autorização.

## Sequência de corte

1. Validar candidata, inventário, permissões, ausência de symlink, bytecode e segredo.
2. Recalcular os hashes pelo algoritmo canônico no staging e imediatamente antes do corte.
3. Adquirir lock exclusivo para impedir implantação concorrente.
4. Criar e verificar backup integral da árvore ativa.
5. Executar troca atômica no mesmo filesystem, preferencialmente com `renameat2(RENAME_EXCHANGE)`.
6. Rodar todos os validators pós-corte sem reiniciar ou aplicar outra mudança na mesma janela.
7. Se qualquer gate falhar, trocar as árvores novamente e validar a restauração do hash anterior.
8. Preservar a candidata retirada, o backup e as evidências até o encerramento formal.

Sem suporte real à troca atômica, parar. Não usar overlay ou sequência de dois renames como fallback silencioso.

## Evidência e recibo

- Registrar eventos append-only com timestamp UTC, correlation ID, ator, plano, hashes antes/depois, validators, resultado e caminho de rollback.
- Encadear eventos por SHA-256 ou mecanismo equivalente para tornar adulteração detectável.
- Ancorar o hash terminal da evidência em um recibo final.
- Lifecycle administrativo e estado real da árvore são dimensões diferentes. Se a ponte nativa não existir, registrar `cut complete, lifecycle pending` sem fingir que a proposta foi aplicada pelo mecanismo administrativo.
- Nunca registrar token, senha, certificado ou segredo no recibo.

## Critério de pronto

O deploy termina somente quando a árvore ativa tem o hash planejado, todos os validators passam, o backup reproduz o hash anterior, o rollback foi comprovado ou permanece executável, a evidência append-only fecha e o lifecycle administrativo está reconciliado ou explicitamente pendente.

## Relações

- `BRAIN/01-DIARIO/2026/2026-07-20.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/60-AGENTES/versionados/`

## Registro de reconciliação (2026-07-21)

- Executada checagem de consistência entre proposta e ativo da Instagram Brand Director.
- Resultado: proposta `instagram-brand-director-20260720` permanece em `pending` e **não** se encontra ativa;
- ativo do workspace segue com hash `ed9fa5704025e7d91b3d171abdb6cc6c6ecd664cbcc41ba5774128cd3f4e68cd` (39 arquivos);
- candidato/histórico do ciclo está com hash `d2c1a74768ed37e6666ac62a14329992ccce393d994c0bf4700443e225165226`.
- Em consequência, reconciliação administrativamente continua em aberto: não houve correlação automática nem atualização de snapshot nesta janela.
