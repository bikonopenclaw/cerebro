#!/usr/bin/env python3

# Local skill path and vendored dependencies
import sys as _sys
from pathlib import Path as _Path
_skill_root = _Path(__file__).resolve().parent.parent
_vendor = _skill_root / 'vendor'
for _p in (_skill_root, _vendor):
    if _p.exists() and str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

"""
Módulo de Configuração - Gerencia configuração da skill

Lê configuração de config/empresa.json ou variáveis de ambiente.
Suporta múltiplas empresas e configuração dinâmica.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

class Config:
    """Gerencia configuração da skill Notaas NFSe"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa configuração.
        
        Args:
            config_path: Caminho opcional para arquivo de config.
                        Se None, usa padrão (config/empresa.json)
        """
        self._config = None
        self._config_path = config_path
        
        # Tentar carregar configuração
        self._carregar_config()
    
    def _carregar_config(self):
        """Carrega configuração do arquivo ou variáveis de ambiente"""
        
        # Tentar arquivo de configuração
        if self._config_path:
            path = Path(self._config_path)
        else:
            # Caminho padrão: config/empresa.json relativo à skill
            skill_dir = Path(__file__).parent.parent
            path = skill_dir / 'config' / 'empresa.json'
        
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            return
        
        # Fallback: variáveis de ambiente
        self._config = {
            'empresa': {
                'nome': os.getenv('EMPRESA_NOME', ''),
                'cnpj': os.getenv('EMPRESA_CNPJ', ''),
                'inscricao_municipal': os.getenv('EMPRESA_IM', ''),
                'cidade': os.getenv('EMPRESA_CIDADE', ''),
                'uf': os.getenv('EMPRESA_UF', ''),
                'ibge': os.getenv('EMPRESA_IBGE', '')
            },
            'notaas': {
                'api_key': os.getenv('NOTAAS_API_KEY', ''),
                'base_url': os.getenv('NOTAAS_BASE_URL', 
                            'https://platform.notaas.com.br/api/v1')
            }
        }
    
    @property
    def empresa(self) -> Dict:
        """Dados da empresa"""
        return self._config.get('empresa', {})
    
    @property
    def notaas(self) -> Dict:
        """Dados de acesso à Notaas"""
        return self._config.get('notaas', {})
    
    @property
    def api_key(self) -> str:
        """API Key da Notaas"""
        return self.notaas.get('api_key', '')
    
    @property
    def base_url(self) -> str:
        """Base URL da API"""
        return self.notaas.get('base_url', 'https://platform.notaas.com.br/api/v1')
    
    @property
    def cnpj(self) -> str:
        """CNPJ da empresa (apenas números)"""
        cnpj = self.empresa.get('cnpj', '')
        return ''.join(filter(str.isdigit, cnpj))
    
    @property
    def inscricao_municipal(self) -> str:
        """Inscrição Municipal"""
        return self.empresa.get('inscricao_municipal', '')
    
    @property
    def cidade_ibge(self) -> str:
        """Código IBGE da cidade"""
        return self.empresa.get('ibge', '')
    
    @property
    def cidade_uf(self) -> str:
        """Cidade/UF"""
        cidade = self.empresa.get('cidade', '')
        uf = self.empresa.get('uf', '')
        return f"{cidade}/{uf}" if cidade and uf else ''
    
    def validar(self) -> tuple[bool, list]:
        """
        Valida configuração.
        
        Returns:
            tuple: (valido, lista_de_erros)
        """
        erros = []
        
        # Validar empresa
        if not self.empresa.get('nome'):
            erros.append("Nome da empresa não configurado")
        
        if not self.empresa.get('cnpj'):
            erros.append("CNPJ da empresa não configurado")
        elif len(self.cnpj) != 14:
            erros.append("CNPJ inválido (deve ter 14 dígitos)")
        
        # Validar Notaas
        if not self.api_key:
            erros.append("API Key da Notaas não configurada")
        elif not self.api_key.startswith('ntaas_'):
            erros.append("API Key inválida (deve começar com 'ntaas_')")
        
        return (len(erros) == 0, erros)
    
    def resumo(self) -> str:
        """Retorna resumo formatado da configuração"""
        linhas = [
            "=" * 50,
            "CONFIGURAÇÃO NOTAAS NFSE",
            "=" * 50,
            "",
            "EMPRESA:",
            f"  • Nome: {self.empresa.get('nome', 'N/A')}",
            f"  • CNPJ: {self.empresa.get('cnpj', 'N/A')}",
            f"  • IM: {self.empresa.get('inscricao_municipal', 'N/A')}",
            f"  • Cidade: {self.cidade_uf}",
            "",
            "NOTAAS:",
            f"  • API Key: {self.api_key[:10]}...{self.api_key[-4:] if len(self.api_key) > 4 else 'N/A'}",
            f"  • Base URL: {self.base_url}",
            "",
        ]
        
        valido, erros = self.validar()
        if valido:
            linhas.append("✅ Configuração válida!")
        else:
            linhas.append("❌ Configuração inválida:")
            for erro in erros:
                linhas.append(f"   • {erro}")
        
        return "\n".join(linhas)
    
    def salvar(self, path: Optional[str] = None):
        """
        Salva configuração em arquivo.
        
        Args:
            path: Caminho opcional. Se None, usa padrão.
        """
        if not path:
            skill_dir = Path(__file__).parent.parent
            config_dir = skill_dir / 'config'
            config_dir.mkdir(exist_ok=True)
            path = config_dir / 'empresa.json'
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)


# Singleton para configuração global
_config_global: Optional[Config] = None

def get_config() -> Config:
    """
    Obtém instância global de configuração.
    
    Returns:
        Config: Instância de configuração
    """
    global _config_global
    if _config_global is None:
        _config_global = Config()
    return _config_global

def reset_config():
    """Reseta configuração global (útil para testes)"""
    global _config_global
    _config_global = None


# Exemplo de uso
if __name__ == '__main__':
    config = get_config()
    print(config.resumo())
