# Plano do Controlador de Execução v2

## Controle

- Solicitante: Hebert Mattedi
- Base documental: Plano Roteador de Execução v1 e Etapa 0 concluída em 2026-07-23
- Revisão proposta: 2026-07-23
- Estado: proposta documental; nenhuma implementação autorizada
- Escopo desta revisão: substituir o roteamento acoplado a nomes de modelos por um sistema baseado em capacidades, esforço de raciocínio, política operacional e registro de modelos
- Fora do escopo: alterar modelo, agente, cron, skill, gateway, configuração, produção, permissões ou gates existentes

## 1. Objetivo

Selecionar, para cada tarefa, a forma de execução mais adequada considerando:

1. necessidade real de LLM;
2. capacidades exigidas;
3. dificuldade cognitiva;
4. risco operacional;
5. latência e custo aceitáveis;
6. reversibilidade;
7. confiança da classificação;
8. disponibilidade e desempenho comprovado dos modelos atuais.

A escolha do modelo nunca amplia autorização. Produção, root, gasto, envio externo, publicação, alteração real, risco financeiro e mudança no próprio ambiente permanecem sujeitos aos gates aprovados.

## 2. Princípio estrutural

O controlador não escolhe diretamente um nome de modelo a partir da descrição da tarefa.

A sequência correta é:

1. decidir se a tarefa precisa de LLM;
2. identificar o perfil de capacidade necessário;
3. definir o esforço de raciocínio;
4. definir a política operacional e os gates;
5. consultar o Registro de Modelos;
6. resolver o modelo concreto disponível;
7. emitir um contrato de execução estruturado;
8. validar o resultado e registrar evidências.

Consequência: regras permanentes ficam vinculadas a capacidades. Nomes de modelos ficam isolados em uma camada substituível.

## 3. Arquitetura proposta

### 3.1 Controlador de Execução

Responsabilidades:

- preservar o pedido original;
- normalizar a tarefa sem alterar sua intenção;
- aplicar gates de autorização antes do roteamento;
- executar o Gate D0;
- classificar capacidade, dificuldade, risco, reversibilidade e confiança;
- escolher esforço de raciocínio;
- resolver o modelo por meio do Registro de Modelos;
- emitir o Contrato de Execução;
- receber pedidos de escalonamento do executor;
- impedir fallback inseguro ou ampliação de escopo.

O controlador deve ser majoritariamente determinístico. LLM é usado na classificação apenas quando regras e schemas não forem suficientes.

### 3.2 Executor

Responsabilidades:

- executar somente o objetivo normalizado;
- respeitar ações permitidas, proibidas e condicionais;
- usar apenas as ferramentas autorizadas;
- produzir as evidências exigidas;
- não trocar o próprio modelo silenciosamente;
- solicitar reclassificação quando surgirem fatos novos;
- parar no último estado seguro quando um gate não puder ser satisfeito.

### 3.3 Validador

Responsabilidades:

- verificar critérios objetivos de pronto;
- comparar saída com o contrato de execução;
- medir resultado, retrabalho, latência, custo, falhas e escalonamentos;
- detectar subdimensionamento e superdimensionamento;
- alimentar avaliações e recalibração.

Quando possível, o validador deve ser determinístico e independente do executor.

### 3.4 Registro de Modelos

Responsabilidades:

- mapear perfis de capacidade para modelos concretos disponíveis;
- registrar capacidades suportadas, esforços aceitos, contexto, ferramentas, modalidades, latência, custo, limites e estado operacional;
- manter aliases separados de snapshots fixos;
- permitir substituição de modelo sem alterar as regras centrais;
- conter resultados de avaliações internas por classe de tarefa;
- impedir o uso de modelo não validado para rota crítica.

## 4. Gate D0: necessidade de LLM

Antes de classificar capacidades, verificar se toda a tarefa pode ser concluída por ferramenta, script ou validador com procedimento fixo e resultado objetivo.

### 4.1 Exemplos de rota determinística

- hashes;
- empacotamento;
- contagens;
- validação estrutural;
- verificação de existência e abertura de arquivos;
- coleta com contrato fixo;
- transformação tabular previsível;
- transcrição local quando não houver interpretação;
- aplicação de formatter, linter ou teste definido;
- consultas parametrizadas sem julgamento.

### 4.2 Regra de exceção

Qualquer divergência, ambiguidade, erro inesperado ou necessidade de julgamento retorna ao controlador. A exceção pode exigir LLM, mas isso não transforma automaticamente toda a rotina determinística em uma rota de LLM.

## 5. Dimensões independentes de classificação

### 5.1 Perfil de capacidade

Define o que o executor precisa ser capaz de fazer.

### 5.2 Esforço de raciocínio

Define quanto processamento cognitivo é necessário para alcançar qualidade suficiente.

### 5.3 Risco operacional

Define aprovações, isolamento, backup, rollback, validação e política de parada.

### 5.4 Política de custo e latência

Define preferência entre modelos que satisfazem a mesma capacidade.

### 5.5 Modo de execução

Define execução padrão, modo de qualidade reforçada ou paralelismo. Não deve ser confundido com esforço de raciocínio.

Regra central:

> Complexidade escolhe capacidade e esforço. Risco escolhe gates. Custo e latência escolhem entre modelos já qualificados.

## 6. Perfis de capacidade

### C0. Determinístico

- LLM: não requerido no caminho feliz.
- Uso: procedimento fixo, entrada estruturada e critério objetivo.
- Escalonamento: qualquer divergência retorna ao controlador.

### C1. Eficiente estruturado

Capacidades requeridas:

- seguir instruções precisas;
- classificação, extração ou transformação simples;
- saída estruturada;
- uso limitado de ferramentas;
- baixo custo e baixa latência.

Uso típico:

- triagem;
- normalização;
- preenchimento de schemas;
- resumo curto de fonte única;
- geração repetitiva com template;
- subagente de escopo fechado.

Restrições:

- não usar em tarefa crítica;
- não usar com baixa confiança;
- não usar quando houver arquitetura, causa raiz, múltiplas dependências ou ambiguidade relevante.

### C2. Profissional equilibrado

Capacidades requeridas:

- síntese entre fontes;
- documentos e comunicação profissional;
- análise operacional;
- conciliação financeira em leitura;
- julgamento moderado;
- uso confiável de ferramentas;
- boa relação entre qualidade, custo e latência.

Uso típico:

- relatórios recorrentes;
- documentos operacionais;
- planejamento conhecido;
- conteúdo com regras claras;
- análise sem ação financeira externa;
- coordenação normal entre agentes.

Este é o perfil de porto seguro quando C1 não estiver comprovado ou a confiança for insuficiente para rebaixamento.

### C3. Profundo multidomínio

Capacidades requeridas:

- raciocínio complexo;
- arquitetura;
- código novo ou refatoração ampla;
- integração entre sistemas;
- diagnóstico difícil;
- causa raiz;
- segurança defensiva;
- alta ambiguidade;
- múltiplas fontes ou modalidades;
- planejamento de longo horizonte.

Uso típico:

- projeto de arquitetura;
- incidente obscuro;
- integração inédita;
- análise de confiabilidade;
- conteúdo multi-asset com QA complexo;
- decisão estratégica de alta incerteza.

### C4. Fronteira de qualidade

Capacidades requeridas:

- maior confiabilidade disponível;
- exploração e verificação intensivas;
- síntese difícil com alto custo de erro intelectual;
- tarefas em que avaliações demonstram ganho real sobre C3.

Importante: C4 não é sinônimo de tarefa operacionalmente crítica. Uma tarefa simples e destrutiva exige gates fortes, não necessariamente capacidade C4. Uma tarefa sem efeito externo pode exigir C4 por dificuldade intelectual.

### C5. Paralelo coordenado

Capacidades requeridas:

- decomposição em duas ou mais frentes independentes;
- delegação com owners claros;
- consolidação e resolução de conflito;
- critério de pronto por frente;
- ganho mensurável de tempo ou qualidade.

Não usar:

- tarefa simples;
- investigação estritamente sequencial;
- mudança urgente sem tempo para consolidação;
- frentes que disputem o mesmo estado mutável;
- tarefa em que paralelismo amplie risco ou custo sem ganho comprovado.

C5 é um modo de orquestração, não uma categoria de “modelo mais inteligente”.

## 7. Níveis de esforço de raciocínio

O controlador usa os níveis lógicos abaixo. O Registro de Modelos traduz o nível lógico para os valores efetivamente aceitos por cada modelo.

### R0. Nenhum

- Procedimento direto ou geração sem necessidade de deliberação.
- Preferência para tarefas de alta previsibilidade.

### R1. Baixo

- Poucas decisões locais.
- Prompt preciso e critério objetivo.
- Prioridade para latência e custo.

### R2. Médio

- Padrão inicial para trabalho profissional equilibrado.
- Algumas etapas de análise, comparação ou uso de ferramentas.

### R3. Alto

- Raciocínio multi-etapa;
- integração de evidências;
- diagnóstico;
- planejamento não trivial;
- ganho de qualidade medido em avaliações.

### R4. Muito alto

- Problemas difíceis e ambíguos;
- arquitetura ou verificação extensa;
- uso somente quando R3 apresentar lacunas mensuráveis.

### R5. Máximo

- Reservado para as tarefas intelectualmente mais difíceis e orientadas a qualidade;
- deve ser comparado empiricamente com R4;
- não é acionado apenas por risco operacional;
- exige justificativa e registro de custo e latência.

## 8. Matriz capacidade × esforço

| Situação | Capacidade | Esforço inicial | Observação |
|---|---|---:|---|
| Extração ou classificação fechada | C1 | R0 ou R1 | saída estruturada e validação objetiva |
| Rotina profissional conhecida | C2 | R1 ou R2 | subir somente por evidência |
| Síntese moderada entre fontes | C2 | R2 | validar fontes e lacunas |
| Patch técnico conhecido e reversível | C1 ou C2 | R2 | depende de avaliações de código |
| Implementação técnica mapeada | C2 ou C3 | R2 ou R3 | testes e diff limitado |
| Código novo ou refatoração ampla | C3 | R3 ou R4 | QA e critérios claros |
| Diagnóstico difícil ou causa raiz | C3 | R3 ou R4 | escalonar se surgirem novos sistemas |
| Arquitetura nova | C3 ou C4 | R3 ou R4 | C4 somente com ganho comprovado |
| Problema intelectual extremo | C4 | R4 ou R5 | comparar qualidade, custo e latência |
| Banco, produção ou perda de dados | capacidade conforme dificuldade | esforço conforme dificuldade | gates críticos obrigatórios e independentes |
| Frentes realmente independentes | C5 + capacidade por frente | esforço por frente | consolidação obrigatória |

## 9. Classes de risco e gates

### G0. Sem efeito externo

- leitura, análise ou geração local;
- validação normal;
- sem aprovação adicional quando já estiver dentro do escopo.

### G1. Reversível e baixo impacto

- alteração local pequena;
- teste obrigatório;
- diff limitado;
- rollback simples documentado.

### G2. Impacto moderado

- múltiplos arquivos ou sistemas;
- revisão antes de aplicar;
- checkpoint;
- evidências e rollback testável.

### G3. Crítico

Inclui, entre outros:

- produção;
- root;
- banco;
- gateway;
- cron;
- pagamento;
- emissão ou cancelamento fiscal;
- envio externo;
- publicação;
- credenciais ou acesso;
- segurança;
- P1/P2;
- perda de dados;
- mudança no próprio ambiente do controlador.

Gates obrigatórios:

- autorização explícita;
- alvo e escopo exatos;
- plano;
- backup ou snapshot quando aplicável;
- rollback;
- validação antes e depois;
- parada no último estado seguro;
- sem fallback silencioso;
- registro de auditoria.

## 10. Política de confiança

A confiança do controlador deve ser registrada em escala normalizada e acompanhada dos fatores que a reduziram.

### Regras

- confiança alta: rota eficiente pode ser considerada se houver avaliação suficiente;
- confiança média: usar porto seguro do perfil de capacidade;
- confiança baixa: não usar C1 automaticamente; preferir C2 ou C3 conforme a dificuldade;
- confiança baixa em G3: parar e exigir reclassificação ou aprovação;
- ausência de fonte, timestamp, escopo ou critério de pronto reduz confiança;
- modelo forte não compensa contrato incompleto.

A confiança da classificação não deve ser confundida com confiança na resposta final. Ambas devem ser medidas separadamente.

## 11. Registro de Modelos

O Registro de Modelos deve ser um artefato versionado, por exemplo `MODEL-REGISTRY.yaml`.

### 11.1 Campos mínimos

```yaml
registry_version: 1
updated_at_utc: "2026-07-23T00:00:00Z"
models:
  - model_id: "modelo-concreto"
    provider: "openai"
    alias_or_snapshot: "alias"
    status: "candidate|validated|restricted|disabled"
    capability_tiers: ["C2", "C3"]
    supported_reasoning: ["R0", "R1", "R2", "R3"]
    modalities: ["text", "image_input"]
    tool_use: true
    structured_outputs: true
    context_class: "large"
    latency_class: "medium"
    cost_class: "medium"
    critical_route_allowed: false
    eval_sets_passed: []
    known_limitations: []
```

### 11.2 Resolução

O controlador deve:

1. filtrar apenas modelos ativos e permitidos;
2. exigir compatibilidade com capacidade, modalidade, ferramentas e contexto;
3. exigir suporte ao esforço escolhido;
4. excluir modelos não validados para a classe de tarefa;
5. aplicar política de risco;
6. escolher a opção de menor custo e latência que alcance o piso de qualidade;
7. registrar alternativas e motivo da escolha.

### 11.3 Alias e snapshot

- alias pode ser usado em experimentação e shadow mode;
- snapshot fixo é preferível em produção quando consistência e auditoria forem críticas;
- mudança de alias deve disparar nova avaliação;
- atualização do Registro não autoriza automaticamente rollout.

## 12. Mapeamento de referência atual

Este mapeamento é informativo e deve permanecer fora das regras permanentes.

| Perfil lógico | Candidato atual de referência | Uso esperado |
|---|---|---|
| C1 eficiente | família eficiente de menor custo validada | classificação, extração, rotinas fechadas e alto volume |
| C2 equilibrado | `gpt-5.6-luna` ou `gpt-5.6-terra`, conforme avaliações | trabalho profissional recorrente e tool use moderado |
| C3 profundo | `gpt-5.6-terra` ou `gpt-5.6-sol` | arquitetura, integração, diagnóstico e código complexo |
| C4 fronteira | `gpt-5.6-sol` | qualidade máxima quando avaliações mostrarem ganho |
| C5 paralelo | GPT-5.6 com recurso multiagente, quando habilitado e validado | frentes independentes com consolidação |

Regras:

- `gpt-5.6` é tratado como alias e não como capacidade;
- `sol`, `terra` e `luna` são opções do Registro, não nomes embutidos na lógica;
- esforço é escolhido independentemente entre os níveis suportados pelo modelo;
- modo de qualidade reforçada, quando utilizado, é independente do esforço;
- multiagente é decisão de orquestração independente;
- o mapeamento deve ser revisto sempre que houver mudança de catálogo, preço, limite ou avaliação.

## 13. Modo de qualidade e modo paralelo

### 13.1 Qualidade reforçada

Usar somente quando:

- qualidade tiver prioridade clara sobre latência e custo;
- tarefa for intelectualmente difícil;
- avaliações demonstrarem ganho;
- houver orçamento e política aprovados.

Não usar como reação automática a risco G3.

### 13.2 Paralelismo

Usar somente quando:

- existirem ao menos duas frentes independentes;
- cada frente tiver entrada, owner e critério de pronto;
- consolidação estiver definida;
- custo adicional estiver justificado;
- não houver disputa por estado mutável.

## 14. Contrato de Execução

O controlador deve emitir um objeto estruturado antes da execução.

### 14.1 Campos mínimos

```json
{
  "task_id": "tsk_...",
  "original_request": "texto imutável",
  "normalized_objective": "objetivo operacional",
  "execution_route": "deterministic|llm|hybrid",
  "capability_profile": "C0|C1|C2|C3|C4|C5",
  "reasoning_effort": "R0|R1|R2|R3|R4|R5",
  "risk_class": "G0|G1|G2|G3",
  "confidence": 0.0,
  "resolved_model": "modelo do registro ou null",
  "execution_mode": "standard|quality|parallel",
  "allowed_actions": [],
  "forbidden_actions": [],
  "approval_requirements": [],
  "required_tools": [],
  "success_criteria": [],
  "required_evidence": [],
  "fallback_policy": "...",
  "reclassification_triggers": [],
  "executor_brief": "..."
}
```

### 14.2 Precedência

Em conflito entre campos:

1. autorização e proibições;
2. gates de risco;
3. pedido original;
4. critérios de sucesso;
5. objetivo normalizado;
6. preferência de modelo, esforço, custo e latência.

## 15. Política de fallback

### 15.1 Fallback permitido

Somente quando:

- o modelo alternativo satisfizer a mesma capacidade mínima;
- suportar ferramentas, modalidade, contexto e esforço necessários;
- estiver validado para a classe de tarefa;
- não reduzir gates;
- a troca for registrada.

### 15.2 Fallback proibido

- para perfil de capacidade inferior sem reclassificação;
- silencioso em G3;
- para modelo não avaliado;
- quando a falha indicar mudança de escopo ou dificuldade;
- quando houver risco de perda de estado ou dados.

### 15.3 Falha segura

Em G3, indisponibilidade de rota ou modelo significa parar no último estado seguro, registrar evidência e solicitar nova decisão.

## 16. Gatilhos de reclassificação durante a execução

O executor deve solicitar nova rota quando ocorrer:

- sistema ou arquivo não previsto;
- aumento do número de componentes afetados;
- divergência relevante entre fontes;
- teste repetidamente falho;
- mudança de patch local para arquitetura;
- surgimento de ação externa;
- aumento de risco;
- contexto insuficiente;
- ferramenta obrigatória indisponível;
- confiança abaixo do limiar;
- necessidade de ação fora da autorização;
- descoberta de que a tarefa pode ser concluída deterministicamente.

O executor não troca o próprio modelo. Ele devolve fatos novos e o estado seguro atual ao controlador.

## 17. Regras duras revisadas

- Gate D0 vem antes de qualquer seleção de modelo.
- Capacidade, esforço, risco, custo e modo de execução são decisões separadas.
- Nomes de modelos não aparecem em regras permanentes.
- O Registro de Modelos é a única camada autorizada a mapear capacidades para modelos concretos.
- Usar o menor perfil que alcance o piso de qualidade comprovado.
- Não rebaixar para C1 com confiança baixa ou sem avaliação suficiente.
- Não elevar esforço apenas porque a tarefa é operacionalmente arriscada.
- Não reduzir gates porque o modelo é mais forte.
- Não usar C4, R5, qualidade reforçada ou paralelismo sem ganho mensurável.
- Não fazer fallback silencioso em tarefa crítica.
- Produção, root, gasto, envio externo e alteração real mantêm os gates existentes.
- Fast mode, prioridade de latência ou equivalente é decisão separada e depende de política de custo aprovada.

## 18. Plano cadenciado revisado

### Etapa 0. Baseline read-only — concluída

- 40 tarefas reais analisadas.
- Primeiro aprendizado preservado: decidir antes se LLM é necessário.
- A baseline histórica deve ser reexpressa em C0–C5, R0–R5 e G0–G3, sem apagar as recomendações originais.
- Nenhuma configuração alterada.

### Etapa 0.5. Normalização da baseline — proposta

- Converter os 40 casos para capacidade, esforço e risco.
- Separar “dificuldade” de “criticidade operacional”.
- Criar versão inicial do Registro de Modelos.
- Marcar recomendações sem evidência suficiente como `candidate`.
- Atualizar casos de teste para verificar contrato, gates e reclassificação.
- Estado: não autorizada.

### Etapa 1. Shadow mode

- Duração de referência: 5 dias úteis.
- O controlador emite capacidade, esforço, risco, modelo resolvido e contrato, mas não muda a execução real.
- Comparar recomendação com rota real e resultado.
- Medir também superdimensionamento, e não apenas subdimensionamento.
- Gates mínimos:
  - zero subdimensionamento em G3;
  - zero ampliação de autorização;
  - pelo menos 90% de concordância útil;
  - contrato válido em pelo menos 98% dos casos;
  - justificativa reproduzível para toda rota C4, R5 ou paralela.
- Estado: não autorizada.

### Etapa 2. Piloto controlado

- Duração de referência: 7 dias.
- Automatizar somente rotas C0 e C1 já validadas e de baixo risco.
- Limite inicial: 20% das execuções elegíveis.
- C2 ou superior continua registrado e revisado.
- Rollback não fixa um nome de modelo; restaura um perfil de porto seguro definido no Registro.
- Estado: não autorizada.

### Etapa 3. Expansão por agente

Cada agente recebe uma política de capacidades permitidas, não uma lista fixa de modelos.

Exemplo:

- Kowalski: C0/C1 em rotinas técnicas fechadas; C2 em relatórios e exceções; C3 mediante critérios.
- Darth Vader: C2 em análise financeira somente leitura; ações fiscais externas permanecem G3; C3 em integração complexa.
- Robotnik: C1 em transformações padronizadas; C2 em campanha e copy; C3 em multi-asset ou QA complexo.
- Sentinel: C3 como porto seguro até avaliações provarem rotas C0/C1 sem perda de sensibilidade; P1/P2 sempre G3.
- Puppet Master: C2 em coordenação normal; C3/C4 em estratégia, arquitetura e crise conforme avaliação.

Estado: não autorizada.

### Etapa 4. Produção governada

Registrar em UTC:

- tarefa;
- pedido original;
- objetivo normalizado;
- capacidade;
- esforço;
- risco;
- confiança;
- modelo resolvido e snapshot;
- modo de execução;
- justificativa;
- gates;
- fallback;
- custo e latência;
- resultado;
- retrabalho;
- escalonamentos;
- validação.

Revisão semanal no primeiro mês. Recalibração mensal ou quando ocorrer mudança relevante no Registro de Modelos.

## 19. Métricas de avaliação

### Qualidade

- conclusão correta;
- aderência ao escopo;
- critérios de pronto atendidos;
- retrabalho;
- falhas factuais;
- falhas de ferramenta;
- avaliações por classe de tarefa.

### Segurança e governança

- ampliação indevida de autorização;
- gate omitido;
- fallback inseguro;
- ação externa não autorizada;
- falha de parada segura;
- rastreabilidade do contrato.

### Eficiência

- latência até primeira entrega útil;
- custo total;
- tokens de entrada, saída e raciocínio quando disponíveis;
- chamadas de ferramentas;
- taxa de uso determinístico;
- taxa de superdimensionamento;
- ganho real de paralelismo.

### Roteamento

- precisão por capacidade;
- precisão por esforço;
- precisão por risco;
- frequência de reclassificação;
- confiança calibrada;
- desempenho por modelo e snapshot.

## 20. Critérios de promoção

Um modelo só pode ser promovido de `candidate` para `validated` em um perfil quando:

- houver amostra representativa;
- o piso de qualidade for atingido;
- não houver falha crítica relevante;
- custo e latência forem medidos;
- limitações estiverem registradas;
- regressões forem comparadas com o porto seguro;
- a decisão for aprovada quando o perfil permitir G3.

Uma rota eficiente não é promovida apenas porque é mais barata. Uma rota de fronteira não é promovida apenas porque é mais forte.

## 21. Rollback futuro

Se uma etapa posterior produzir erro de rota:

1. desativar o controlador automático;
2. limpar overrides da etapa;
3. restaurar o perfil de porto seguro configurado no Registro de Modelos;
4. preservar gates e autorizações;
5. validar agentes, sessões e jobs afetados;
6. registrar evento, modelo, snapshot, capacidade, esforço, risco e causa;
7. bloquear a combinação que falhou até nova avaliação.

O rollback não deve depender de um nome fixo de modelo no documento principal.

## 22. Impacto sobre a Etapa 0 existente

A Etapa 0 continua válida como evidência histórica, mas suas recomendações precisam ser reinterpretadas:

- “Determinístico, sem LLM” torna-se C0.
- “Spark” torna-se hipótese de C1, ainda não validada.
- “GPT-5.5 high” torna-se principalmente C2 com R2 ou R3, sujeito a reavaliação.
- “GPT-5.6-Sol high/xhigh” torna-se C3 com R3 ou R4.
- “GPT-5.6-Sol max” deve ser dividido em duas perguntas:
  - a dificuldade realmente exige C4/R5?
  - ou a tarefa é apenas G3 e requer gates fortes?
- “Ultra” torna-se C5, modo paralelo, e continua sem evidência na amostra.

As contagens históricas não devem ser convertidas mecanicamente sem revisar cada caso, porque o plano anterior misturava dificuldade intelectual com risco operacional.

## 23. Decisão recomendada

Não iniciar troca automática de modelo.

Próximo passo recomendado:

1. executar a Etapa 0.5 em modo documental e read-only;
2. reclassificar os 40 casos nas dimensões C, R e G;
3. criar o Registro de Modelos inicial;
4. definir o perfil de porto seguro por classe de tarefa;
5. preparar testes de roteamento, fallback e reclassificação;
6. somente depois solicitar autorização para shadow mode.

## 24. Garantias desta revisão

- Nenhum modelo ou esforço foi alterado.
- Nenhuma configuração, agente, cron, skill, gateway ou produção foi alterada.
- Nenhuma autorização foi ampliada.
- As etapas de implementação continuam não autorizadas.


## 24. Referências normativas e operacionais

- A camada permanente de roteamento é baseada em capacidades, não em nomes de modelos.
- O Registro de Modelos é uma fotografia operacional datada e deve ser recalibrado quando modelos, preços, limites ou parâmetros mudarem.
- Na fotografia de 2026-07-23, a documentação oficial da OpenAI descreve GPT-5.6 Sol como opção de fronteira, Terra como equilíbrio entre inteligência e custo e Luna como opção eficiente; `reasoning.effort` é configurável independentemente do modelo e pode variar conforme o modelo.
- Modo `pro`, multiagente, ferramentas, contexto e esforço de raciocínio são dimensões distintas e não devem ser fundidas em uma única escala.

## 25. Decisão de aprovação

Este documento substitui o Plano Roteador de Execução v1 apenas como proposta arquitetural. A Etapa 0 histórica permanece imutável. A próxima ação autorizável é a Etapa 0.5, em modo read-only, para reclassificar a baseline e validar o Registro de Modelos. Nenhuma troca automática de modelo está autorizada por este documento.
