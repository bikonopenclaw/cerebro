# Especificação do Controlador de Execução v1

## 1. Propósito

Definir o comportamento normativo do componente que transforma um pedido humano em um Contrato de Execução seguro, auditável e resolvido para um executor. Esta especificação é a fonte de verdade; prompts, código e configurações são implementações substituíveis.

## 2. Invariantes

1. Preservar o pedido original, sem edição.
2. Nunca ampliar autorização por inferência.
3. Ausência de proibição não equivale a permissão para efeito externo.
4. Aplicar gates antes de resolver modelo.
5. Executar sem LLM quando o caminho feliz for integralmente determinístico.
6. Separar capacidade, esforço, risco, custo/latência e modo de execução.
7. Não permitir fallback silencioso em rotas críticas.
8. Não permitir que o executor troque o próprio modelo.
9. Parar no último estado seguro quando um gate obrigatório falhar.
10. Registrar justificativa, confiança, evidência e resultado.

## 3. Entradas

Obrigatórias:

- `request_original`: texto original e anexos referenciados;
- `requester`: identidade ou origem autenticada;
- `executor_target`: agente ou classe de executor;
- `authorization_context`: permissões, gates e escopo vigentes;
- `environment_context`: ferramentas, modelos e políticas disponíveis.

Opcionais:

- prazo e prioridade;
- limite de custo;
- requisito de latência;
- formato de saída;
- evidências anteriores;
- contrato pai, em caso de subtarefa.

## 4. Saídas

O controlador deve produzir exatamente um dos estados:

- `deterministic_execution_contract`;
- `llm_execution_contract`;
- `approval_required`;
- `clarification_required` somente quando a ambiguidade impedir execução segura;
- `rejected_out_of_scope`;
- `stop_safe_state`.

Toda saída deve incluir `task_id`, classificação, confiança, justificativa objetiva, gates, política de falha e trilha de auditoria.

## 5. Algoritmo normativo

### Passo 1 — Preservação

Salvar hash, timestamp e conteúdo do pedido original. Não reescrever o original.

### Passo 2 — Normalização

Produzir uma versão operacional contendo objetivo, contexto, entradas, entregáveis, restrições, critérios de pronto e itens fora do escopo. A normalização pode esclarecer, mas não adicionar autorização.

### Passo 3 — Gate de autorização

Classificar ações em:

- permitidas;
- proibidas;
- condicionadas à aprovação;
- desconhecidas.

Ações desconhecidas com efeito externo são tratadas como condicionadas à aprovação.

### Passo 4 — Gate D0

Verificar se toda a tarefa possui procedimento fixo e critério objetivo. Em caso positivo, emitir C0/R0. Qualquer exceção retorna ao controlador.

### Passo 5 — Classificação cognitiva

Classificar:

- padrão conhecido;
- ambiguidade;
- novidade;
- número de fontes e sistemas;
- necessidade de ferramentas;
- necessidade de visão, código ou contexto longo;
- profundidade de síntese;
- decomponibilidade.

### Passo 6 — Capacidade

Selecionar C1 a C5 pela menor capacidade que satisfaz os requisitos com margem de segurança. C4 exige evidência de ganho sobre C3. C5 exige frentes independentes e critério de consolidação.

### Passo 7 — Esforço

Selecionar R0 a R5 pela menor intensidade que alcança o critério de qualidade. O risco operacional não eleva esforço automaticamente.

### Passo 8 — Risco e gates

Selecionar G0 a G3. Definir aprovação, backup, rollback, isolamento, owner e política de parada.

### Passo 9 — Resolução de modelo

Consultar o Registro de Modelos e filtrar por:

1. status ativo ou validado;
2. capacidade mínima;
3. esforço suportado;
4. ferramentas e modalidades;
5. contexto;
6. permissão para classe de risco;
7. avaliações aprovadas;
8. custo e latência.

Sem candidato elegível, parar e escalar. Não escolher modelo inferior por disponibilidade.

### Passo 10 — Contrato

Emitir contrato estruturado e brief amigável para o executor.

### Passo 11 — Execução e reclassificação

O executor pode solicitar reclassificação ao encontrar fatos novos, mas não pode aplicar a mudança por conta própria.

### Passo 12 — Validação

Validar resultado por critérios objetivos. Registrar sucesso, parcial, bloqueado ou falhou, além de latência, custo, retrabalho e mudança de rota.

## 6. Regras de confiança

- `alta`: evidência direta, padrão conhecido e classificação inequívoca;
- `média`: uma dimensão relevante depende de interpretação;
- `baixa`: fontes incompletas, pedido ambíguo ou impacto incerto.

Com confiança baixa:

- C1 é proibido;
- rotas G2/G3 exigem revisão;
- não há fallback silencioso;
- o contrato deve explicitar lacunas.

## 7. Estados de reclassificação

- `increase_reasoning`;
- `decrease_reasoning_after_eval`;
- `upgrade_capability`;
- `change_modality_or_tool_requirement`;
- `split_task`;
- `request_approval`;
- `stop_safe_state`.

Cada solicitação deve conter fatos novos, impacto, estado atual e rollback disponível.

## 8. Métricas obrigatórias

- acurácia de classificação;
- subdimensionamento crítico;
- superdimensionamento;
- taxa de fallback;
- taxa de reclassificação;
- qualidade por classe;
- latência até primeira entrega útil;
- custo por tarefa concluída;
- retrabalho;
- violações ou quase violações de gate.

## 9. Critérios de aceitação

O controlador só pode avançar do shadow mode quando:

- houver zero subdimensionamento em G3;
- concordância útil for pelo menos 90%;
- 100% dos contratos preservarem o pedido original e gates;
- todos os modelos ativos possuírem avaliação e owner;
- rollback global tiver sido testado.
