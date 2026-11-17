"""Every workflow declares the permissions it runs with (WP82: the default workflow permissions
are read, so a job that writes names the write; a job without its own inherits the workflow's)."""

from pathlib import Path

import pytest
import yaml

WORKFLOWS = sorted((Path(__file__).resolve().parent.parent / ".github" / "workflows").glob("*.yml"))


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda p: p.name)
def test_every_job_has_declared_permissions(path):
    wf = yaml.safe_load(path.read_text(encoding="utf-8"))
    top = wf.get("permissions")
    for job_id, job in wf["jobs"].items():
        perms = job.get("permissions", top)
        assert isinstance(perms, dict) and perms, (path.name, job_id)
        assert all(v in ("read", "write") for v in perms.values()), (path.name, job_id)
    if top is not None:  # the workflow's own line never writes contents; a job that must says so
        assert top.get("contents") == "read", path.name
