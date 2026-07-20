#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shutil, subprocess
from pathlib import Path
from runtime_lib import atomic_write_json, load_json, request_hash, utc_now, validate_approval

DISCOVERY = {"who_am_i", "account", "tool_list"}
TASK_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,200}$")

def load_contract(path: Path) -> dict:
    data = load_json(path)
    if not data.get("production_enabled"):
        raise ValueError("contrato Kling ainda não está habilitado")
    return data

def build_argv(request: dict, kling: str, contract_path: Path) -> list[str]:
    if request.get("tool") != "kling":
        raise ValueError("tool precisa ser kling")
    operation = request.get("operation")
    if operation in DISCOVERY:
        return [kling, operation]
    if operation == "query_tasks":
        task_id = request.get("parameters", {}).get("task_id", "")
        if not TASK_ID_RE.fullmatch(task_id):
            raise ValueError("task_id inválido")
        return [kling, "query_tasks", task_id]
    contract = load_contract(contract_path)
    spec = contract.get("operations", {}).get(operation)
    if not isinstance(spec, dict):
        raise ValueError("operação não autorizada pelo contrato")
    params = request.get("parameters")
    if not isinstance(params, dict):
        raise ValueError("parameters precisa ser objeto")
    flags = spec.get("flags", {})
    positionals = spec.get("positionals", [])
    if not isinstance(flags, dict):
        raise ValueError("flags inválidas no contrato")
    if (not isinstance(positionals, list) or
            not all(isinstance(key, str) and key for key in positionals) or
            len(positionals) != len(set(positionals))):
        raise ValueError("positionals inválidos no contrato")
    if set(flags) & set(positionals):
        raise ValueError("parâmetro duplicado entre flags e positionals")
    required = set(spec.get("required", []))
    allowed = set(flags) | set(positionals)
    if not required <= allowed:
        raise ValueError("required contém parâmetro fora do contrato")
    missing = required - params.keys()
    if missing:
        raise ValueError("parâmetros obrigatórios ausentes: " + ",".join(sorted(missing)))
    unknown = set(params) - allowed
    if unknown:
        raise ValueError("parâmetros não autorizados: " + ",".join(sorted(unknown)))
    argv = [kling, operation]
    for key in sorted(set(params) - set(positionals)):
        value = params[key]
        flag = flags[key]
        if not isinstance(flag, str) or not flag.startswith("--"):
            raise ValueError("flag inválida no contrato")
        if isinstance(value, bool):
            if value:
                argv.append(flag)
        elif isinstance(value, (str, int, float)):
            rendered = str(value)
            if rendered.startswith("--"):
                raise ValueError(f"valor de flag inválido em {key}")
            argv.extend([flag, rendered])
        elif isinstance(value, list) and all(isinstance(v, str) for v in value):
            if any(item.startswith("--") for item in value):
                raise ValueError(f"valor de flag inválido em {key}")
            for item in value:
                argv.extend([flag, item])
        else:
            raise ValueError(f"tipo inválido em {key}")
    for key in positionals:
        if key not in params:
            continue
        value = params[key]
        if isinstance(value, bool) or not isinstance(value, (str, int, float)):
            raise ValueError(f"tipo inválido em {key}")
        rendered = str(value)
        if not rendered.strip() or rendered.startswith("--"):
            raise ValueError(f"positional inválido em {key}")
        argv.append(rendered)
    return argv

def sanitize(text: str) -> str:
    return re.sub(r"(?i)(token|secret|password|authorization)[=: ]+\S+", r"\1=[REDACTED]", text)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--request", required=True)
    p.add_argument("--approval")
    p.add_argument("--contract", default=str(Path(__file__).resolve().parent.parent / "templates" / "kling-contract.json"))
    p.add_argument("--execute", action="store_true")
    p.add_argument("--timeout", type=int, default=120)
    args = p.parse_args()
    request = load_json(Path(args.request).resolve())
    kling = shutil.which("kling")
    if not kling:
        raise SystemExit("kling não encontrado")
    argv = build_argv(request, kling, Path(args.contract).resolve())
    paid = request.get("operation") not in DISCOVERY | {"query_tasks"}
    approval = None
    if paid:
        if not args.approval:
            raise SystemExit("aprovação obrigatória")
        approval_path = Path(args.approval).resolve()
        approval = load_json(approval_path)
        validate_approval(request, approval)
    if not args.execute:
        print(json.dumps({"execute": False, "argv": argv, "request_hash": request_hash(request)}, ensure_ascii=False))
        return
    if paid:
        approval["used_at"] = utc_now()
        atomic_write_json(approval_path, approval)
    cp = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=args.timeout)
    result = {
        "executed_at": utc_now(), "returncode": cp.returncode,
        "stdout": sanitize(cp.stdout), "stderr": sanitize(cp.stderr),
        "request_hash": request_hash(request)
    }
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(cp.returncode)

if __name__ == "__main__":
    main()
