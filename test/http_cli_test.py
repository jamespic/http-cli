import pytest

from http_cli import main as run_http_cli


def test_happy_path(server: str, capsys: pytest.CaptureFixture[str]) -> None:
    url = f"{server}/test"
    result = run_http_cli([url])
    assert result == 0
    captured = capsys.readouterr()
    assert '"url": "/test"' in captured.out


def test_404_response(server: str, capsys: pytest.CaptureFixture[str]) -> None:
    url = f"{server}/notfound"
    result = run_http_cli(["-v", "-H", "Mock-Status: 404 Not Found", url])
    assert result == 1
    captured = capsys.readouterr()
    assert '"url": "/notfound"' in captured.out
    assert "< HTTP/1.1 404 Not Found" in captured.err


def test_post_request(server: str, capsys: pytest.CaptureFixture[str]) -> None:
    url = f"{server}/submit"
    data = "key=value"
    result = run_http_cli(["-X", "POST", "-d", data, url])
    assert result == 0
    captured = capsys.readouterr()
    assert '"method": "POST"' in captured.out
    assert '"body": "key=value"' in captured.out


def test_https(https_server: str, capsys: pytest.CaptureFixture[str]) -> None:
    url = f"{https_server}/get"
    result = run_http_cli(["-k", url])
    assert result == 0
    captured = capsys.readouterr()
    assert '"url": "/get"' in captured.out
