"""Exercise the installed runner's gates without executing its module entry or I/O."""
import ast
import hashlib
from pathlib import Path
import re
import tempfile
import unittest


@unittest.skipUnless(Path(__file__).with_name('review.py').exists(), 'Generate the reviewed runner candidate first')
class RunnerGateTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).with_name('review.py').read_text()
        tree = ast.parse(source)
        names = {'Blocked','norm','field','validate_contract','executor_fields','assigned','valid_branch'}
        selected = [node for node in tree.body if isinstance(node,(ast.ClassDef,ast.FunctionDef)) and node.name in names]
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ns = {'re':re,'hashlib':hashlib,'STATE':Path(self.tmp.name),
                   'REPO':'mundoinformaticacanaria/whereis','EXECUTOR':'PROGRAMADOR-LINUX',
                   'ROLES':{'PROPIETARIO','FUNCIONAL','TECH LEAD','ARQUITECTO','PROGRAMADOR','QA'},
                   'git':lambda *_:'trusted-workflow.yml'}
        exec(compile(ast.Module(body=selected,type_ignores=[]),'runner-gates','exec'),self.ns)
        self.policy = 'Synthetic policy including trailing newline\n'
        self.issue = {'body':'\n'.join(['Autorización de desarrollo: https://github.com/mundoinformaticacanaria/whereis/issues/999',
            'QA independiente prevista: CHATGPT-QA','Alcance','Exclusiones','Criterios de aceptación','Dependencias','Validación requerida'])}
        self.docs = {'docs/logs/README.md':self.policy}
        (self.ns['STATE']/'heartbeat-policy.sha256').write_text(hashlib.sha256(self.policy.encode()).hexdigest()+'\n')

    def test_exact_policy_bytes_accepted(self):
        self.ns['validate_contract'](self.issue,self.docs)

    def test_changed_policy_blocks(self):
        with self.assertRaises(self.ns['Blocked']):
            self.ns['validate_contract'](self.issue,{'docs/logs/README.md':self.policy+'Changed'})

    def test_live_baseline_veto_not_bypassed(self):
        with self.assertRaises(self.ns['Blocked']):
            self.ns['validate_contract'](self.issue,dict(self.docs,baseline='no hay programación autorizada'))

    def test_absent_ci_not_bypassed(self):
        self.ns['git']=lambda *_:''
        with self.assertRaises(self.ns['Blocked']):self.ns['validate_contract'](self.issue,self.docs)

    def test_multirole_and_executor_ambiguity_rejected(self):
        issue={'labels':[{'name':'PROGRAMADOR'},{'name':'QA'}],'body':'Ejecutor autorizado: PROGRAMADOR-LINUX'}
        self.assertFalse(self.ns['assigned'](issue))
        issue['labels']=[{'name':'PROGRAMADOR'}]
        issue['body']+='\nEjecutor autorizado: CODEX'
        self.assertFalse(self.ns['assigned'](issue))


if __name__ == '__main__':unittest.main()
