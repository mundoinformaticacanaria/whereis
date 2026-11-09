"""Generate a candidate from the exact backed-up runner, without running it."""
import ast
import hashlib
from pathlib import Path
import sys

EXPECTED = 'e67e42bf23de4fe4b0d980800124e809f5cc2a5bf53eb1a4dc3007e5302f2039'


def adapt(source):
    if hashlib.sha256(source.encode()).hexdigest() != EXPECTED:
        raise RuntimeError('Runner changed; inspect and reconcile instead of overwriting')
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    invoke = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'invoke')
    lines[invoke.lineno-1:invoke.end_lineno] = ['def invoke(prompt,output):\n', ' return invoke_engine(prompt,output)\n']
    result = ''.join(lines)
    old = 'def run(*args):'
    assert result.count(old) == 1
    result = result.replace(old, 'def run(*args,raw=False):')
    result = result.replace(' return r.stdout.strip()', ' return r.stdout if raw else r.stdout.strip()', 1)
    old = 'docs={p:git("show","origin/main:"+p) for p in DOCS}; validate_contract(issue,docs)'
    assert result.count(old) == 1
    result = result.replace(old, 'docs={p:run("git","show","origin/main:"+p,raw=True) for p in DOCS}; validate_contract(issue,docs)\n heartbeat.start(number)')
    tree = ast.parse(result)
    main = tree.body[-1]
    assert isinstance(main, ast.If) and '__name__' in ast.unparse(main.test)
    lines = result.splitlines(keepends=True)
    lines[main.lineno-1:main.end_lineno] = ['''if __name__=="__main__":
 if "--self-test" in sys.argv: selftest()
 else:
  result="REVISION_COMPLETADA"
  try: work()
  except Blocked as exc:
   result="BLOQUEADO"; log("BLOCKED "+str(exc))
  except Exception as exc:
   result="ERROR"; log("ERROR "+type(exc).__name__+"; raw output suppressed"); raise
  finally:
   if heartbeat.current:
    try: heartbeat.finish(result)
    except Exception: log("HEARTBEAT_FIN_FAILED; retained owned ID; no fabricated persistence")
''']
    result = 'from guard import require_sandbox\nrequire_sandbox()\nfrom runner_support import heartbeat, invoke_engine\n' + ''.join(lines)
    ast.parse(result)
    return result


if __name__ == '__main__':
    source, target = map(Path, sys.argv[1:])
    if target.exists(): raise RuntimeError('Candidate exists; preserve it')
    target.write_text(adapt(source.read_text()))
    target.chmod(0o600)
    print('RUNNER_CANDIDATE_AST_PASS', hashlib.sha256(target.read_bytes()).hexdigest())
