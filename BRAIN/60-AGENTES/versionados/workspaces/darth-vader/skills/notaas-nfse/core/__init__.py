
# Local skill path and vendored dependencies
import sys as _sys
from pathlib import Path as _Path
_skill_root = _Path(__file__).resolve().parent.parent
_vendor = _skill_root / 'vendor'
for _p in (_skill_root, _vendor):
    if _p.exists() and str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

"""
Notaas NFSe - Skill de Emissão de NFS-e via API Notaas
"""

from .client import NotaasClient, NFSeResult, criar_payload_individual, criar_payload_lote, montar_tomador

__version__ = "1.0.0"
__all__ = [
    "NotaasClient",
    "NFSeResult",
    "criar_payload_individual",
    "criar_payload_lote",
    "montar_tomador"
]
