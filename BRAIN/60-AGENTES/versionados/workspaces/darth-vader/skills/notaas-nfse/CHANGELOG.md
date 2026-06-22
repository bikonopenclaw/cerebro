# 📝 CHANGELOG - NOTAAS NFSE SKILL

Todas as mudanças significativas neste projeto.

---

## [2.0.0] - 2026-06-12

### ✨ **NOVIDADES**

- **Setup Interativo** (`scripts/setup.py`)
  - Coleta dados da empresa via CLI
  - Validação em tempo real
  - Cria configuração automaticamente

- **Configuração Portátil** (`core/config.py`)
  - Lê de `config/empresa.json` ou `.env`
  - Suporte a múltiplas empresas
  - Validação automática

- **Scripts de Implantação**
  - `instalar.sh` - Instalação automática
  - `empacotar.sh` - Cria pacote ZIP limpo
  - Remove dados sensíveis automaticamente

- **Documentação Expandida**
  - `IMPLANTACAO.md` - Guia completo de implantação
  - `BOAS_VINDAS.md` - Primeiros passos
  - `PACOTE_LEIA_ME.md` - Resumo do pacote
  - `README.md` - Atualizado para versão portátil

### 🔧 **MUDANÇAS**

- **Removido:** Dependência de certificado local
  - Certificado agora fica na plataforma Notaas
  - Simplifica implantação

- **Removido:** Dados hardcoded da Marques Cap
  - Agora genérico para qualquer empresa
  - Configuração via setup

- **Alterado:** Estrutura de configuração
  - Antes: `.env` manual
  - Agora: `setup.py` interativo + `config/empresa.json`

### 📦 **NOVOS ARQUIVOS**

```
scripts/
  ├── setup.py              # NOVO: Setup interativo
  └── cadastrar_cliente.py  # NOVO: Cadastro de clientes

core/
  └── config.py             # NOVO: Gerencia configuração

instalar.sh                 # NOVO: Script de instalação
empacotar.sh                # NOVO: Criar pacote ZIP

IMPLANTACAO.md              # NOVO: Guia de implantação
BOAS_VINDAS.md              # NOVO: Primeiros passos
PACOTE_LEIA_ME.md           # NOVO: Resumo do pacote
```

### 🐛 **CORREÇÕES**

- Validação de CNPJ no setup
- Fallback para variáveis de ambiente
- Paths relativos para portabilidade

---

## [1.0.0] - 2026-04-24

### ✨ **PRIMEIRA VERSÃO**

- **Emissão Individual** - POST /emitir
- **Emissão em Lote** - POST /emitir/batch
- **Cancelamento** - POST /cancelar
- **Consulta Status** - GET /invoices/{id}/status
- **Download PDF/XML** - CDN Notaas

### 📁 **ESTRUTURA INICIAL**

```
core/
  ├── client.py             # API client (500 linhas)
  └── emitter.py            # Lógica de emissão

scripts/
  ├── emitir_nota.py
  ├── emitir_lote.py
  └── cancelar_nota.py

examples/
  ├── exemplo_01_individual.py
  └── exemplo_02_lote.py
```

### 🎯 **FUNCIONALIDADES**

- ✅ Emissão individual e em lote
- ✅ Retry automático (backoff exponencial)
- ✅ Validação de payload
- ✅ Logging completo
- ✅ Templates de e-mail

### 📝 **DOCUMENTAÇÃO**

- `SKILL.md` - Especificação completa
- `README.md` - Guia de uso
- `CHANGELOG.md` - Histórico

---

## 📊 RESUMO DAS VERSÕES

| Versão | Data | Foco | Status |
|--------|------|------|--------|
| **2.0.0** | 2026-06-12 | Portabilidade | ✅ Produção |
| **1.0.0** | 2026-04-24 | Funcionalidade | ✅ Produção (Marques Cap) |

---

## 🎯 PRÓXIMAS VERSÕES (BACKLOG)

### [2.1.0] - Em Planejamento

- [ ] Webhooks para notificações automáticas
- [ ] Suporte a múltiplas empresas simultâneas
- [ ] Dashboard web simples
- [ ] Relatórios de emissões

### [2.2.0] - Em Planejamento

- [ ] Integração com BeeFormal
- [ ] Emissão automática por CSV do Drive
- [ ] Conciliação automática (PDF vs XML)

---

**Mantido por:** Claw D. Marques <clawmarquescap@gmail.com>
