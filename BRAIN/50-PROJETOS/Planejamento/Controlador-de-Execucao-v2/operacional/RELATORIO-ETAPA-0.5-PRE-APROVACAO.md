# Etapa 0.5, relatório pré-aprovação

> Status: `superseded`.
>
> Este documento preserva o estado anterior à aprovação das nove correções C/R/G. Foi substituído por [RELATORIO-ETAPA-0.5-VALIDADO.md](RELATORIO-ETAPA-0.5-VALIDADO.md) e não é a referência operacional vigente.

## Estado

- Modo: read-only sobre evidências e configuração.
- Implementação: não autorizada.
- Roteamento automático: não ativado.
- Casos de teste: preservados sem alterações C/R/G.
- Resultado: `31 alinhados`, `9 divergências C/R/G`, `2 lacunas de evidência local`.

## Integridade do pacote

- Manifesto: 10 de 10 hashes e tamanhos conferidos.
- Baseline v2: 40 registros, além do cabeçalho.
- Delimitador: `;`.
- Colunas: 26.
- Os 18 campos históricos da baseline v1 foram preservados sem diferença, desconsiderando apenas o zero à esquerda do ID.
- Distribuição proposta pelo pacote:
  - C0: 8;
  - C2: 14;
  - C3: 18;
  - G0: 27;
  - G1: 2;
  - G2: 5;
  - G3: 6.

## Evidências

- 25 referências locais existiam exatamente no caminho informado.
- A referência do caso 13 existe em `logs/alteracoes-modelos/`, não em `logs/alteracoes/`.
- A referência do caso 21 usa notação de intervalo, mas os 28 PDFs `NFSe-191.pdf` a `NFSe-218.pdf` existem.
- 11 referências de sessão foram preservadas da baseline v1 e as sessões correspondentes permanecem conhecidas no ambiente.
- Casos 27 e 28: os diretórios de evidência informados não existem mais no workspace do Robotnik. A classificação não pode virar ground truth com a evidência atual.

## Revisão linha a linha

| ID | Evidência | C/R/G proposto | Veredito |
|---:|---|---|---|
| 01 | sessão conhecida | C3/R4/G0 | alinhado |
| 02 | sessão conhecida | C2/R3/G3 | alinhado |
| 03 | sessão conhecida | C2/R2/G2 | divergência: publicação externa é G3 pelos gates vigentes |
| 04 | sessão conhecida | C0/R0/G0 | alinhado |
| 05 | artefato local | C3/R3/G0 | alinhado |
| 06 | plano local | C3/R4/G3 | divergência: produzir o plano é G0; executar a migração seria G3 |
| 07 | registro local | C3/R3/G2 | alinhado |
| 08 | diretório local | C2/R3/G0 | alinhado |
| 09 | relatório local | C0/R0/G0 | alinhado |
| 10 | relatório local | C0/R0/G0 | alinhado |
| 11 | relatório local | C0/R0/G0 | alinhado |
| 12 | modelo local | C2/R2/G0 | alinhado |
| 13 | caminho corrigível | C2/R3/G1 | C/R/G alinhado; referência de evidência precisa correção |
| 14 | diretório local | C3/R3/G0 | alinhado |
| 15 | diretório local | C3/R3/G0 | alinhado |
| 16 | sessão conhecida | C2/R3/G0 | alinhado |
| 17 | sessão conhecida | C2/R2/G0 | alinhado |
| 18 | CSV local | C2/R2/G0 | alinhado com confiança média |
| 19 | relatório local | C3/R3/G2 | divergência: consulta API read-only sem efeito é G0 |
| 20 | relatório local | C2/R2/G0 | divergência: conferência objetiva de manifesto é C0/R0 |
| 21 | 28 PDFs presentes | C0/R0/G0 | alinhado |
| 22 | hashes locais | C0/R0/G0 | alinhado |
| 23 | ZIP local | C0/R0/G0 | alinhado |
| 24 | relatório local | C2/R2/G0 | alinhado |
| 25 | sessão conhecida | C0/R0/G0 | alinhado |
| 26 | sessão conhecida | C3/R3/G0 | alinhado |
| 27 | artefato ausente | C2/R2/G0 | não confirmável; manter candidate |
| 28 | artefato ausente | C3/R3/G0 | não confirmável; manter candidate |
| 29 | artefato local | C2/R2/G0 | alinhado |
| 30 | artefato local | C2/R3/G2 | divergência: preparar prompt e QA local é G0; gerar mídia com custo exigiria novo gate |
| 31 | sessão conhecida | C3/R3/G1 | alinhado |
| 32 | sessão conhecida | C2/R2/G3 | alinhado |
| 33 | registro local | C3/R3/G0 | divergência: criou integração, arquivos, backup e executou probe; classificar G2 |
| 34 | registro local | C3/R3/G0 | divergência: criou integração, arquivos, backup e executou probe; classificar G2 |
| 35 | registro local | C3/R3/G0 | divergência: criou integração, inventário e auditoria; classificar G2 |
| 36 | evidência local | C3/R4/G3 | alinhado |
| 37 | registro local | C3/R3/G3 | alinhado |
| 38 | evidência local | C3/R3/G2 | divergência: ativação de canário com cron é G3 |
| 39 | evidência local | C3/R3/G3 | alinhado |
| 40 | sessão conhecida | C3/R3/G0 | alinhado |

## Divergências pendentes de aprovação

Nenhuma linha ou caso de teste foi alterado.

| ID | Campo | Pacote | Recomendação |
|---:|---|---|---|
| 03 | G | G2 | G3 |
| 06 | G | G3 | G0 |
| 19 | G | G2 | G0 |
| 20 | C/R | C2/R2 | C0/R0 |
| 30 | G | G2 | G0 |
| 33 | G | G0 | G2 |
| 34 | G | G0 | G2 |
| 35 | G | G0 | G2 |
| 38 | G | G2 | G3 |

## Registry operacional

- Configuração ativa confirmada pelo hash `7ff4d90f62514e5d4c842858fe95c9f5211ca8b9e3a1aa62663878881a39f06f`.
- Modelos efetivamente observados nas sessões verificadas: dois IDs concretos, ambos com pensamento `high`.
- Modelos eficientes e fallbacks aparecem configurados, mas não foram promovidos por ausência de avaliação.
- Os candidatos Luna e Terra do pacote não aparecem na configuração ativa nem nas sessões verificadas.
- O runtime não expôs snapshots fixos reproduzíveis. Por isso nenhuma rota crítica foi habilitada.

Referência: [MODEL-REGISTRY-OPERACIONAL-V1.yaml](MODEL-REGISTRY-OPERACIONAL-V1.yaml).

## Diff documental v1 para v2

- Roteamento por nome concreto foi substituído por capacidade C0-C5.
- Esforço R0-R5 foi separado da criticidade operacional G0-G3.
- Gate D0 foi mantido e formalizado.
- C5 passou a representar modo paralelo, não inteligência máxima.
- O executor não pode trocar o próprio modelo.
- O Registry virou a única camada operacional autorizada a conter nomes concretos.
- Os gates históricos foram preservados.

## Limitações

- A Etapa 0.5 não mede qualidade, custo ou latência por modelo.
- C1 continua sem subamostra técnica independente.
- Nenhum modelo possui snapshot fixo confirmado.
- Casos 27 e 28 não têm evidência local consultável.
- As nove divergências aguardam decisão do Hebert.

## Próximo passo

Submeter as nove divergências C/R/G para aprovação. Somente depois atualizar a baseline v2 e os casos de teste. A Etapa 1 permanece bloqueada e, se autorizada no futuro, deve ser apenas shadow mode.
