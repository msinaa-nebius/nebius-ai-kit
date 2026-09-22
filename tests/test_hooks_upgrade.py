"""Synthetic upgrade and hook regressions; never touch real home or credentials."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import test_bootstrap as base_tests
SOURCE = base_tests.SOURCE
import bootstrap as kit
import doctor
import hook_config
import legacy

spec = importlib.util.spec_from_file_location("memory_hook", SOURCE / "scripts/memory_hook.py")
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


class HooksUpgradeTests(base_tests.BootstrapTests):
    # Only inherit fixture helpers, not duplicate the original test run below.
    def test_hook_receipts_fresh_and_private_files_never_opened(self):
        self.install()
        private = self.target / '.nebius-local'
        private.mkdir()
        (private / 'STATE.md').write_text('SYNTHETIC_PRIVATE_CANARY')
        for event in hook.EVENTS:
            payload = {'hook_event_name': event, 'cwd': str(self.target),
                       'prompt': 'PROMPT_CANARY', 'transcript_path': '/never/open/me'}
            before = self.snapshot()
            result = hook.response(payload, self.target)
            self.assertNotEqual(result, hook.response(payload, self.target))
            text = result['hookSpecificOutput']['additionalContext']
            self.assertNotIn('CANARY', text)
            self.assertEqual(before, self.snapshot())
            with patch.object(Path, 'open', side_effect=AssertionError('must not read files')):
                hook.response(payload, self.target)

    def test_both_hook_commands_from_subdirectory_and_special_paths(self):
        self.target = self.base / "employee's $work ñ"
        self.install()
        sub = self.target / 'a b'
        sub.mkdir()
        for rel in hook_config.FILES:
            cfg = json.loads((self.target / rel).read_text())
            for event, groups in cfg['hooks'].items():
                command = groups[0]['hooks'][0]['command']
                for cwd in (self.target, sub):
                    result = subprocess.run(command, shell=True, cwd=cwd, input=json.dumps({
                        'hook_event_name': event, 'cwd': str(cwd), 'prompt': 'PAYLOAD_CANARY'}),
                        capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    output = json.loads(result.stdout)['hookSpecificOutput']
                    self.assertEqual(output['hookEventName'], event)
                    self.assertNotIn('PAYLOAD_CANARY', result.stdout)

    def test_hook_invalid_inputs_never_echo_payload(self):
        self.install()
        script = self.target / '.nebius-kit/memory_hook.py'
        for payload in ('SECRET_PAYLOAD', '[]', '{}', json.dumps({'hook_event_name':'Stop','cwd':str(self.target)}),
                        json.dumps({'hook_event_name':'SessionStart','cwd':'/outside'}), 'x'*(hook.LIMIT+1)):
            result = subprocess.run([sys.executable,str(script)],input=payload,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(result.stdout,'')
            self.assertNotIn('SECRET_PAYLOAD',result.stderr)

    def test_nested_workspace_cannot_use_parent_hook(self):
        self.install()
        nested = self.target / 'nested'
        (nested / '.nebius-kit').mkdir(parents=True)
        (nested / '.nebius-kit/install.json').write_text('{}')
        with self.assertRaises(ValueError):
            hook.response({'hook_event_name':'SessionStart','cwd':str(nested)},self.target)

    def test_merge_preserves_settings_permissions_and_other_hooks(self):
        self.target.mkdir()
        settings = self.target / '.claude/settings.json'
        settings.parent.mkdir()
        original = {'permissions':{'deny':['Bash(rm *)']}, 'disableAllHooks': True,
                    'hooks':{'SessionStart':[{'hooks':[{'type':'command','command':'echo mine'}]}]}}
        settings.write_text(json.dumps(original))
        self.install()
        result=json.loads(settings.read_text())
        self.assertTrue(result['disableAllHooks'])
        self.assertEqual(result['permissions'],original['permissions'])
        self.assertEqual(result['hooks']['SessionStart'][0],original['hooks']['SessionStart'][0])
        result['extra'] = 'new user setting'
        settings.write_text(json.dumps(result))
        self.assertEqual(doctor.check(self.target)[0],[])
        self.assertEqual(self.install(),{})

    def test_broken_json_preserves_whole_install(self):
        self.target.mkdir()
        p=self.target / '.claude/settings.json';p.parent.mkdir();p.write_text('{broken')
        before=self.snapshot()
        with self.assertRaises(ValueError):self.install()
        self.assertEqual(before,self.snapshot())

    def test_changed_nebius_hook_not_silently_replaced(self):
        self.install()
        p=self.target / '.codex/hooks.json';cfg=json.loads(p.read_text())
        cfg['hooks']['SessionStart'][0]['hooks'][0]['command']='echo my edit'
        p.write_text(json.dumps(cfg));before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'Edited Nebius hooks'):self.install()
        self.assertEqual(before,self.snapshot())

    def test_old_workspace_record_upgrades_and_preserves_notes(self):
        self.install()
        recordpath=self.target / doctor.RECORD
        record=json.loads(recordpath.read_text())
        record['files']={k:v for k,v in record['files'].items() if k in doctor.LEGACY_EXPECTED}
        record.pop('hook_files');record['version']='2.0.0-dev'
        recordpath.write_text(json.dumps(record))
        private=self.target / '.nebius-local';private.mkdir();(private/'STATE.md').write_text('private unchanged')
        self.install()
        self.assertEqual((private/'STATE.md').read_text(),'private unchanged')
        self.assertEqual(doctor.check(self.target)[0],[])

    def test_exact_reviewed_replacement_and_private_destination_rejected(self):
        self.install();p=self.target/'START_HERE.md';p.write_text('obsolete modified kit text')
        changes,before=kit.plan(SOURCE,self.target,replace_files=['START_HERE.md'])
        kit.apply_plan(self.target,changes,before)
        self.assertEqual(p.read_bytes(),(SOURCE/'templates/START_HERE.md').read_bytes())
        for path in ('.nebius-local/STATE.md','.claude/settings.json','../outside'):
            with self.assertRaises(ValueError):kit.plan(SOURCE,self.target,replace_files=[path])

    def legacy_fixture(self):
        source=self.source_copy();name='nebius-setup';old=b'synthetic old skill'
        known=json.loads((source/'scripts/legacy-hashes.json').read_text());known[name].append(doctor.digest(old))
        (source/'scripts/legacy-hashes.json').write_text(json.dumps(known))
        (source/'MANIFEST.sha256').write_text(kit.manifest_text(source))
        home=self.base/'synthetic home'
        for base in ('.codex/skills','.claude/skills','.agents/skills'):
            p=home/base/name/'SKILL.md';p.parent.mkdir(parents=True);p.write_bytes(old)
        return source,home

    def test_legacy_both_assistants_preview_apply_repeat(self):
        source,home=self.legacy_fixture()
        changes=legacy.plan(source,home)
        self.assertEqual(len(changes),3)
        self.assertTrue(all((home/r).read_bytes()==old for r,old,_ in changes))
        legacy.apply(home,changes)
        self.assertEqual(legacy.plan(source,home),[])
        self.assertFalse((home/'.claude/settings.json').exists())

    def test_legacy_unknown_edit_blocks_all_and_reviewed_override(self):
        source,home=self.legacy_fixture();p=home/'.claude/skills/nebius-setup/SKILL.md';p.write_text('user edit')
        with self.assertRaisesRegex(ValueError,'Modified global'):legacy.plan(source,home)
        changes=legacy.plan(source,home,replace=['nebius-setup']);self.assertEqual(len(changes),3)
        legacy.apply(home,changes)
        self.assertEqual(legacy.plan(source,home),[])

    def test_legacy_failure_rolls_back_and_concurrent_edit_preserved(self):
        source,home=self.legacy_fixture();changes=legacy.plan(source,home);real=legacy.atomic_write;calls=0
        def fail(path,data):
            nonlocal calls
            calls+=1
            if calls==2:raise OSError('disk failure')
            real(path,data)
        with patch.object(legacy,'atomic_write',side_effect=fail):
            with self.assertRaises(OSError):legacy.apply(home,changes)
        self.assertTrue(all((home/r).read_bytes()==old for r,old,_ in changes))
        (home/changes[0][0]).write_text('concurrent')
        with self.assertRaises(ValueError):legacy.apply(home,changes)
        self.assertEqual((home/changes[0][0]).read_text(),'concurrent')

    def test_legacy_symlink_refused(self):
        source,home=self.legacy_fixture();p=home/'.claude/skills/nebius-setup/SKILL.md'
        p.unlink();p.symlink_to(home/'.codex/skills/nebius-setup/SKILL.md')
        with self.assertRaises(ValueError):legacy.plan(source,home)

# Reuse setup/helpers without running inherited tests a second time.
for _name in list(vars(base_tests.BootstrapTests)):
    if _name.startswith('test_') and _name not in vars(HooksUpgradeTests):
        setattr(HooksUpgradeTests,_name,None)
