from nox import Session, options
from nox_uv import session

options.default_venv_backend = "uv"
options.sessions = ["lint", "tests"]


@session(uv_groups=["dev"])
def lint(session: Session) -> None:
    session.run("ruff", "check")
    session.run("ruff", "format", "--check")
    session.run("ty", "check")


@session(uv_groups=["dev"])
def fix(session: Session) -> None:
    session.run("ruff", "check", "--fix")
    session.run("ruff", "format")


@session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], uv_groups=["dev"])
def tests(session: Session) -> None:
    session.run("pytest")


