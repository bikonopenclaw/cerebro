---
name: notaas-nfse
description: Emitir, consultar, baixar e cancelar NFS-e via API Notaas com guardrails de dry-run e confirmação explícita para operações fiscais reais. Use para tarefas de nota fiscal de serviço, integração Notaas, emissão em lote, consulta de status e download de PDF/XML de NFS-e.
---

# 🧠 NOTAAS NFSE - Skill de Emissão de Notas Fiscais de Serviço

> **Versão:** 2.0.0 (Portável)  
> **Criado:** 2026-04-24  
> **Atualizado:** 2026-06-12  
> **Status:** ✅ Produção Ready  
> **Autor:** Claw D. Marques  
> **Licença:** Proprietário

---

## 🎯 PROPÓSITO

Skill **100% portátil e genérica** para emissão de NFS-e via API Notaas. Funciona em **qualquer instância OpenClaw** com qualquer empresa.

**Para quem é:**
- 🤖 **Qualquer agente** em qualquer instância OpenClaw
- 👨‍💼 **Qualquer empresa** com conta na Notaas
- 🏢 **Escritórios de contabilidade** multi-empresa

**Objetivo:** Automatizar emissão de NFS-e com configuração mínima no primeiro uso.

---

## 📋 FUNCIONALIDADES

| Funcionalidade | Status | Descrição |
|----------------|--------|-----------|
| **Configuração Automática** | ✅ | Setup interativo no primeiro uso |
| **Multi-Empresa** | ✅ | Suporta múltiplas configurações |
| **Emissão Individual** | ✅ | POST /emitir - 1 nota por vez |
| **Emissão em Lote** | ✅ | POST /emitir/batch - até 100 notas |
| **Cancelamento** | ✅ | POST /cancelar - cancela nota emitida |
| **Consulta Status** | ✅ | GET /invoices/{id}/status |
| **Download PDF/XML** | ✅ | Baixa arquivos da NFS-e |
| **Retry Automático** | ✅ | Backoff exponencial em erros |
| **Webhooks** | ✅ | Suporte a notificações automáticas |

---

## 🚀 INSTALAÇÃO (QUALQUER INSTÂNCIA)

### **Passo 1: Instalar a Skill**

```bash
# Via ClawHub (recomendado)
clawhub install notaas-nfse

# OU cópia direta
cp -r /caminho/skills/notaas-nfse ~/.openclaw/workspace/skills/
```

### **Passo 2: Rodar Setup Inicial**

```bash
cd ~/.openclaw/workspace/skills/notaas-nfse
python3 scripts/setup.py
```

O setup vai pedir:
1. **API Key da Notaas** (`ntaas_xxxxxx`)
2. **Nome da Empresa** (razão social)
3. **CNPJ da Empresa** (00.000.000/0001-00)
4. **Inscrição Municipal** (opcional)
5. **Cidade/UF** (para código IBGE automático)

### **Passo 3: Cadastrar Clientes**

```bash
python3 scripts/cadastrar_cliente.py
```

Ou editar manualmente `data/clientes.json`.

---

## 🔧 CONFIGURAÇÃO

### **Arquivo de Configuração**

Após o setup, será criado:
```
config/empresa.json
```

Conteúdo:
```json
{
  "empresa": {
    "nome": "SUA EMPRESA LTDA",
    "cnpj": "00.000.000/0001-00",
    "inscricao_municipal": "123456",
    "cidade_ibge": "3205307",
    "cidade_uf": "Vitória/ES"
  },
  "notaas": {
    "api_key": "ntaas_xxxxxx",
    "base_url": "https://platform.notaas.com.br/api/v1"
  }
}
```

### **Variáveis de Ambiente (.env)**

```bash
NOTAAS_API_KEY=ntaas_xxxxxx
NOTAAS_BASE_URL=https://platform.notaas.com.br/api/v1
EMPRESA_CNPJ=00.000.000/0001-00
```

---

## ✅ PADRÃO BIKON PARA DADOS DO TOMADOR

Para emissões da Bikon, a NFS-e deve usar **todos os dados disponíveis no cadastro mestre do cliente**.

Regra obrigatória antes de emitir:

- Enviar `tomador.cpf` ou `tomador.cnpj`, conforme o tamanho do documento.
- Enviar `tomador.nome` com a razão social/nome do cadastro.
- Enviar `tomador.email` quando existir e-mail financeiro.
- Enviar `tomador.endereco` sempre que houver endereço no cadastro, com:
  - `logradouro`
  - `numero`
  - `complemento`, se houver
  - `bairro`
  - `cidade`
  - `uf`
  - `cep`, preferencialmente sem máscara
- Não emitir lote usando só documento, nome e e-mail quando o cadastro tiver endereço.
- Se endereço estiver ausente ou ambíguo, marcar como pendência antes da emissão.

Histórico: em 2026-06-19, um lote de homologação saiu sem endereço porque o script descartava `tomador.endereco`. Correção aplicada em `core/client.py` e `scripts/emitir_lote.py` para preservar endereço quando disponível.

Decisão Bikon de 2026-06-22: manter a configuração sem inscrição municipal. A ausência de IM não deve bloquear emissão da Bikon enquanto a API Notaas aceitar sem esse campo. Não marcar IM ausente como pendência crítica; validar tomador completo, serviço, valor, competência e autorização explícita para emissão real.

## 📧 PADRÃO BIKON PARA E-MAIL AO CLIENTE

Após NFS-e emitida e PDF/XML baixados, preparar automaticamente o e-mail para o financeiro do cliente.

Configuração: `config/email.json`.
Script: `scripts/preparar_email_cliente.py`.
Agrupador de e-mails por cliente em lote: `scripts/preparar_emails_lote_clientes.py`.

Regras obrigatórias:

- Buscar destinatários no cadastro financeiro `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_emails_financeiro.csv`.
- Também aceitar `tomador.email` ou `email.to` no job quando informado.
- Anexar DANFSe PDF, XML da NFS-e e boleto PDF quando houver cobrança por boleto.
- Gerar rascunho `.eml`, metadados `.json` e checklist `checklist-envio-nfse.md/json` por pacote.
- Usar o template HTML padrão Bikon em `templates/email_nfse_bikon.html` para toda emissão de NFS-e.
- Gerar e-mail multipart com texto simples + HTML, para compatibilidade com clientes de e-mail.
- Envio real para cliente externo exige checklist sem bloqueios, autorização explícita do Hebert e `job.email.aprovado_por_hebert=true`.
- Se faltar e-mail financeiro, bloquear o envio e marcar pendência cadastral. Em `modo` iniciado por `teste`, não buscar cadastro automaticamente quando `email.to` ou `--to` estiver definido.
- Quando houver duas ou mais NFS-e para o mesmo ID/documento de cliente na mesma rodada, agrupar tudo em um único e-mail para esse cliente.
- O e-mail agrupado deve listar as notas no corpo e anexar todos os PDFs/XMLs de NFS-e e todos os boletos existentes.
- O checklist deve bloquear envio externo quando faltar PDF da NFS-e, XML da NFS-e, boleto PDF quando houver boleto indicado, destinatário final ou aprovação do Hebert.
- Não enviar boleto, NFS-e, remessa ou qualquer comunicação externa sem aprovação explícita.

---

## 📖 USO

### **Emissão Individual (CLI)**

Use `--documento` para CPF ou CNPJ. A skill detecta automaticamente:
- 11 dígitos: envia `tomador.cpf`
- 14 dígitos: envia `tomador.cnpj`

```bash
python3 scripts/emitir_nota.py --confirmar-emissao \
  --documento "00.000.000/0001-00" \
  --nome "Cliente LTDA" \
  --email "financeiro@cliente.com" \
  --codigo "010701" \
  --valor 1000.00 \
  --competencia "2026-06-13" \
  --descricao "Assessoria Contábil"
```

Para pessoa física, use CPF no mesmo campo:

```bash
python3 scripts/emitir_nota.py --dry-run \
  --documento "10301594759" \
  --nome "Hebert Dummer Mattedi" \
  --email "hebertmattedi@gmail.com" \
  --codigo "010701" \
  --valor 1.00 \
  --aliquota 5 \
  --competencia "2026-06-13" \
  --descricao "serviço de infraestrutura de rede"
```

### **Emissão em Lote (CLI)**

```bash
python3 scripts/emitir_lote.py \
  --arquivo clientes_lote.csv
```

### **Via Python (API)**

```python
from skills.notaas_nfse.core import NotaasClient

client = NotaasClient()  # Lê config automaticamente

nota = client.emitir({
    'tomador_cnpj': '00.000.000/0001-00',
    'valor': 1000.00,
    'descricao': 'Serviços',
    'competencia': '01/2026'
})

print(f"Nota emitida: {nota['numero']}")
```

### **Via Agente OpenClaw**

```python
# Em qualquer agente
from skills.notaas_nfse import emitir_nfse

result = emitir_nfse(
    cliente="Empresa X",
    valor=1000.00,
    competencia="01/2026",
    descricao="Serviços"
)
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
notaas-nfse/
├── SKILL.md              # Esta documentação
├── README.md             # Guia rápido
├── setup.py              # Setup inicial (INTERATIVO)
├── requirements.txt      # Dependências
├── .env.example          # Template .env
├── config/
│   └── empresa.json      # Config da empresa (criado no setup)
├── core/
│   ├── __init__.py
│   ├── client.py         # API client
│   ├── config.py         # Gerencia configuração
│   └── emitter.py        # Lógica de emissão
├── scripts/
│   ├── setup.py          # Setup interativo
│   ├── emitir_nota.py    # Emissão individual
│   ├── emitir_lote.py    # Emissão em lote
│   ├── cancelar_nota.py  # Cancelamento
│   ├── cadastrar_cliente.py  # Cadastro de clientes
│   └── consultar_status.py   # Consulta status
├── data/
│   ├── clientes.json     # Base de clientes
│   └── historico.json    # Histórico de emissões
├── templates/
│   ├── payload.json      # Template de payload
│   └── email.html        # Template de e-mail
└── examples/
    ├── individual.py     # Exemplo individual
    └── lote.py           # Exemplo lote
```

---

## 🔐 SEGURANÇA

- ✅ API Key armazenada em `.env` (não versionado)
- ✅ Certificado na plataforma Notaas (não local)
- ✅ Config da empresa em `config/empresa.json` (não versionado)
- ✅ Logs sem dados sensíveis

---

## 🆘 SUPORTE

| Problema | Solução |
|----------|---------|
| API Key inválida | Verifique em platform.notaas.com.br |
| Cliente não encontrado | Rode `cadastrar_cliente.py` |
| Erro na emissão | Verifique logs em `logs/` |
| PDF não disponível | Aguarde 15 min (retry automático) |

---

## 📝 CHANGELOG

### 2.0.0 (2026-06-12)
- ✅ Setup interativo para configuração inicial
- ✅ Configuração genérica (qualquer empresa)
- ✅ Multi-empresa suportada
- ✅ Removida dependência de certificado local

### 1.0.0 (2026-04-24)
- ✅ Primeira versão (Marques Cap)
- ✅ Emissão individual e em lote
- ✅ Download PDF/XML
- ✅ Cancelamento

---

**Skill pronta para usar em qualquer instância!** 🚀
