# Status do projeto — SERPRO Integra Contador / Parcelamentos

## 2026-06-18 — Stand by

Projeto pausado por decisão do Hebert.

Motivo:
- Para autenticação completa no SERPRO Integra Contador é necessário usar certificado digital A1/e-CNPJ.
- Hebert não se sente confortável em entregar ou armazenar o certificado no servidor/OpenClaw.
- Decisão correta do ponto de vista de segurança: certificado A1 é credencial crítica da empresa.

Estado atual:
- Contrato SERPRO Integra Contador 540190 recebido e analisado.
- Credenciais Basic recebidas foram salvas no cofre local, mas passaram pelo Telegram e devem ser regeneradas antes de produção.
- API Reference, Quick Start e serviços PARCSN foram documentados.
- Nenhuma emissão de DAS foi realizada.
- Nenhuma chamada de emissão real foi habilitada.
- `SERPRO_ALLOW_EMITIR=false` deve permanecer.

Próxima retomada só quando Hebert definir modelo seguro, opções possíveis:
1. Rodar autenticação local no computador do Hebert e usar tokens temporários.
2. Usar ambiente controlado/cofre dedicado para certificado A1.
3. Manter processo manual assistido via portal.
4. Validar com contador/SERPRO alternativa com procuração/token sem expor A1.

Regra até retomar:
- Não pedir certificado.
- Não tentar autenticação SAPI.
- Não chamar `/Emitir`.
- Não gerar guia real.
