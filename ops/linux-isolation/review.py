from guard import require_sandbox
require_sandbox()
from runner_support import heartbeat, invoke_engine
#!/usr/bin/env python3
"""Whereis-only scheduler. Model and paths are configuration."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess as sp
import sys
REPO=os.environ["REPOSITORY"]
EXECUTOR=os.environ["IDENTITY"]
ROOT=Path(os.environ["REPO_DIR"])
STATE=Path(os.environ["STATE_DIR"])
ROLES={"PROPIETARIO","FUNCIONAL","TECH LEAD","ARQUITECTO","PROGRAMADOR","QA"}
DOCS=["AGENTS.md","README.md","docs/estado-proyecto.md","docs/criterios-desarrollo.md",
"docs/contexto-programador.md","docs/arquitectura.md","docs/bootstrap-proyecto.md",
"docs/orquestacion/README.md",'docs/orquestacion/programador-linux.md',
"docs/decisiones/G-02-orquestacion-qwen-codex-chatgpt.md","docs/logs/README.md"]
class Blocked(Exception): pass
def log(message):
    line=dt.datetime.now(dt.timezone.utc).isoformat()+" "+message
    print("[whereis] "+line,flush=True)
    with (STATE/"runner.log").open("a") as out: out.write(line+"\n")
def run(*args,raw=False):
    r=sp.run(args,cwd=ROOT,text=True,capture_output=True,timeout=90)
    if r.returncode: raise Blocked("Command failed: "+args[0]+" "+args[1]+" exit="+str(r.returncode))
    return r.stdout if raw else r.stdout.strip()
def gh(path): return json.loads(run("gh","api","repos/"+REPO+"/"+path))
def pages(path):
    raw=run("gh","api","--paginate","repos/"+REPO+"/"+path,"--jq",".[] | tojson")
    return [json.loads(line) for line in raw.splitlines() if line.strip()]
def git(*args): return run("git",*args)
def norm(body): return re.sub(r"[*\x60_]","",body or "")
def executor_fields(issue):
    return [value.strip() for value in re.findall(r"(?mi)^[ \t]*Ejecutor autorizado[ \t]*:[ \t]*(.*?)[ \t]*$",norm(issue.get("body")))]
def assigned(issue):
    return EXECUTOR=="PROGRAMADOR-LINUX" and {x["name"] for x in issue["labels"]}&ROLES=={"PROGRAMADOR"} and executor_fields(issue)==[EXECUTOR]
def relevant_issues(issues):
    return [i for i in issues if "pull_request" not in i and "PROGRAMADOR" in {x["name"] for x in i["labels"]} and any(re.search(r"\b(?:PROGRAMADOR-LINUX|QWEN-LINUX)\b",value) for value in executor_fields(i))]
def valid_branch(branch,number):
    return re.fullmatch(r"programador-linux/"+str(number)+r"-[a-z0-9][a-z0-9-]*",branch) is not None
def fingerprint(issue,comments):
    value=[issue["body"],sorted(x["name"] for x in issue["labels"]),comments]
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
def clean():
    if git("status","--porcelain"): raise Blocked("Dirty checkout: preserve and inspect recovery.")
def field(body,key):
    m=re.search(r"(?mi)^\s*"+re.escape(key)+r"\s*:\s*(.+)$",norm(body))
    return m.group(1).strip() if m else ""
def validate_contract(issue,docs):
    body=norm(issue["body"]); auth=field(body,"Autorización de desarrollo")
    if not auth or "BLOQUEADO" in auth or "https://github.com/"+REPO not in auth:
        raise Blocked("Missing development authorization/baseline link.")
    if field(body,"QA independiente prevista") not in ("CHATGPT-QA","CODEX-QA"):
        raise Blocked("Independent QA not designated.")
    for marker in ("Alcance","Exclusiones","Criterios de aceptación","Dependencias","Validación requerida"):
        if marker not in body: raise Blocked("Incomplete contract: "+marker)
    text="\n".join(docs.values()).lower()
    forbidden=("implementación no autorizada","no hay programación autorizada",
    "desarrollo del producto todavía no autorizado","estado:** pendiente de proyecto",
    "primera issue de programación:** todavía no autorizada")
    if any(x in text for x in forbidden): raise Blocked("Live main blocks development/baselines.")
    if not git("ls-tree","-r","--name-only","origin/main",".github/workflows"):
        raise Blocked("No CI on main: no implementation or QA handoff.")
    if hashlib.sha256(docs["docs/logs/README.md"].encode()).hexdigest()!=(STATE/"heartbeat-policy.sha256").read_text().strip():
        raise Blocked("Heartbeat policy changed: adapt scheduler before material work.")
def invoke(prompt,output):
 return invoke_engine(prompt,output)
def ci_green(sha):
    checks=gh("commits/"+sha+"/check-runs?per_page=100"); runs=checks.get("check_runs",[])
    statuses=gh("commits/"+sha+"/status")
    return bool(runs) and checks.get("total_count",0)==len(runs) and all(
    c["status"]=="completed" and c["conclusion"]=="success" for c in runs) and all(
    s["state"]=="success" for s in statuses.get("statuses",[]))
def work():
    if REPO!="mundoinformaticacanaria/whereis": raise Blocked("Wrong repository config.")
    if git("remote","get-url","origin") not in ("https://github.com/"+REPO+".git",
    "https://github.com/"+REPO,"git@github.com:"+REPO+".git"): raise Blocked("Wrong origin.")
    clean(); git("fetch","--prune","origin")
    issues=[i for i in pages("issues?state=open&per_page=100") if "pull_request" not in i]
    relevant=relevant_issues(issues)
    if not relevant:
        log("NO_WORK assigned=0 model_invocations=0")
        return
    if len(relevant)!=1 or not assigned(relevant[0]): raise Blocked("Ambiguous assignment; no model.")
    issue=relevant[0]; number=issue["number"]
    comments=pages("issues/"+str(number)+"/comments?per_page=100")
    docs={p:run("git","show","origin/main:"+p,raw=True) for p in DOCS}; validate_contract(issue,docs)
    heartbeat.start(number)
    if not {"PROGRAMADOR","QA"}<={x["name"] for x in pages("labels?per_page=100")}:
        raise Blocked("Missing role labels.")
    branch=field(issue["body"],"Rama prevista")
    if not valid_branch(branch,number):
        raise Blocked('Tech Lead must specify one programador-linux issue branch.')
    owned=[p for p in pages("pulls?state=open&per_page=100") if p["head"]["ref"].startswith(("programador-linux/","qwen/"))]
    if any(p["head"]["ref"]!=branch for p in owned): raise Blocked('Another Linux executor PR active (including historical qwen/).')
    prs=[p for p in owned if p["head"]["ref"]==branch]
    if any(p["base"]["ref"]!="main" or p["head"]["repo"]["full_name"]!=REPO for p in prs):
        raise Blocked("Unexpected PR repository/base.")
    fp=fingerprint(issue,comments); statefile=STATE/"recovery"/("issue-"+str(number)+".json")
    state=json.loads(statefile.read_text()) if statefile.exists() else {}
    if state.get("fingerprint")==fp and state.get("phase") in ("started","blocked"):
        raise Blocked("Same contract attempted; inspect recovery or update assignment.")
    if git("branch","--list",branch): git("switch",branch)
    elif git("branch","-r","--list","origin/"+branch): git("switch","--track","origin/"+branch)
    elif prs: raise Blocked("Existing PR branch unavailable.")
    else: git("switch","-c",branch,"origin/main")
    if state.get("phase")!="published" or state.get("fingerprint")!=fp:
        state={"fingerprint":fp,"phase":"started","branch":branch}; statefile.write_text(json.dumps(state,indent=2))
        context={"issue":issue,"comments":comments,"pull_requests":prs}
        if prs:
            n=str(prs[0]["number"])
            context["reviews"]=pages("pulls/"+n+"/reviews?per_page=100")
            context["review_comments"]=pages("pulls/"+n+"/comments?per_page=100")
            context["pr_conversation"]=pages("issues/"+n+"/comments?per_page=100")
        contract=STATE/"recovery"/("contract-"+str(number)+".json")
        contract.write_text(json.dumps(context,ensure_ascii=False,indent=2))
        prompt=("Solo issue #"+str(number)+", rama "+branch+". Lee contrato completo "+str(contract)+
        " y documentos origin/main. Verifica referencias y autorizaciones. No push, PR, merge ni labels. "
        "Implementa solo alcance autorizado, ejecuta gates y crea commits locales. "
        "Si falta algo: WHEREIS_RESULT BLOCKED. Si listo: WHEREIS_RESULT READY con evidencias concretas.")
        output=STATE/"logs"/("model-"+str(number)+"-"+dt.datetime.now().strftime("%Y%m%dT%H%M%S")+".jsonl")
        log("MODEL_START issue="+str(number)); response=invoke(prompt,output)
        if not re.search(r"(?m)^WHEREIS_RESULT READY:",response) or "WHEREIS_RESULT BLOCKED:" in response:
            state["phase"]="blocked"; statefile.write_text(json.dumps(state))
            raise Blocked("No READY result; recovery retained.")
        clean()
        if git("branch","--show-current")!=branch: raise Blocked("Model changed branch.")
        git("diff","--check","origin/main...HEAD"); paths=git("diff","--name-only","origin/main...HEAD").splitlines()
        if not paths: raise Blocked("No changes; no PR.")
        protected=("AGENTS.md",".github/","docs/logs/","docs/orquestacion/","docs/contexto-","docs/decisiones/G-")
        if any(any(p.startswith(x) for x in protected) or p.endswith(".env") or "opencode" in p.lower() for p in paths):
            raise Blocked("Protected configuration/instructions changed; manual review.")
        latest=gh("issues/"+str(number))
        if not assigned(latest) or fingerprint(latest,pages("issues/"+str(number)+"/comments?per_page=100"))!=fp:
            raise Blocked("Contract changed; no publication.")
        git("push","origin","HEAD:refs/heads/"+branch); sha=git("rev-parse","HEAD")
        body=STATE/"recovery"/("pr-"+str(number)+".md")
        body.write_text("Refs #"+str(number)+"\n\nPROGRAMADOR "+EXECUTOR+" / "+os.environ["INSTANCE_ID"]+".\n\n"+
        response+"\n\nHead SHA: "+sha+"\n\nPendiente CI y QA independiente. Sin merge.\n")
        if not prs:
            run("gh","pr","create","--repo",REPO,"--base","main","--head",branch,
            "--title",EXECUTOR+" #"+str(number)+": "+issue["title"][:150],"--body-file",str(body))
        else: run("gh","pr","edit",str(prs[0]["number"]),"--repo",REPO,"--body-file",str(body))
        state.update(phase="published",sha=sha); statefile.write_text(json.dumps(state,indent=2))
    sha=state["sha"]
    if git("rev-parse","HEAD")!=sha: raise Blocked("Published HEAD changed.")
    current=gh("pulls?state=open&head=mundoinformaticacanaria:"+branch)
    if len(current)!=1 or current[0]["head"]["sha"]!=sha: raise Blocked("PR head mismatch.")
    if not ci_green(sha):
        log("WAIT_CI issue="+str(number)+" head="+sha+" no_QA_handoff"); return
    latest=gh("issues/"+str(number))
    if not assigned(latest) or fingerprint(latest,pages("issues/"+str(number)+"/comments?per_page=100"))!=fp:
        raise Blocked("Contract changed before QA handoff.")
    run("gh","issue","edit",str(number),"--repo",REPO,"--remove-label","PROGRAMADOR","--add-label","QA")
    state["phase"]="handoff"; statefile.write_text(json.dumps(state,indent=2))
    log("HANDOFF_QA issue="+str(number)+" head="+sha+" no_merge")
def selftest():
    sample={"labels":[{"name":"PROGRAMADOR"}],"body":'Ejecutor autorizado: PROGRAMADOR-LINUX'}
    assert assigned(sample)
    for body in ("Ejecutor autorizado: CODEX",'Ejecutor autorizado: PROGRAMADOR-LINUX\nEjecutor autorizado: CODEX',
    'Ejecutor autorizado: PROGRAMADOR-LINUX / CODEX',""): assert not assigned(dict(sample,body=body))
    assert not assigned(dict(sample,labels=[{"name":"PROGRAMADOR"},{"name":"QA"}]))
    assert field('**Rama prevista:** programador-linux/40-fix',"Rama prevista")=='programador-linux/40-fix'
    try: validate_contract(sample,{})
    except Blocked: pass
    else: raise AssertionError("Missing authorization accepted")
    print("SELFTEST PASS: executor, ambiguity, branch, missing authorization")
if __name__=="__main__":
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
