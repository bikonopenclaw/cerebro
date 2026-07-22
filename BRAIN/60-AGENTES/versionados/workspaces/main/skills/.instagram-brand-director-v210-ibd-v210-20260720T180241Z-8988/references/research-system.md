# Pesquisa empresarial

## Responsabilidade

Robotnik conduz a pesquisa. Puppet Master verifica aderência ao objetivo. Kowalski é a fonte primária para fatos internos de marca, produto e identidade.

## Ferramentas free-first

Usar, em ordem:

1. documentos internos fornecidos pela empresa e por Kowalski;
2. Web Search do OpenClaw;
3. SearXNG auto-hospedado, quando configurado;
4. browser ou web fetch para páginas específicas;
5. extração local de arquivos fornecidos.

Não exigir mecanismo de pesquisa pago. Não instalar serviço externo como fallback silencioso.

## Privacidade de consulta

- Usar consultas públicas e sanitizadas por padrão.
- Não incluir nome de cliente, dados pessoais, estratégia não pública, preço confidencial ou conteúdo do brandpack em consulta externa.
- Quando informação não pública for indispensável a uma consulta externa, apresentar o payload e solicitar OK específico do proprietário.
- Não enviar arquivo interno a mecanismo externo apenas para facilitar extração.

## Ordem de fontes

Priorizar:

1. documentação e canais oficiais;
2. dados públicos primários;
3. estudos e relatórios com metodologia clara;
4. imprensa reconhecida;
5. fontes secundárias com confirmação.

Para regras, preços, produtos, recursos, leis ou dados que possam mudar, verificar no momento da produção.

## Registro

Guardar em `research.md`:

| Campo | Conteúdo |
|---|---|
| URL ou arquivo | Fonte exata |
| Data de acesso | Data e fuso |
| Afirmação | O que a fonte sustenta |
| Uso | Estratégia, copy, referência ou compliance |
| Limitação | Incerteza, recorte ou possível desatualização |
| Direitos | Condições conhecidas de reutilização |
| Sensibilidade | Público ou interno |

Não guardar uma conclusão sem a fonte que a sustenta.

## Concorrentes e tendências

- Usar concorrentes para mapear território, não para copiar execução.
- Não reproduzir composição, personagem, slogan ou roteiro distintivo.
- Tratar tendência como sinal, não como obrigação.
- Rejeitar tendência incompatível com marca, público ou compliance.
- Não copiar trechos extensos, imagens ou vídeos protegidos.
- Produzir direção original a partir dos aprendizados.

## Saída

Entregar:

- fatos verificados;
- sinais de mercado;
- lacunas;
- implicações editoriais;
- oportunidades;
- riscos;
- fontes;
- dados que exigiriam autorização antes de sair do ambiente.


---

## Playbook consolidado: pesquisa

Conteúdo incorporado integralmente do playbook autônomo da candidata de 66 arquivos:

# Playbook: pesquisa

1. Classificar cada dado como público, interno ou sensível.
2. Usar fonte interna aprovada e fonte pública primária.
3. Não enviar dado interno a provider Search.
4. Se Skipper estiver desabilitado, Robotnik executa.
5. Registrar URL/arquivo, acesso UTC, afirmação, uso, limitação e direitos.
6. Separar fato, inferência e hipótese.
7. Bloquear claim sem evidência.
