import datetime as dt
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from heartbeat import Heartbeat, HeartbeatBlocked, Conflict, line_at, pending, UTC
from engine import registry, selected, credential_environment, instance

NOW = dt.datetime(2026, 11, 9, 10, 0, tzinfo=UTC)


class Store:
    def __init__(self, text=""):
        self.text, self.sha, self.conflict = text, 0, False

    def read(self):
        return self.text, self.sha

    def write(self, text, sha):
        if self.conflict:
            self.conflict = False
            self.text = line_at(NOW, 99, "other-writer", "INICIO") + "\n" + self.text
            self.sha += 1
        if sha != self.sha:
            raise Conflict()
        self.text, self.sha = text, self.sha + 1


class HeartbeatTests(unittest.TestCase):
    def test_29_59_blocks(self):
        row = line_at(NOW - dt.timedelta(seconds=1799), 28, "a", "INICIO")
        self.assertEqual(pending(row, 28, NOW), ["a"])

    def test_30_00_expires(self):
        row = line_at(NOW - dt.timedelta(seconds=1800), 28, "a", "INICIO")
        self.assertEqual(pending(row, 28, NOW), [])

    def test_paired_finish_immediate(self):
        rows = '\n'.join([line_at(NOW, 28, 'a', 'INICIO'), line_at(NOW, 28, 'a', 'FIN', 'OK')])
        self.assertEqual(pending(rows, 28, NOW), [])

    def test_other_finish_does_not_unlock(self):
        rows = '\n'.join([line_at(NOW, 28, 'a', 'INICIO'), line_at(NOW, 28, 'b', 'FIN', 'OK')])
        self.assertEqual(pending(rows, 28, NOW), ['a'])

    def test_finish_before_start_does_not_unlock(self):
        rows = '\n'.join([line_at(NOW, 28, 'a', 'INICIO'), line_at(NOW-dt.timedelta(seconds=1), 28, 'a', 'FIN', 'OK')])
        self.assertEqual(pending(rows, 28, NOW), ['a'])

    def test_future_start_blocks(self):
        self.assertEqual(pending(line_at(NOW+dt.timedelta(seconds=1), 28, 'a', 'INICIO'), 28, NOW), ['a'])

    def test_other_issue_independent(self):
        self.assertEqual(pending(line_at(NOW, 29, 'a', 'INICIO'), 28, NOW), [])

    def test_local_dst_representation(self):
        self.assertIn('2026-07-01T13:00:00+01:00', line_at(dt.datetime(2026,7,1,12,tzinfo=UTC),28,'a','INICIO'))
        self.assertIn('2026-11-09T10:00:00+00:00', line_at(NOW,28,'a','INICIO'))

    def test_transition_boundaries(self):
        for utc, local in [('2026-03-29T00:59:59+00:00','2026-03-29T00:59:59+00:00'),
                           ('2026-03-29T01:00:00+00:00','2026-03-29T02:00:00+01:00'),
                           ('2026-10-25T00:59:59+00:00','2026-10-25T01:59:59+01:00'),
                           ('2026-10-25T01:00:00+00:00','2026-10-25T01:00:00+00:00')]:
            self.assertIn(local, line_at(dt.datetime.fromisoformat(utc),28,'a','INICIO'))

    def test_conflict_reconciles_without_lost_other_writer(self):
        store = Store(); store.conflict = True
        beat = Heartbeat(store.read, store.write, lambda: NOW)
        beat.start(28)
        self.assertIn('other-writer', store.text)
        beat.finish('SYNTHETIC_PASS')
        self.assertEqual(len(store.text.splitlines()), 3)

    def test_two_independent_clients_block_same_issue(self):
        store = Store()
        first = Heartbeat(store.read, store.write, lambda: NOW)
        second = Heartbeat(store.read, store.write, lambda: NOW)
        first.start(28)
        with self.assertRaises(HeartbeatBlocked): second.start(28)
        first.finish('OK')
        second.start(28)

    def test_late_finish_keeps_new_start_pending(self):
        store = Store(); clock = [NOW]
        first = Heartbeat(store.read, store.write, lambda: clock[0])
        second = Heartbeat(store.read, store.write, lambda: clock[0])
        first.start(28); clock[0] += dt.timedelta(seconds=1800)
        other = second.start(28); first.finish('LATE')
        self.assertEqual(pending(store.text,28,clock[0]), [other])

    def test_retention_preserves_historical_rows(self):
        store = Store('\n'.join('historical-'+str(i) for i in range(100))+'\n')
        beat = Heartbeat(store.read,store.write,lambda:NOW);beat.start(28)
        self.assertEqual(len(store.text.splitlines()),100)
        self.assertIn('historical-98',store.text)
        self.assertNotIn('historical-99',store.text)

    def test_transport_error_not_ignored(self):
        def denied(): raise PermissionError('synthetic')
        with self.assertRaises(PermissionError): Heartbeat(denied,lambda *_:None).start(28)

    def test_evicted_start_never_fabricated(self):
        store=Store();beat=Heartbeat(store.read,store.write,lambda:NOW);beat.start(28)
        store.text=''
        with self.assertRaises(HeartbeatBlocked):beat.finish('OK')

    def test_conflict_exhaustion_blocks(self):
        def conflict(*_):raise Conflict()
        with self.assertRaises(HeartbeatBlocked):Heartbeat(lambda:('',0),conflict,lambda:NOW).start(28)

    def test_invalid_id_and_result_rejected(self):
        with self.assertRaises(ValueError):line_at(NOW,28,'injected\n','INICIO')
        with self.assertRaises(ValueError):line_at(NOW,28,'a','FIN','secret text')


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.profiles=json.loads((Path(__file__).parent/'provider-profiles.json').read_text())

    def test_current_qwen_preserved(self):
        result=registry({'MODEL':'openrouter/qwen/qwen3.8-27b:free'},self.profiles,{'permissions':['synthetic']})
        self.assertIn('qwen/qwen3.8-27b:free',result['providers']['openrouter']['models'])
        self.assertEqual(result['permissions'],['synthetic'])

    def test_compatible_model_uses_configuration_only(self):
        result=registry({'MODEL':'openrouter/synthetic/offline'},self.profiles,{})
        self.assertIn('synthetic/offline',result['providers']['openrouter']['models'])

    def test_other_provider_is_not_silently_enabled(self):
        with self.assertRaises(KeyError):selected({'MODEL':'unapproved/model'},self.profiles)

    def test_declarative_profile_has_no_runner_dependency(self):
        profiles={'fixture':{'approved':True,'endpoint':'https://example.invalid','package':'fixture-only','credential_env':'FIXTURE_KEY'}}
        self.assertEqual(selected({'MODEL':'fixture/model'},profiles)[0],'fixture')

    def test_plaintext_endpoint_rejected(self):
        self.profiles['openrouter']['endpoint']='http://example.invalid'
        with self.assertRaises(ValueError):selected({'MODEL':'openrouter/model'},self.profiles)

    def test_unapproved_profile_rejected(self):
        self.profiles['openrouter']['approved']=False
        with self.assertRaises(ValueError):selected({'MODEL':'openrouter/model'},self.profiles)

    def test_private_exclusive_auth_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'credential.json';path.write_text('{"OPENROUTER_API_KEY":"synthetic-only"}');path.chmod(0o600)
            values={'MODEL':'openrouter/model'}
            self.assertEqual(set(credential_environment(values,self.profiles,path)),{'OPENROUTER_API_KEY'})
            path.chmod(0o644)
            with self.assertRaises(ValueError):credential_environment(values,self.profiles,path)

    def test_no_shell_evaluation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'instance.env';path.write_text('MODEL=$(false)\n')
            self.assertEqual(instance(path)['MODEL'],'$(false)')

    def test_duplicate_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'instance.env';path.write_text('MODEL=a\nMODEL=b\n')
            with self.assertRaises(ValueError):instance(path)


if __name__ == '__main__':
    unittest.main()
