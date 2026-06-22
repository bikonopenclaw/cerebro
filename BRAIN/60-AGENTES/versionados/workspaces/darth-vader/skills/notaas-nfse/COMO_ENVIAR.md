# 🎯 SKILL NOTAAS NFSE v2.0 - PRONTA PARA IMPLANTAÇÃO!

---

## ✅ **O QUE FOI CRIADO**

Skill **100% portátil e genérica** que funciona em QUALQUER instância OpenClaw com QUALQUER empresa!

### **Arquivos Criados/Atualizados**

| Arquivo | Descrição |
|---------|-----------|
| `SKILL.md` | Documentação completa (atualizado v2.0) |
| `README.md` | Guia de instalação rápida |
| `BOAS_VINDAS.md` | Primeiros passos (5 min) |
| `IMPLANTACAO.md` | Guia de implantação detalhado |
| `PACOTE_LEIA_ME.md` | Resumo do pacote para envio |
| `CHANGELOG.md` | Histórico de versões |
| `scripts/setup.py` | ⭐ **SETUP INTERATIVO** (novo!) |
| `core/config.py` | ⭐ **CONFIG AUTOMÁTICA** (novo!) |
| `instalar.sh` | Script de instalação |
| `empacotar.sh` | Criar pacote ZIP |
| `.env.example` | Template de variáveis |

---

## 🚀 **COMO USAR EM OUTRA INSTÂNCIA**

### **Opção 1: Criar Pacote ZIP** (Recomendado)

```bash
# Na instância ATUAL (Marques Cap):
cd /mnt/data/openclaw/workspace/.openclaw/workspace/skills/notaas-nfse
./empacotar.sh

# Vai criar: /tmp/notaas-nfse.zip
# Enviar este arquivo para a nova instância
```

**Na NOVA instância:**
```bash
# Receber arquivo
unzip notaas-nfse.zip -d ~/.openclaw/workspace/skills/
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh

# Setup interativo vai pedir:
# 1. API Key da Notaas
# 2. Nome/CNPJ da empresa
# 3. Cidade/UF
# PRONTO!
```

### **Opção 2: ClawHub**

```bash
# Na instância ATUAL:
clawhub publish skills/notaas-nfse --name notaas-nfse --version 2.0.0

# Na NOVA instância:
clawhub install notaas-nfse
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

### **Opção 3: SCP/RSYNC**

```bash
# Copiar direto via rede:
rsync -avz --exclude 'config/*' --exclude 'data/*' --exclude '.env' \
  /mnt/data/openclaw/workspace/.openclaw/workspace/skills/notaas-nfse \
  usuario@nova-instancia:~/.openclaw/workspace/skills/

# Na nova instância:
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

---

## 📋 **O QUE A NOVA INSTÂNCIA PRECISA TER**

| Item | Obrigatório? | Observação |
|------|--------------|------------|
| **OpenClaw instalado** | ✅ | Qualquer instância |
| **Python 3.8+** | ✅ | Já vem no OpenClaw |
| **Conta na Notaas** | ✅ | platform.notaas.com.br |
| **API Key** | ✅ | Gerar na plataforma |
| **Certificado A1** | ✅ | Cadastrado na Notaas |
| **CNPJ da Empresa** | ✅ | Para configuração |

---

## 🎁 **DIFERENCIAIS DA VERSÃO 2.0**

### **Antes (v1.0 - Marques Cap)**
- ❌ Dados hardcoded
- ❌ Certificado local
- ❌ Configuração manual
- ❌ 1 empresa apenas

### **Agora (v2.0 - Portátil)**
- ✅ Setup interativo
- ✅ Certificado na Notaas
- ✅ Configuração automática
- ✅ Multi-empresas
- ✅ Genérica

---

## 📦 **COMO ENVIAR PARA O CLIENTE**

### **Pacote Mínimo para Envio**

1. **ZIP da Skill** (`notaas-nfse.zip`)
2. **Arquivo `PACOTE_LEIA_ME.md`** (instruções)
3. **Arquivo `BOAS_VINDAS.md`** (primeiros passos)

### **Instruções para o Cliente**

```
Olá!

Segue a skill NOTAAS NFSE v2.0 para emissão automática de NFS-e.

INSTALAÇÃO RÁPIDA:
1. unzip notaas-nfse.zip -d ~/.openclaw/workspace/skills/
2. cd ~/.openclaw/workspace/skills/notaas-nfse
3. ./instalar.sh
4. Preencher setup (API Key, CNPJ, cidade)
5. PRONTO!

TEMPO ESTIMADO: 15 minutos

DÚVIDAS? Leia: PACOTE_LEIA_ME.md
```

---

## 🧪 **TESTES QUE FIZEMOS**

Esta skill já foi testada em produção:

- ✅ **7+ NFS-e emitidas** (Marques Cap)
- ✅ **Clientes reais** (ACEMES, Donna Madeiras, etc.)
- ✅ **PDF + XML** baixando
- ✅ **E-mails** enviando
- ✅ **Retry de PDF** (15 min) funcionando
- ✅ **Lotes** de 4 notas simultâneas

---

## 📞 **SUPORTE**

**Criado por:** Claw D. Marques - Marques Cap  
**Email:** clawmarquescap@gmail.com  
**Telegram:** Grupo OpenClaw

**Documentação incluída:**
- `SKILL.md` - Técnica completa
- `README.md` - Instalação
- `BOAS_VINDAS.md` - Primeiros passos
- `IMPLANTACAO.md` - Implantação
- `PACOTE_LEIA_ME.md` - Resumo

---

## 🎉 **PRONTO!**

**A skill está 100% pronta para ser implantada em qualquer instância!**

Só escolher o método de envio (ZIP, ClawHub, SCP) e mandar! 🚀

---

*Gerado em 2026-06-12 por Claw D. Marques*
