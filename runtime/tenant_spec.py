"""TenantSpec v1 schema and mandatory-policy validation."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
SCHEMA_PATH=ROOT/'schemas'/'tenant-spec.v1.schema.json'
class TenantSpecValidationError(ValueError): pass
def _fail(message:str)->None: raise TenantSpecValidationError(message)
def _assert_no_literal_secrets(value:Any,path:str='$')->None:
    forbidden={'password','token','secret','api_key','apikey','private_key'}
    if isinstance(value,dict):
        for key,child in value.items():
            if key.lower() in forbidden: _fail(f'{path}.{key}: literal secrets are forbidden; use secretRefs')
            _assert_no_literal_secrets(child,f'{path}.{key}')
    elif isinstance(value,list):
        for index,child in enumerate(value): _assert_no_literal_secrets(child,f'{path}[{index}]')
def _assert_acyclic_delegation(agents:list[dict[str,Any]])->None:
    graph={a['id']:set(a.get('delegates',{}).get('allow',[])) for a in agents}
    for source,targets in graph.items():
        if unknown:=targets-graph.keys(): _fail(f'agent {source}: delegates to unknown agents: {sorted(unknown)}')
    visiting=set(); visited=set()
    def visit(node:str)->None:
        if node in visiting: _fail(f'delegation graph contains a cycle at agent {node}')
        if node not in visited:
            visiting.add(node)
            for target in graph[node]: visit(target)
            visiting.remove(node); visited.add(node)
    for agent_id in graph: visit(agent_id)
def validate_tenant_spec(spec:dict[str,Any])->None:
    required={'apiVersion','kind','metadata','business','security','connectors','agents'}
    if missing:=required-spec.keys(): _fail(f'missing required top-level fields: {sorted(missing)}')
    if spec['apiVersion']!='hermes.platform/v1' or spec['kind']!='TenantSpec': _fail('unsupported TenantSpec apiVersion or kind')
    security=spec['security']; audit=security.get('audit',{})
    if security.get('baseline')!='mandatory-baseline@1.0.0': _fail('mandatory baseline cannot be replaced or removed')
    if security.get('secretsProvider') not in {'docker-secrets','vault'}: _fail('secretsProvider must be docker-secrets or vault')
    if audit.get('enabled') is not True or audit.get('immutable') is not True: _fail('immutable audit logging is mandatory')
    if not isinstance(audit.get('retentionDays'),int) or audit['retentionDays']<30: _fail('audit retentionDays must be at least 30')
    if security.get('network',{}).get('defaultDenyEgress') is not True: _fail('default-deny egress is mandatory')
    _assert_no_literal_secrets(spec)
    connectors={c['id']:set(c.get('allowedOperations',[])) for c in spec['connectors']}
    if len(connectors)!=len(spec['connectors']): _fail('connector ids must be unique')
    agent_ids=set()
    for agent in spec['agents']:
        agent_id=agent.get('id')
        if not agent_id or agent_id in agent_ids: _fail('agent ids must be present and unique')
        agent_ids.add(agent_id); isolation=agent.get('isolation',{})
        if not isolation.get('dataNamespace') or isolation.get('networkPolicy')!='strict' or isolation.get('filesystem')!='read_only': _fail(f'agent {agent_id}: strict data, network and filesystem isolation is mandatory')
        for binding in agent.get('connectors',[]):
            cid=binding.get('connectorId')
            if cid not in connectors: _fail(f'agent {agent_id}: unknown connector {cid}')
            if unknown:=set(binding.get('scopes',[]))-connectors[cid]: _fail(f'agent {agent_id}: scopes not granted by {cid}: {sorted(unknown)}')
        if agent.get('permissions',{}).get('maxEffect')=='irreversible' and agent.get('permissions',{}).get('confirmation',{}).get('required') is not True: _fail(f'agent {agent_id}: irreversible actions require confirmation')
    _assert_acyclic_delegation(spec['agents'])
def validate_file(spec_path:Path,schema_path:Path=SCHEMA_PATH)->None:
    try: spec=json.loads(spec_path.read_text(encoding='utf-8')); schema=json.loads(schema_path.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc: _fail(f'cannot load validation input: {exc}')
    errors=sorted(Draft202012Validator(schema).iter_errors(spec),key=lambda error:list(error.path))
    if errors: _fail(f'schema violation: {errors[0].message}')
    validate_tenant_spec(spec)
def main()->int:
    parser=argparse.ArgumentParser(description='Validate a TenantSpec v1 JSON file.'); parser.add_argument('spec',type=Path); args=parser.parse_args()
    try: validate_file(args.spec)
    except TenantSpecValidationError as exc: print(f'INVALID: {exc}'); return 1
    print(f'VALID: {args.spec}'); return 0
if __name__=='__main__': raise SystemExit(main())
