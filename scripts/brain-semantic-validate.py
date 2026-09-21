"""Validate an explicit Brain batch without claiming semantic completeness."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, re, sys
sys.dont_write_bytecode=True
import yaml
from jsonschema import Draft202012Validator, FormatChecker

def frontmatter(text):
    if not text.startswith('---\n'):raise ValueError('Missing structured frontmatter')
    return yaml.safe_load(text.split('---',2)[1])

def validate(root,baseline,manifest,proposal_file="coverage-20260921.json"):
    root=root.resolve();baseline=baseline.resolve()
    sys=root/'BRAIN/99-SISTEMA/brain-v2'
    schema=json.loads((sys/'schemas/note.schema.json').read_text())
    note_validator=Draft202012Validator(schema,format_checker=FormatChecker())
    proposal_validator=Draft202012Validator(json.loads((sys/'schemas/proposal.schema.json').read_text()))
    types=yaml.safe_load((sys/'relationships/relationship-types.yaml').read_text())['approved_relationship_types']
    failures=[]; tested=0; typed=0
    for row in manifest:
        path=root/row['path']
        if path.is_symlink() or not path.is_file():failures.append(row['path']+': missing/linked file');continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['after_sha256']:failures.append(row['path']+': hash mismatch')
        if not row['path'].endswith('.md'):continue
        if row['path'].startswith('BRAIN/60-AGENTES/versionados/shared-skills/'):
            meta=frontmatter(path.read_text())
            if not meta.get('name') or not meta.get('description'):failures.append(row['path']+': invalid skill metadata')
            continue
        try:meta=frontmatter(path.read_text())
        except Exception as e:failures.append(row['path']+': '+str(e));continue
        errors=list(note_validator.iter_errors(meta))
        failures.extend(row['path']+': '+e.message for e in errors)
        tested+=1
        for rel in meta.get('relationships',[]):
            typed+=1
            if rel['type'] not in types:failures.append(row['path']+': unknown relation type')
            if not rel.get('reason','').strip() or not rel.get('source','').strip():failures.append(row['path']+': missing relation evidence')
            target=(root/rel['target']).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():failures.append(row['path']+': unresolved relation target '+rel['target'])
    proposals=json.loads((sys/'proposals'/proposal_file).read_text())
    seen=set(); manifestpaths={r['path'] for r in manifest}
    for proposal in proposals:
        failures.extend('proposal: '+e.message for e in proposal_validator.iter_errors(proposal))
        if proposal['proposal_id'] in seen:failures.append('Duplicate proposal identity')
        seen.add(proposal['proposal_id'])
        if proposal['target_note'] not in manifestpaths:failures.append('Proposal outside manifest')
    spec=importlib.util.spec_from_file_location('link_gate',sys/'tools/brain_link_gate.py')
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    current=gate.scan(root)
    old=gate.scan(baseline)
    ok,graph_failures=gate.delta_ok(current,old)
    failures.extend(graph_failures)
    if current['broken_internal_links']:failures.append('Broken internal links')
    # Unlike the legacy gate, inspect all changed text files, including JSON and tools.
    signatures=[re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
                re.compile(r'\bgh[pousr]_[A-Za-z0-9_]{30,}\b'),
                re.compile(r'\bgithub_pat_[A-Za-z0-9_]{30,}\b'),
                re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
                re.compile(r'\bsk-[A-Za-z0-9_-]{30,}\b'),
                re.compile(r'(?i)(?:password|passwd|senha|api_key|access_token)\s*[=:]\s*[\"\x27][A-Za-z0-9_+/=-]{20,}[\"\x27]')]
    for row in manifest:
        text=(root/row['path']).read_text()
        if any(s.search(text) for s in signatures):failures.append(row['path']+': potential credential; inspect privately')
    return {'ok':not failures,'failures':failures,'changed_notes_tested':tested,'typed_relationships_tested':typed,
            'proposal_envelopes_tested':len(proposals),'graph':current,
            'semantic_quality_of_all_notes':'not_measured','historical_coverage_complete':False,
            'legacy_health_score_is_not_semantic_validation':True}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--proposals',default='coverage-20260921.json')
    a=p.parse_args();r=validate(a.root,a.baseline,json.loads(a.manifest.read_text()),a.proposals)
    a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='graph'},ensure_ascii=False))
    raise SystemExit(0 if r['ok'] else 1)

if __name__=='__main__':main()
