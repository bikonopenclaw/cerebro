# Rota produtiva Bikon

Estado: ROTA NATIVA REGISTRADA PARA VALIDAÇÃO COM UM PILOTO; aceite produtivo final depende do resultado real, revisão e decisão humana.

Autenticação permitida: somente conta ChatGPT já autorizada do Robotnik, na identidade nativa do gateway existente. Nenhuma API key, CLI de imagem paga, outro provider, conector, root renderer ou ampliação de permissões é rota alternativa.

A rota principal única é `image_gen.imagegen`, ferramenta embutida do Codex/ChatGPT, anunciada no schema real da sessão Robotnik `01a08130-089d-7a10-ae3c-a5a7cfe144e1`, gateway run `a30f1349-aa82-49be-a923-abb208df95d4` em 08/09/2026. Consumir pelo code mode nativo, com `tools.image_gen__imagegen`, conforme schema anunciado. Não usar `openclaw.image_generate`: foi apenas inventariado, não é a rota principal registrada. Não gerar pela CLI de imagem.

O caminho host da skill técnica `.system/imagegen/SKILL.md` não está montado no filesystem de comandos do Robotnik. Isso não bloqueia a ferramenta embutida. A instrução técnica legível para esta rota está neste documento; não ficar tentando ler o caminho inacessível nem copiar credenciais. Nenhuma permissão do sandbox foi ampliada.

Operação: abrir primeiro a referência local com `view_image`; fornecer `referenced_image_paths` quando o schema e o acesso nativo admitirem todos os arquivos, ou `num_last_images_to_include` com o menor número de imagens já visíveis necessário. Nunca usar os dois campos juntos. O papel da imagem é referência de estilo, não alvo a copiar. Chamar uma vez para o único piloto; aguardar o mesmo handle com `wait` se a chamada ainda estiver em execução. Entregar o retorno ao runtime com `generatedImage(result)` quando aplicável. Capturar o resultado real e copiar somente o artefato gerado pelo mecanismo autorizado para `entregas/piloto-contrato-criativo-v1-20260908/`. Não depender de um argumento inventado de destino ou de uma cópia root. Se o artefato não for legível por mecanismo autorizado, registrar a falha de handoff e bloquear, sem ampliar roots.

A ferramenta embutida usa a autenticação ChatGPT já existente; não solicitar API key. Conteúdo, restrições e referência vêm do contrato integral. Deterministicamente aplicar o logo PNG oficial na finalização sem redesenho, mantendo alfa e proporção. Uma eventual mudança da ferramenta principal exige revisão explícita deste registro e aprovação de Hebert.

Para produção, carregar o contrato integral e insumos de brand-assets.json. A referência é entrada de geração/edição quando suportada e comparação visual obrigatória. Registrar nome exato da ferramenta, chamada, provider, sessão, referência de entrada, saída bruta e hashes separados. Não chamar ferramentas de publicação ou staging.

Finalização determinística permitida: tipografia, aplicação do PNG oficial transparente, recorte, contraste e exportação 1080 × 1350 sRGB. Não substitui a fotografia humana. Revisão Kowalski exige os arquivos reais por handoff restrito autorizado. Falta de acesso do revisor bloqueia a entrega final. Telegram usa apenas a diretiva MEDIA e a conversa autenticada descrita em TOOLS.md, após revisão.
