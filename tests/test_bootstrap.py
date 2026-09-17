"""Offline, synthetic filesystem cases. No company data or home writes."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(SOURCE / "scripts"))
import bootstrap as kit
import doctor
import package as kit_package


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=SOURCE / "tests")
        self.base = Path(self.temp.name)
        self.target = self.base / "colleague workspace"

    def tearDown(self):
        self.temp.cleanup()

    def install(self, integrate=False):
        changes, before = kit.plan(SOURCE, self.target, integrate)
        kit.apply_plan(self.target, changes, before)
        return changes

    def snapshot(self):
        return {str(p.relative_to(self.target)): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()} if self.target.exists() else {}

    def test_preview_never_creates_target(self):
        changes, _ = kit.plan(SOURCE, self.target)
        self.assertIn("AGENTS.md", changes)
        self.assertIn(".claude/skills/nebius-setup/SKILL.md", changes)
        self.assertFalse(self.target.exists())

    def test_fresh_install_both_assistants_and_doctor(self):
        self.install()
        self.assertEqual((self.target / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        for name in kit.SKILLS:
            self.assertEqual((self.target / f".agents/skills/{name}/SKILL.md").read_bytes(),
                             (self.target / f".claude/skills/{name}/SKILL.md").read_bytes())
        self.assertFalse((self.target / ".nebius-local/ROLE-MAP.md").exists())
        self.assertFalse((self.target / ".git").exists())
        run = subprocess.run([sys.executable, str(self.target / ".nebius-kit/doctor.py")],
                             cwd=self.base, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("NOT VERIFIED", run.stdout)

    def test_repeat_is_noop_keeps_install_date_and_user_context(self):
        self.install()
        private = self.target / ".nebius-local"
        private.mkdir()
        (private / "STATE.md").write_text("My own synthetic note\n")
        snapshot = self.snapshot()
        self.assertEqual(self.install(), {})
        self.assertEqual(snapshot, self.snapshot())

    def test_existing_instructions_block_whole_install(self):
        self.target.mkdir()
        (self.target / "AGENTS.md").write_text("Keep my instructions\n")
        snapshot = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Conflicts preserved"):
            kit.plan(SOURCE, self.target)
        self.assertEqual(snapshot, self.snapshot())

    def test_explicit_integration_preserves_instructions_and_repeats(self):
        self.target.mkdir()
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.target / name).write_text("My existing rules\n")
        (self.target / ".gitignore").write_text("mine\n")
        self.install(integrate=True)
        for name in ("AGENTS.md", "CLAUDE.md"):
            self.assertTrue((self.target / name).read_text().startswith("My existing rules\n"))
        self.assertTrue((self.target / ".gitignore").read_text().startswith("mine\n"))
        self.assertEqual(self.install(), {})

    def test_user_skill_edit_is_never_overwritten(self):
        self.install()
        path = self.target / ".claude/skills/nebius-ask/SKILL.md"
        path.write_text("My edits\n")
        snapshot = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Conflicts preserved"):
            self.install(integrate=True)
        self.assertEqual(snapshot, self.snapshot())
        self.assertTrue(doctor.check(self.target)[0])

    def test_missing_file_can_be_repaired(self):
        self.install()
        (self.target / "START_HERE.md").unlink()
        self.assertTrue(doctor.check(self.target)[0])
        self.install()
        self.assertEqual(doctor.check(self.target)[0], [])

    def test_symlinked_destination_is_refused(self):
        outside = self.base / "elsewhere"
        outside.mkdir()
        self.target.mkdir()
        (self.target / ".claude").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink refused"):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_symlinked_target_and_hardlinks_refused(self):
        outside = self.base / "elsewhere"
        outside.mkdir()
        self.target.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink refused"):
            self.install()
        self.target.unlink()
        self.target.mkdir()
        original = self.base / "original"
        original.write_text("private unrelated instructions")
        os.link(original, self.target / "AGENTS.md")
        with self.assertRaisesRegex(ValueError, "Hard-linked"):
            self.install(integrate=True)
        self.assertEqual(original.read_text(), "private unrelated instructions")

    def test_file_instead_of_directory_refused(self):
        self.target.mkdir()
        (self.target / ".agents").write_text("user file")
        with self.assertRaisesRegex(ValueError, "Not a directory"):
            self.install()
        self.assertEqual(self.snapshot(), {".agents": b"user file"})

    def test_write_failure_rolls_back_existing_and_new_files(self):
        self.target.mkdir()
        (self.target / "AGENTS.md").write_text("my rules")
        before_snapshot = self.snapshot()
        real = kit.atomic_write
        calls = 0
        def fail_once(path, data):
            nonlocal calls
            calls += 1
            if calls == 5:
                raise OSError("synthetic disk failure")
            real(path, data)
        with patch.object(kit, "atomic_write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "disk failure"):
                self.install(integrate=True)
        self.assertEqual(before_snapshot, self.snapshot())
        self.assertEqual([p.name for p in self.target.iterdir()], ["AGENTS.md"])

    def test_change_after_plan_is_preserved(self):
        self.install()
        (self.target / "START_HERE.md").unlink()
        changes, before = kit.plan(SOURCE, self.target)
        (self.target / "START_HERE.md").write_text("concurrent user note")
        with self.assertRaisesRegex(ValueError, "Changed during install"):
            kit.apply_plan(self.target, changes, before)
        self.assertEqual((self.target / "START_HERE.md").read_text(), "concurrent user note")

    def test_invalid_record_cannot_read_outside_workspace(self):
        self.install()
        record_path = self.target / doctor.RECORD
        record = json.loads(record_path.read_text())
        record["files"]["../../private"] = "0" * 64
        record_path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "Invalid install record"):
            doctor.check(self.target)

    def source_copy(self):
        source = self.base / "bundle"
        for name in kit.SOURCES | {"MANIFEST.sha256"}:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, path)
        return source

    def test_corrupt_source_fails_before_writes(self):
        source = self.source_copy()
        (source / "templates/AGENTS.md").write_text("corrupt")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            kit.plan(source, self.target)
        self.assertFalse(self.target.exists())

    def test_manifest_traversal_duplicate_and_incomplete_rejected(self):
        source = self.source_copy()
        path = source / "MANIFEST.sha256"
        original = path.read_text()
        cases = [original + "0"*64 + "  ../private\n",
                 original + original.splitlines()[1] + "\n",
                 "\n".join(original.splitlines()[:-1])]
        for case in cases:
            path.write_text(case)
            with self.assertRaisesRegex(ValueError, "manifest"):
                kit.plan(source, self.target)
        self.assertFalse(self.target.exists())

    def test_upgrade_preserves_private_notes_and_integrated_prefix(self):
        self.target.mkdir()
        (self.target / "AGENTS.md").write_text("My rules\n")
        self.install(integrate=True)
        source = self.source_copy()
        path = source / "templates/AGENTS.md"
        path.write_text(path.read_text() + "\nNew kit version\n")
        (source / "MANIFEST.sha256").write_text(kit.manifest_text(source))
        changes, before = kit.plan(source, self.target)
        kit.apply_plan(self.target, changes, before)
        text = (self.target / "AGENTS.md").read_text()
        self.assertTrue(text.startswith("My rules\n"))
        self.assertIn("New kit version", text)
        self.assertEqual(text.count("nebius-ai-kit:start"), 1)

    def test_git_ignore_works_and_tracked_private_data_is_detected(self):
        self.install()
        subprocess.run(["git", "init", "-q", str(self.target)], check=True)
        private = self.target / ".nebius-local"
        private.mkdir()
        (private / "STATE.md").write_text("synthetic note")
        self.assertEqual(doctor.check(self.target)[0], [])
        subprocess.run(["git", "-C", str(self.target), "add", "-f", ".nebius-local/STATE.md"], check=True)
        self.assertTrue(any("tracked" in err for err in doctor.check(self.target)[0]))

    def test_postcheck_failure_rolls_back(self):
        with patch.object(kit, "check", return_value=(["synthetic failed check"], [])):
            with self.assertRaisesRegex(ValueError, "Post-install"):
                self.install()
        self.assertFalse(self.target.exists())

    def test_override_blocks_readiness_without_touching_user_file(self):
        self.target.mkdir()
        (self.target / "AGENTS.override.md").write_text("existing override")
        with self.assertRaisesRegex(ValueError, "shadows AGENTS.md"):
            self.install()
        self.assertEqual(self.snapshot(), {"AGENTS.override.md": b"existing override"})

    def test_cli_preview_and_global_config_guard(self):
        run = subprocess.run([sys.executable, str(SOURCE / "scripts/bootstrap.py"),
                              "init", "--workspace", str(self.target)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(self.target.exists())
        run = subprocess.run([sys.executable, str(SOURCE / "scripts/bootstrap.py"),
                              "init", "--workspace", str(Path.home() / ".codex/kit")],
                             capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("outside global", run.stderr)

    def test_missing_git_in_repository_fails_before_any_write(self):
        with patch.object(doctor, "repository_present", return_value=True), \
                patch.object(doctor.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaisesRegex(ValueError, "Git unavailable"):
                kit.plan(SOURCE, self.target)
        self.assertFalse(self.target.exists())

    def test_standalone_workspace_needs_no_git(self):
        # Filesystem repo detection is mocked because fixtures live inside this repo.
        with patch.object(doctor, "repository_present", return_value=False), \
                patch.object(doctor.subprocess, "run", side_effect=AssertionError("Git must not run")):
            self.install()
            errors, notes = doctor.check(self.target)
            self.assertEqual(errors, [])
            self.assertTrue(any("not applicable" in note for note in notes))

    def test_git_timeout_and_broken_mac_shim_fail_before_writes(self):
        for outcome, expected in ((subprocess.TimeoutExpired("git", 15), "15 seconds"),
                                  (subprocess.CompletedProcess(["git"], 1), "cannot run")):
            with patch.object(doctor, "repository_present", return_value=True):
                if isinstance(outcome, Exception):
                    mock = patch.object(doctor.subprocess, "run", side_effect=outcome)
                else:
                    mock = patch.object(doctor.subprocess, "run", return_value=outcome)
                with mock, self.assertRaisesRegex(ValueError, expected):
                    kit.plan(SOURCE, self.target)
            self.assertFalse(self.target.exists())

    def test_private_subdirectory_symlinks_and_extra_hardlinks_refused(self):
        self.install()
        local = self.target / ".nebius-local"
        local.mkdir()
        outside = self.base / "outside"
        outside.mkdir()
        link = local / "notes"
        link.symlink_to(outside, target_is_directory=True)
        self.assertTrue(any("symlink" in e for e in doctor.check(self.target)[0]))
        link.unlink()
        note = self.base / "synthetic-note"
        note.write_text("synthetic private preference")
        os.link(note, local / "other.md")
        with self.assertRaisesRegex(ValueError, "Hard-linked"):
            doctor.check(self.target)

    def test_copied_bundle_cli_from_another_directory(self):
        source = self.source_copy()
        for extra in ([], ["--apply"], ["--apply"]):
            run = subprocess.run([sys.executable, str(source / "scripts/bootstrap.py"),
                                  "init", "--workspace", str(self.target), *extra],
                                 cwd=self.base, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("no files changed", run.stdout)
        shutil.rmtree(source)
        run = subprocess.run([sys.executable, str(self.target / ".nebius-kit/doctor.py")],
                             cwd=self.base, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_dangling_git_directory_never_passes_privacy(self):
        self.target.mkdir()
        (self.target / ".git").symlink_to(self.base / "missing-git", target_is_directory=True)
        self.assertTrue(doctor.repository_present(self.target))
        failed = subprocess.CompletedProcess(["git"], 128, stdout="", stderr="")
        original_exists = Path.exists
        # Hide the enclosing test repository so only the dangling marker remains.
        with patch.object(Path, "exists", autospec=True,
                          side_effect=lambda p: False if p.name == ".git" else original_exists(p)), \
                patch.object(doctor, "run_git", return_value=failed):
            self.assertEqual(doctor.git_privacy(self.target), ["Git repository could not be inspected"])

    def test_git_environment_overrides_cannot_hide_private_tracking(self):
        for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
                     "GIT_CONFIG_COUNT", "GIT_CONFIG_VALUE_0"):
            with patch.dict(os.environ, {name: "synthetic-sensitive-value"}):
                with self.assertRaisesRegex(ValueError, name) as raised:
                    kit.plan(SOURCE, self.target)
                self.assertNotIn("synthetic-sensitive-value", str(raised.exception))
                with self.assertRaisesRegex(ValueError, name):
                    doctor.git_privacy(self.target)
            self.assertFalse(self.target.exists())

    def package_source(self):
        source = self.source_copy()
        for name in kit_package.EXTRAS - {doctor.RECORD, ".gitignore", "MANIFEST.sha256"}:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, path)
        changes, before = kit.plan(source, source)
        kit.apply_plan(source, changes, before)
        return source

    def test_archive_allowlist_and_extracted_verification(self):
        source = self.package_source()
        canary = "synthetic-private-" + os.urandom(16).hex()
        private = source / ".nebius-local"
        private.mkdir()
        (private / "STATE.md").write_text(canary)
        (source / ".claude/settings.json").write_text(json.dumps({"synthetic": canary}))
        (source / "unlisted.txt").write_text(canary)
        output = source / "dist/test.zip"
        self.assertEqual(kit_package.build_archive(source, output), len(kit_package.FILES))
        extracted = self.base / "extracted colleague workspace"
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(set(archive.namelist()), kit_package.FILES)
            self.assertIn(".claude/skills/nebius-setup/SKILL.md", archive.namelist())
            self.assertIn(".agents/skills/nebius-setup/SKILL.md", archive.namelist())
            self.assertFalse(any(canary.encode() in archive.read(n) for n in archive.namelist()))
            archive.extractall(extracted)
        run = subprocess.run([sys.executable, str(extracted / "scripts/bootstrap.py"), "verify"],
                             cwd=self.base, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        with self.assertRaisesRegex(ValueError, "already exists"):
            kit_package.build_archive(source, output)

    def test_archive_rejects_stale_generated_files_before_output(self):
        source = self.package_source()
        (source / "START_HERE.md").write_text("unreviewed edit")
        output = source / "dist/test.zip"
        with self.assertRaisesRegex(ValueError, "Changed"):
            kit_package.build_archive(source, output)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
