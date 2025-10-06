# tests/test_00_conftest.py
#
# `conftest.py` の動作確認用テストプログラム
#
# `cli_runner`: conftest.pyで定義されたフィクスチャー
#
import pytest

CMDNAME = "pyclibase"
HISTFILE = "/tmp/hist"

CMDLINE = "uv run " + CMDNAME


class TestOptions:
    """基本的なコマンドのテスト。"""

    @pytest.mark.parametrize(
        "opts, e_stdout, e_stderr, e_ret",
        [
            ("-V", [f"{CMDNAME}"], [], 0),
            ("-h", [f"Usage: {CMDNAME}", "Options:", "--help"], [], 0),
            ("-x", [], [f"Usage: {CMDNAME}", "Error: No such option:"], 2),
        ],
    )
    def test_command(self, cli_runner, opts, e_stdout, e_stderr, e_ret):
        """Test command options."""
        cli_runner.test_command(
            CMDLINE, opts, e_stdout=e_stdout, e_stderr=e_stderr, e_ret=e_ret
        )
