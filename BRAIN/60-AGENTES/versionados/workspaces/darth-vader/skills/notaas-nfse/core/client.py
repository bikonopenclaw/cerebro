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
Notaas NFSe Client - Cliente para API Notaas

Provides a clean interface to the Notaas API for NFS-e operations.
"""

import os
import re
import json
import logging
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configurar logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class NFSeResult:
    """Resultado de operação NFSe"""
    success: bool
    invoice_id: Optional[str] = None
    chNFSe: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class NotaasClient:
    """
    Cliente para API Notaas v1
    
    Fornece interface limpa para operações de NFS-e:
    - Emissão
    - Cancelamento
    - Consulta de status
    - Download de arquivos
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        env: str = "homologation"
    ):
        """
        Inicializa o cliente Notaas.
        
        Args:
            api_key: API Key da Notaas (obtido de env ou parâmetro)
            base_url: URL base da API
            env: Ambiente (homologation ou production)
        """
        self.api_key = api_key or os.getenv('NOTAAS_API_KEY')
        if not self.api_key:
            raise ValueError("API Key não configurada")
        
        self.base_url = base_url or os.getenv('NOTAAS_BASE_URL', 
                      'https://platform.notaas.com.br/api/v1')
        self.env = env
        
        # Configurar session para reutilização de conexões
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        })
        
        logger.info(f"Cliente Notaas inicializado - Ambiente: {env}")
    
    @classmethod
    def from_env(cls) -> 'NotaasClient':
        """Cria cliente a partir de variáveis de ambiente"""
        return cls()
    
    # =========================================================================
    # EMISSÃO
    # =========================================================================
    
    def emitir(self, payload: Dict[str, Any]) -> NFSeResult:
        """
        Emite uma NFS-e individual.
        
        Args:
            payload: Payload completo de emissão
            
        Returns:
            NFSeResult com status da emissão
        """
        url = f"{self.base_url}/emitir"
        
        logger.info(f"Enviando emissão para: {url}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 202:
                data = response.json()
                logger.info(f"Emissão aceita - Invoice ID: {data.get('invoiceId')}")
                
                return NFSeResult(
                    success=True,
                    invoice_id=data.get('invoiceId'),
                    status=data.get('status'),
                    data=data
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return NFSeResult(success=False, error=error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout na requisição de emissão"
            logger.error(error_msg)
            return NFSeResult(success=False, error=error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro de conexão: {str(e)}"
            logger.error(error_msg)
            return NFSeResult(success=False, error=error_msg)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=3, max=27),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def emitir_com_retry(self, payload: Dict[str, Any]) -> NFSeResult:
        """Emite com retry automático em caso de erro"""
        return self.emitir(payload)
    
    def emitir_lote(self, items: List[Dict[str, Any]]) -> NFSeResult:
        """
        Emite múltiplas NFS-e em batch.
        
        Args:
            items: Lista de payloads individuais
            
        Returns:
            NFSeResult com status do batch
        """
        if not items:
            return NFSeResult(success=False, error="Lista de itens vazia")
        
        payload = {"items": items}
        url = f"{self.base_url}/emitir/batch"
        
        logger.info(f"Enviando batch de {len(items)} notas")
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 202:
                data = response.json()
                logger.info(f"Batch aceito - Batch ID: {data.get('batchId')}")
                
                return NFSeResult(
                    success=True,
                    invoice_id=data.get('batchId'),  # Usando invoice_id para batchId
                    status=data.get('status'),
                    data=data
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return NFSeResult(success=False, error=error_msg)
                
        except Exception as e:
            error_msg = f"Erro no batch: {str(e)}"
            logger.error(error_msg)
            return NFSeResult(success=False, error=error_msg)
    
    # =========================================================================
    # CONSULTA DE STATUS
    # =========================================================================
    
    def consultar_status(self, invoice_id: str) -> NFSeResult:
        """
        Consulta status de uma NFS-e.
        
        Args:
            invoice_id: ID da nota (UUID)
            
        Returns:
            NFSeResult com status completo
        """
        url = f"{self.base_url}/invoices/{invoice_id}/status"
        
        logger.debug(f"Consultando status de: {invoice_id}")
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Status: {data.get('status')}")
                
                return NFSeResult(
                    success=True,
                    invoice_id=invoice_id,
                    status=data.get('status'),
                    chNFSe=data.get('chNFSe'),
                    data=data
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return NFSeResult(success=False, error=error_msg)
                
        except Exception as e:
            error_msg = f"Erro na consulta: {str(e)}"
            logger.error(error_msg)
            return NFSeResult(success=False, error=error_msg)
    
    def consultar_batch_status(self, batch_id: str) -> NFSeResult:
        """
        Consulta status de um batch.
        
        Args:
            batch_id: ID do batch
            
        Returns:
            NFSeResult com status do batch
        """
        url = f"{self.base_url}/invoices/batch/{batch_id}/status"
        
        logger.debug(f"Consultando batch: {batch_id}")
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Batch {batch_id}: {data.get('status')}")
                
                return NFSeResult(
                    success=True,
                    invoice_id=batch_id,
                    status=data.get('status'),
                    data=data
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return NFSeResult(success=False, error=error_msg)
                
        except Exception as e:
            error_msg = f"Erro na consulta do batch: {str(e)}"
            logger.error(error_msg)
            return NFSeResult(success=False, error=error_msg)
    
    # =========================================================================
    # CANCELAMENTO
    # =========================================================================
    
    def cancelar(self, invoice_id: str, motivo: str) -> NFSeResult:
        """
        Cancela uma NFS-e.
        
        Args:
            invoice_id: ID da nota (UUID)
            motivo: Justificativa do cancelamento
            
        Returns:
            NFSeResult com status do cancelamento
        """
        url = f"{self.base_url}/cancelar"
        
        payload = {
            "invoiceId": invoice_id,
            "motivo": motivo
        }
        
        logger.info(f"Solicitando cancelamento: {invoice_id}")
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 202:
                data = response.json()
                logger.info(f"Cancelamento solicitado - Status: {data.get('status')}")
                
                return NFSeResult(
                    success=True,
                    invoice_id=invoice_id,
                    status=data.get('status'),
                    data=data
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return NFSeResult(success=False, error=error_msg)
                
        except Exception as e:
            error_msg = f"Erro no cancelamento: {str(e)}"
            logger.error(error_msg)
            return NFSeResult(success=False, error=error_msg)
    
    # =========================================================================
    # DOWNLOAD
    # =========================================================================
    
    def baixar_pdf(self, invoice_id: str) -> Optional[bytes]:
        """
        Baixa PDF da NFS-e.
        
        Args:
            invoice_id: ID da nota (UUID)
            
        Returns:
            Conteúdo binário do PDF ou None
        """
        url = f"{self.base_url}/invoices/{invoice_id}/pdf"
        
        logger.debug(f"Baixando PDF: {invoice_id}")
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"PDF baixado com sucesso - {len(response.content)} bytes")
                return response.content
            else:
                logger.error(f"Erro ao baixar PDF: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao baixar PDF: {str(e)}")
            return None
    
    def baixar_xml(self, invoice_id: str) -> Optional[bytes]:
        """
        Baixa XML da NFS-e.
        
        Args:
            invoice_id: ID da nota (UUID)
            
        Returns:
            Conteúdo binário do XML ou None
        """
        url = f"{self.base_url}/invoices/{invoice_id}/xml"
        
        logger.debug(f"Baixando XML: {invoice_id}")
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"XML baixado com sucesso - {len(response.content)} bytes")
                return response.content
            else:
                logger.error(f"Erro ao baixar XML: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao baixar XML: {str(e)}")
            return None
    
    def baixar_tudo(self, invoice_id: str, output_dir: str) -> Dict[str, bool]:
        """
        Baixa PDF e XML e salva em arquivo.
        
        Args:
            invoice_id: ID da nota
            output_dir: Diretório de saída
            
        Returns:
            Dict com sucesso de cada download
        """
        import os
        
        resultados = {}
        
        # Baixar PDF
        pdf = self.baixar_pdf(invoice_id)
        if pdf:
            pdf_path = os.path.join(output_dir, f"nfse_{invoice_id}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(pdf)
            resultados['pdf'] = True
            logger.info(f"PDF salvo em: {pdf_path}")
        else:
            resultados['pdf'] = False
        
        # Baixar XML
        xml = self.baixar_xml(invoice_id)
        if xml:
            xml_path = os.path.join(output_dir, f"nfse_{invoice_id}.xml")
            with open(xml_path, 'wb') as f:
                f.write(xml)
            resultados['xml'] = True
            logger.info(f"XML salvo em: {xml_path}")
        else:
            resultados['xml'] = False
        
        return resultados
    
    # =========================================================================
    # UTILITÁRIOS
    # =========================================================================
    
    def validar_payload(self, payload: Dict[str, Any]) -> List[str]:
        """
        Valida payload antes de enviar.
        
        Args:
            payload: Payload a validar
            
        Returns:
            Lista de erros (vazia se válido)
        """
        errors = []
        
        # Validar tomador
        if 'tomador' not in payload:
            errors.append("Campo 'tomador' obrigatório")
        else:
            tomador = payload['tomador']
            if 'cnpj' not in tomador and 'cpf' not in tomador:
                errors.append("tomador.cnpj ou tomador.cpf obrigatório")
            if 'cnpj' in tomador and len(only_digits(str(tomador['cnpj']))) != 14:
                errors.append("tomador.cnpj deve conter 14 dígitos")
            if 'cpf' in tomador and len(only_digits(str(tomador['cpf']))) != 11:
                errors.append("tomador.cpf deve conter 11 dígitos")
            if 'nome' not in tomador:
                errors.append("tomador.nome obrigatório")
        
        # Validar serviço
        if 'servico' not in payload:
            errors.append("Campo 'servico' obrigatório")
        else:
            servico = payload['servico']
            if 'codigo' not in servico:
                errors.append("servico.codigo obrigatório")
            if 'descricao' not in servico:
                errors.append("servico.descricao obrigatório")
        
        # Validar valores
        if 'valores' not in payload:
            errors.append("Campo 'valores' obrigatório")
        else:
            valores = payload['valores']
            if 'total' not in valores:
                errors.append("valores.total obrigatório")
            if 'aliquotaIss' not in valores:
                errors.append("valores.aliquotaIss obrigatório")
        
        return errors
    
    def close(self):
        """Fecha a session"""
        self.session.close()
        logger.info("Cliente Notaas encerrado")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# =========================================================================
# FUNÇÕES AUXILIARES
# =========================================================================

def only_digits(value: str) -> str:
    """Retorna apenas dígitos de CPF/CNPJ/documentos formatados."""
    return re.sub(r'\D', '', value or '')


def montar_tomador(documento: str, nome: str, email: str, endereco: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Monta tomador com cpf ou cnpj conforme tamanho do documento.

    - 11 dígitos: pessoa física, envia `cpf`
    - 14 dígitos: pessoa jurídica, envia `cnpj`
    - `endereco` é opcional, mas deve ser enviado quando disponível no cadastro.
    """
    digits = only_digits(documento)
    if len(digits) == 11:
        doc_field = 'cpf'
    elif len(digits) == 14:
        doc_field = 'cnpj'
    else:
        raise ValueError(
            f"Documento inválido: esperado CPF com 11 dígitos ou CNPJ com 14 dígitos. Recebido: {documento!r}"
        )

    tomador = {
        doc_field: digits,
        "nome": nome
    }
    if email:
        tomador["email"] = email
    if endereco:
        tomador["endereco"] = endereco
    return tomador


def criar_payload_individual(
    nome: str,
    email: str,
    codigo: str,
    descricao: str,
    valor: float,
    aliquota: float,
    competencia: str = "2026-04",
    cnpj: str = None,
    cpf: str = None,
    documento: str = None,
    endereco: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Cria payload para emissão individual.

    Args:
        nome: Nome do tomador
        email: Email do tomador
        codigo: Código LC 116
        descricao: Descrição do serviço
        valor: Valor total
        aliquota: Alíquota ISS
        competencia: Competência (YYYY-MM)
        cnpj: CNPJ do tomador, aceito por compatibilidade
        cpf: CPF do tomador
        documento: CPF ou CNPJ do tomador, detectado automaticamente

    Returns:
        Payload completo para emissão
    """
    doc = documento or cpf or cnpj
    return {
        "tomador": montar_tomador(doc, nome, email, endereco),
        "servico": {
            "codigo": codigo,
            "descricao": descricao
        },
        "valores": {
            "total": valor,
            "aliquotaIss": aliquota
        },
        "competencia": competencia
    }


def criar_payload_lote(clientes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Cria payload para emissão em lote.
    
    Args:
        clientes: Lista de clientes (cada um com tomador, servico, valores)
        
    Returns:
        Payload completo para batch
    """
    items = []
    for cliente in clientes:
        documento = cliente.get('documento') or cliente.get('cpf') or cliente.get('cnpj')
        items.append({
            "tomador": montar_tomador(documento, cliente['nome'], cliente.get('email', ''), cliente.get('endereco')),
            "servico": {
                "codigo": cliente['codigo'],
                "descricao": cliente['descricao']
            },
            "valores": {
                "total": cliente['valor'],
                "aliquotaIss": cliente.get('aliquota', 0)
            }
        })
    
    return {"items": items}
