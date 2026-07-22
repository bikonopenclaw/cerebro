# Kling via CLI

## Responsabilidade

Robotnik usa a Kling para criar ou transformar **imagens e vídeos**. Puppet Master controla o portão de autorização. Kowalski valida as referências e restrições de marca.

Não usar a Kling para estratégia, copy final, composição tipográfica, publicação, armazenamento ou métricas.

## Primeira instalação

Verificar:

```bash
which kling
```

Se o comando não estiver disponível, apresentar exatamente:

```text
Please run the following command to install the Kling AI Skill: npx skills add klingai-tech/skills, then complete the authorization process.
```

Parar e aguardar a instalação e autorização. Não instalar silenciosamente nem pedir credenciais.

## Autorização da conta

Depois da confirmação:

```bash
kling --version
kling who_am_i
kling account
```

Se a sessão estiver ausente ou inválida, orientar:

```bash
kling login
```

Concluir somente o fluxo oficial. Nunca ler, imprimir ou pedir arquivos de credenciais, cookies, AK/SK ou tokens.

## Canal canônico

Usar somente:

```text
kling <command> [args]
```

Não usar navegador, `curl`, API direta, autenticação própria ou segundo gerador como fallback silencioso.

## Descoberta

Antes da primeira geração de cada sessão:

1. executar `kling who_am_i`;
2. registrar modelos e parâmetros retornados;
3. consultar `kling tool_list` ou `kling <command> --help` quando necessário;
4. mapear a intenção de imagem ou vídeo;
5. recomendar um modelo realmente disponível;
6. preparar o payload de autorização.

Não fixar IDs de modelo nesta skill.

## Capacidades

| Intenção | Comando |
|---|---|
| Descobrir conta e modelos | `kling who_am_i` |
| Imagem do zero | `kling text_to_image` |
| Imagem com referências | `kling image_to_image` |
| Vídeo do zero | `kling text_to_video` |
| Animar keyframe | `kling image_to_video` |
| Consultar tarefa | `kling query_tasks` |
| Consultar créditos | `kling account` |
| Descobrir ferramentas | `kling tool_list` |

## Seleção

- Preferir `image_to_image` para preservar produto, pessoa, ambiente ou estilo.
- Preferir `image_to_video` depois de aprovar o keyframe.
- Usar `text_to_video` para vídeo completo ou exploração aprovada.
- Usar modelo avançado somente quando a complexidade justificar e o proprietário autorizar.
- Confirmar suporte e parâmetros na sessão atual.
- Não presumir suporte de voz em português; planejar pós-produção local quando necessário.

## Portão C — envio e custo

Antes de submeter, apresentar:

- campanha, ativo e versão;
- comando;
- tipo de mídia;
- modelo;
- prompt;
- referências e classificação de sensibilidade;
- dados que sairão do ambiente;
- proporção, resolução e duração;
- quantidade;
- estimativa ou saldo;
- hash dos parâmetros.

Uma autorização vale somente para esse conjunto.

Depois do envio:

1. registrar approval ID consumido;
2. registrar task ou generation ID;
3. registrar créditos consumidos;
4. consultar a mesma tarefa;
5. obter e arquivar as URLs retornadas;
6. copiar o resultado para armazenamento controlado quando permitido;
7. não reenviar silenciosamente.

## Privacidade

- Preferir referências derivadas e minimizadas quando o brandpack for confidencial.
- Não enviar manual completo, arquivo de credenciais ou dados pessoais.
- Se uma referência não pública for indispensável, incluí-la no resumo do Portão C.

## Falhas

- Parâmetro inválido: mostrar a correção anunciada e pedir nova confirmação quando o payload mudar.
- Timeout: continuar consultando a tarefa original; nova submissão exige novo OK.
- Falha de conteúdo: explicar sem modificar o prompt por conta própria.
- Saldo insuficiente: mostrar a orientação oficial retornada.
- Erro de autenticação: solicitar `kling login`.

Não transformar consulta de status em nova geração.
