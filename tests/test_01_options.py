# tests/test_00_conftest.py
#
# `conftest.py` の動作確認用テストプログラム
#
# `cli_runner`: conftest.pyで定義されたフィクスチャー
#
import subprocess

import pytest

CMDNAME = "pyclibase"
HISTFILE = "/tmp/hist"

CMDLINE = "uv run " + CMDNAME


class TestOptions:
    """基本的なコマンドのテスト。"""

    @pytest.mark.parametrize(
        "opts, retcode, expected_stdout, expected_stderr",
        [
            ("-V", 0, [f"{CMDNAME}"], []),
            ("-h", 0, ["Usage: ", "Options:"], []),
            ("-x", 2, [], ["Usage: ", "Error: "]),
        ],
    )
    def test_options(self, opts, retcode, expected_stdout, expected_stderr):
        """Test command options."""
        cmdline = CMDLINE + " " + opts
        print(f"\n\n## cmdline = {cmdline}")

        result = subprocess.run(
            cmdline.split(), capture_output=True, text=True
        )

        print(f"## returncode> {result.returncode} == {retcode}")
        assert result.returncode == retcode

        print(f"## stdout\n{result.stdout.rstrip()}")
        for s in expected_stdout:
            print(f"### expecte:{s!r}")
            assert s in result.stdout

        print(f"## stderr\n{result.stderr.rstrip()}")
        for s in expected_stderr:
            print(f"### expecte:{s!r}")
            assert s in result.stderr
