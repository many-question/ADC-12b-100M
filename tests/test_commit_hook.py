"""Run the real Git hook with a competing adcflow on PYTHONPATH."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


@pytest.mark.parametrize("reject_local", [False, True])
def test_hook_checks_committing_checkout(tmp_path, reject_local):
    git = shutil.which("git")
    if git is None:
        pytest.skip("Git is required to exercise its hook invocation")
    root = tmp_path / "committing checkout"
    root.mkdir()
    hook = root / "tools" / "hooks" / "pre-commit"
    hook.parent.mkdir(parents=True)
    shutil.copyfile(Path(__file__).resolve().parents[1] / "tools/hooks/pre-commit", hook)
    hook.chmod(0o755)
    local = root / "tools" / "adcflow"
    local.mkdir()
    (local / "__init__.py").write_text("", encoding="utf-8")
    (local / "__main__.py").write_text(
        "from pathlib import Path\nimport sys\n"
        "with Path('hook-calls.txt').open('a') as f:\n"
        "    f.write(' '.join(sys.argv[1:]) + '\\n')\n"
        f"sys.exit({int(reject_local)})\n", encoding="utf-8",
    )
    foreign = tmp_path / "other checkout" / "tools" / "adcflow"
    foreign.mkdir(parents=True)
    (foreign / "__init__.py").write_text("", encoding="utf-8")
    (foreign / "__main__.py").write_text(
        "raise SystemExit('WRONG CHECKOUT IMPORTED')\n", encoding="utf-8",
    )
    env = os.environ.copy()
    # Do not inherit the enclosing commit's index/repository into this test repo.
    for key in tuple(env):
        if key.startswith("GIT_"):
            env.pop(key)
    env["PYTHONPATH"] = str(foreign.parent)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    subprocess.run([git, "init", "--quiet", str(root)], env=env, check=True)
    result = subprocess.run(
        [git, "-C", str(root), "-c", "core.hooksPath=tools/hooks",
         "-c", "user.name=Hook Test", "-c", "user.email=hook@example.invalid",
         "commit", "--allow-empty", "--no-gpg-sign", "-m", "Exercise hook"],
        env=env, capture_output=True, text=True,
    )
    assert "WRONG CHECKOUT IMPORTED" not in result.stdout + result.stderr
    assert (result.returncode != 0) == reject_local, result.stdout + result.stderr
    expected = ["check hygiene"] if reject_local else ["check hygiene", "check ports", "gen --check"]
    assert (root / "hook-calls.txt").read_text().splitlines() == expected
