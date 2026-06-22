# 🚀 NOTAAS NFSE - Guia de Instalação Rápida

> Skill portátil para emissão de NFS-e em qualquer instância OpenClaw

---

## ⚡ INSTALAÇÃO EM 3 PASSOS

### **Passo 1: Copiar/Instalar a Skill**

```bash
# Opção A: ClawHub (recomendado)
clawhub install notaas-nfse

# Opção B: Cópia direta
cp -r /caminho/notaas-nfse ~/.openclaw/workspace/skills/
```

### **Passo 2: Rodar Setup**

```bash
cd ~/.openclaw/workspace/skills/notaas-nfse
python3 scripts/setup.py
```

O setup vai pedir:
- ✅ API Key da Notaas
- ✅ Nome/CNPJ da sua empresa
- ✅ Cidade/UF

### **Passo 3: Pronto!**

```bash
# Testar emissão
python3 scripts/emitir_nota.py --dry-run --cnpj 00.000.000/0001-00 --nome TESTE --email teste@exemplo.com --codigo 171901 --descricao 'Teste' --valor 100

# Cadastrar cliente
python3 scripts/cadastrar_cliente.py
```

---

## 📋 PRÉ-REQUISITOS

1. **Conta na Notaas** - https://platform.notaas.com.br
2. **API Key** - Gerar em Configurações → API
3. **Python 3.8+** - Já instalado no OpenClaw
4. **Certificado A1** - Cadastrado na plataforma Notaas

---

## 🔧 CONFIGURAÇÃO MANUAL (OPCIONAL)

Se preferir configurar manualmente:

### **1. Criar .env**

```bash
cd ~/.openclaw/workspace/skills/notaas-nfse
cp .env.example .env
```

Editar `.env`:
```env
NOTAAS_API_KEY=ntaas_xxxxxx
NOTAAS_BASE_URL=https://platform.notaas.com.br/api/v1
EMPRESA_CNPJ=00000000000100
EMPRESA_NOME=SUA EMPRESA LTDA
```

### **2. Criar config/empresa.json**

```json
{
  "empresa": {
    "nome": "SUA EMPRESA LTDA",
    "cnpj": "00.000.000/0001-00",
    "inscricao_municipal": "123456",
    "cidade": "SUA CIDADE",
    "uf": "ES",
    "ibge": "3205307"
  },
  "notaas": {
    "api_key": "ntaas_xxxxxx",
    "base_url": "https://platform.notaas.com.br/api/v1"
  }
}
```

---

## 📖 USO BÁSICO

### **Emitir NFS-e Individual**

```bash
python3 scripts/emitir_nota.py --confirmar-emissao \
  --cnpj "00.000.000/0001-00" \
  --valor 1000.00 \
  --competencia "01/2026" \
  --descricao "Assessoria Contábil"
```

### **Emitir em Lote**

Criar CSV:
```csv
cnpj,valor,competencia,descricao
00.000.000/0001-00,1000,01/2026,Servicos
11.111.111/0001-11,2000,01/2026,Servicos
```

Emitir:
```bash
python3 scripts/emitir_lote.py --arquivo lote.csv
```

### **Cancelar NFS-e**

```bash
python3 scripts/cancelar_nota.py --confirmar-cancelamento \
  --invoice-id "uuid-da-nota" \
  --motivo "Erro na emissao"
```

---

## 🐍 USO VIA PYTHON

```python
from core.config import get_config
from core.client import NotaasClient

# Carregar configuração
config = get_config()

# Validar
valido, erros = config.validar()
if not valido:
    print("Erros:", erros)
    exit(1)

# Criar client
client = NotaasClient(
    api_key=config.api_key,
    base_url=config.base_url
)

# Emitir nota
nota = client.emitir({
    'tomador_cnpj': '00.000.000/0001-00',
    'tomador_nome': 'Cliente LTDA',
    'valor': 1000.00,
    'descricao': 'Serviços',
    'competencia': '01/2026'
})

print(f"Nota emitida: {nota['numero']}")
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
notaas-nfse/
├── scripts/
│   ├── setup.py              ← PRIMEIRO USO
│   ├── emitir_nota.py
│   ├── emitir_lote.py
│   └── cancelar_nota.py
├── core/
│   ├── client.py             ← API client
│   └── config.py             ← Configuração
├── data/
│   ├── clientes.json         ← Seus clientes
│   └── historico.json        ← Histórico
├── config/
│   └── empresa.json          ← Config (criado no setup)
└── .env                      ← Variáveis (criado no setup)
```

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### **Erro: "API Key inválida"**

1. Verifique em https://platform.notaas.com.br
2. Gere nova chave em Configurações → API
3. Rode `setup.py` novamente

### **Erro: "CNPJ não encontrado"**

1. Cadastre o cliente: `python3 scripts/cadastrar_cliente.py`
2. Ou edite `data/clientes.json` manualmente

### **Erro: "PDF não disponível"**

- Aguarde 15 minutos (PDF demora para gerar)
- XML está disponível imediatamente
- Script faz retry automático

---

## 📞 SUPORTE

- **Docs:** `cat SKILL.md`
- **Exemplos:** `ls examples/`
- **Logs:** `ls logs/`

---

**Instalação completa em 5 minutos!** ⚡
