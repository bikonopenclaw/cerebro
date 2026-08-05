#!/usr/bin/env python3
"""Brain v2 link gate.

The gate is intentionally dependency-free. It scans Markdown files, resolves
wiki/Markdown links against repository files and aliases, and fails when a
change adds knowledge debt beyond the accepted baseline.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


WIKILINK_RE = re.compile(r"!?\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MDLINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ID_RE = re.compile(r"^\s*id:\s*['\"]?([^'\"\n]+)['\"]?\s*$", re.MULTILINE)
ALIASES_BLOCK_RE = re.compile(r"^\s*aliases:\s*(?:\n((?:\s+-\s+.+\n)+)|\[(.*?)\])", re.MULTILINE)
SECRET_RE = re.compile(
    r"(BEGIN [A-Z ]*PRIVATE KEY|"
    r"(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,})",
    re.IGNORECASE,
)
ENTRY_POINTS = (
    "BRAIN/99-SISTEMA/INDEX.md",
    "BRAIN/01-DIARIO/README.md",
    "BRAIN/99-SISTEMA/brain-v2/governance/README.md",
)
COGNITIVE_EXCLUDED_PREFIXES = (
    "BRAIN/60-AGENTES/versionados/",
)
COGNITIVE_EXCLUDED_PARTS = (
    "/evidence/",
    "/exports/",
    "/relatorios/",
    "/reports/",
    "/runtime/",
    "/snapshots/",
)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_files(root: Path) -> list[Path]:
    return sorted((root / "BRAIN").glob("**/*.md"))


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end == -1:
        return ""
    return text[4:end]


def aliases_from(text: str) -> list[str]:
    fm = frontmatter(text)
    aliases: list[str] = []
    for match in ALIASES_BLOCK_RE.finditer(fm):
        block, inline = match.groups()
        if block:
            aliases.extend(line.split("-", 1)[1].strip().strip("'\"") for line in block.splitlines())
        if inline:
            aliases.extend(item.strip().strip("'\"") for item in inline.split(",") if item.strip())
    return aliases


def build_resolver(files: list[Path], root: Path) -> tuple[set[str], dict[str, str], dict[str, list[str]], dict[str, list[str]]]:
    targets: set[str] = set()
    target_to_path: dict[str, str] = {}
    aliases: dict[str, list[str]] = {}
    ids: dict[str, list[str]] = {}
    for path in files:
        r = rel(path, root)
        no_ext = r[:-3]
        stem = path.stem
        for target in (r, no_ext, stem):
            targets.add(target)
            target_to_path.setdefault(target, r)
        text = path.read_text(encoding="utf-8", errors="replace")
        for alias in aliases_from(text):
            aliases.setdefault(alias, []).append(r)
            targets.add(alias)
            target_to_path.setdefault(alias, r)
        found_id = ID_RE.search(frontmatter(text))
        if found_id:
            ids.setdefault(found_id.group(1).strip(), []).append(r)
    return targets, target_to_path, aliases, ids


def resolve_wikilink_target(target: str, target_to_path: dict[str, str]) -> str | None:
    clean = target.strip().split("#", 1)[0]
    if not clean:
        return ""
    normalized = clean.replace("\\", "/")
    without_ext = normalized.removesuffix(".md")
    variants = (
        normalized,
        without_ext,
        f"BRAIN/{normalized}",
        f"BRAIN/{without_ext}",
    )
    for item in variants:
        if item in target_to_path:
            return target_to_path[item]
    return None


def resolve_wikilink(target: str, target_to_path: dict[str, str]) -> bool:
    return resolve_wikilink_target(target, target_to_path) is not None


def resolve_mdlink_target(target: str, source: Path, root: Path) -> str | None:
    target = target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
        return ""
    target = target.split("#", 1)[0]
    candidate = (source.parent / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return ""
    if candidate.exists():
        return rel(candidate, root)
    return None


def resolve_mdlink(target: str, source: Path, root: Path) -> bool:
    return resolve_mdlink_target(target, source, root) is not None


def classify(path: Path, root: Path) -> str:
    r = rel(path, root)
    if r.startswith("BRAIN/01-DIARIO/"):
        return "diary"
    if r.startswith("BRAIN/20-EMPRESAS/"):
        return "entity"
    if r.startswith("BRAIN/30-PESSOAS/"):
        return "entity"
    if r.startswith("BRAIN/40-CONHECIMENTO/"):
        return "knowledge"
    if r.startswith("BRAIN/50-PROJETOS/"):
        return "project"
    if r.startswith("BRAIN/60-AGENTES/"):
        return "agent"
    if r.startswith("BRAIN/70-AUTOMACOES/"):
        return "automation"
    if r.startswith("BRAIN/80-DASHBOARDS/"):
        return "dashboard"
    if r.startswith("BRAIN/99-SISTEMA/"):
        return "system"
    return "uncategorized"


def cognitive_excluded(path_rel: str) -> bool:
    return path_rel.startswith(COGNITIVE_EXCLUDED_PREFIXES) or any(part in path_rel for part in COGNITIVE_EXCLUDED_PARTS)


def graph_metrics(edges: dict[str, set[str]], cognitive_files: set[str]) -> dict:
    entry_points = [entry for entry in ENTRY_POINTS if entry in cognitive_files]
    reachable: set[str] = set()
    stack = list(entry_points)
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        stack.extend(sorted(edges.get(current, set()) & cognitive_files - reachable))

    incident = {path: 0 for path in cognitive_files}
    undirected: dict[str, set[str]] = {path: set() for path in cognitive_files}
    for source, targets in edges.items():
        if source not in cognitive_files:
            continue
        for target in targets:
            if target not in cognitive_files:
                continue
            incident[source] += 1
            incident[target] += 1
            undirected[source].add(target)
            undirected[target].add(source)

    seen: set[str] = set()
    components = 0
    for path in sorted(cognitive_files):
        if path in seen:
            continue
        components += 1
        stack = [path]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(sorted(undirected[current] - seen))

    unreachable = sorted(cognitive_files - reachable)
    isolated = sorted(path for path, count in incident.items() if count == 0)
    total = len(cognitive_files)
    reachability_rate = 1 if total == 0 else len(reachable) / total
    return {
        "entry_points": entry_points,
        "cognitive_markdown": total,
        "reachable_cognitive_markdown": len(reachable),
        "unreachable_cognitive_markdown": len(unreachable),
        "unreachable_files": unreachable,
        "isolated_cognitive_markdown": len(isolated),
        "isolated_files": isolated,
        "graph_components": components,
        "reachability_rate": reachability_rate,
    }


def scan(root: Path) -> dict:
    files = markdown_files(root)
    targets, target_to_path, aliases, ids = build_resolver(files, root)
    broken: list[dict] = []
    secret_candidates: list[str] = []
    class_counts: dict[str, int] = {}
    internal_link_count = 0
    edges: dict[str, set[str]] = {}
    cognitive_files: set[str] = set()
    excluded_cognitive_files: list[str] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        r = rel(path, root)
        class_counts[classify(path, root)] = class_counts.get(classify(path, root), 0) + 1
        if cognitive_excluded(r):
            excluded_cognitive_files.append(r)
        else:
            cognitive_files.add(r)
        if SECRET_RE.search(text):
            secret_candidates.append(r)
        for match in WIKILINK_RE.finditer(text):
            target = match.group(1)
            resolved = resolve_wikilink_target(target, target_to_path)
            if resolved is None:
                broken.append({"source": r, "type": "wikilink", "target": target})
            elif resolved:
                internal_link_count += 1
                edges.setdefault(r, set()).add(resolved)
        for match in MDLINK_RE.finditer(text):
            target = match.group(1)
            resolved = resolve_mdlink_target(target, path, root)
            if resolved is None:
                broken.append({"source": r, "type": "markdown", "target": target})
            elif resolved:
                internal_link_count += 1
                edges.setdefault(r, set()).add(resolved)

    duplicate_ids = {k: v for k, v in ids.items() if len(v) > 1}
    duplicate_aliases = {k: v for k, v in aliases.items() if len(v) > 1}
    total_links = max(1, internal_link_count + len(broken))
    link_integrity_rate = 1 - (len(broken) / total_links)
    graph = graph_metrics(edges, cognitive_files)
    schema_pass_rate = 1
    relationship_pass_rate = 1
    identity_integrity_rate = 0 if duplicate_ids or duplicate_aliases else 1
    knowledge_health = (
        (0.30 * schema_pass_rate)
        + (0.25 * relationship_pass_rate)
        + (0.20 * graph["reachability_rate"])
        + (0.15 * link_integrity_rate)
        + (0.10 * identity_integrity_rate)
    )

    return {
        "markdown_total": len(files),
        "internal_links": internal_link_count,
        "broken_internal_links": len(broken),
        "broken_links": broken,
        "classification_counts": class_counts,
        "uncategorized_markdown": class_counts.get("uncategorized", 0),
        "duplicate_ids": duplicate_ids,
        "duplicate_aliases": duplicate_aliases,
        "secret_candidates": sorted(set(secret_candidates)),
        "cognitive_excluded_markdown": len(excluded_cognitive_files),
        "cognitive_excluded_files": sorted(excluded_cognitive_files),
        "graph": graph,
        "knowledge_health_estimate": max(0, min(1, knowledge_health)),
    }


def delta_ok(current: dict, baseline: dict) -> tuple[bool, list[str]]:
    if not baseline:
        return True, []
    failures: list[str] = []
    for key in ("broken_internal_links", "uncategorized_markdown"):
        if current.get(key, 0) > baseline.get(key, math.inf):
            failures.append(f"{key} increased: {baseline.get(key)} -> {current.get(key)}")
    current_graph = current.get("graph", {})
    baseline_graph = baseline.get("graph", {})
    for key in ("unreachable_cognitive_markdown", "isolated_cognitive_markdown"):
        if baseline_graph and current_graph.get(key, 0) > baseline_graph.get(key, math.inf):
            failures.append(f"graph.{key} increased: {baseline_graph.get(key)} -> {current_graph.get(key)}")
    if baseline_graph and current_graph.get("reachability_rate", 0) < baseline_graph.get("reachability_rate", 0):
        failures.append(
            "graph.reachability_rate decreased: "
            f"{baseline_graph.get('reachability_rate')} -> {current_graph.get('reachability_rate')}"
        )
    if current.get("duplicate_ids"):
        failures.append("duplicate_ids present")
    if current.get("duplicate_aliases"):
        failures.append("duplicate_aliases present")
    current_secrets = set(current.get("secret_candidates", []))
    baseline_secrets = set(baseline.get("secret_candidates", []))
    new_secrets = sorted(current_secrets - baseline_secrets)
    if new_secrets:
        failures.append(f"new secret candidates present: {new_secrets}")
    return not failures, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--baseline")
    parser.add_argument("--write-baseline")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    current = scan(root)

    if args.write_baseline:
        out = Path(args.write_baseline)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    baseline = load_json(Path(args.baseline)) if args.baseline else {}
    ok, failures = delta_ok(current, baseline)
    result = {"ok": ok, "failures": failures, "metrics": current}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"ok={ok}")
        print(f"broken_internal_links={current['broken_internal_links']}")
        print(f"uncategorized_markdown={current['uncategorized_markdown']}")
        for failure in failures:
            print(f"FAIL: {failure}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
