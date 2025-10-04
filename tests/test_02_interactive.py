# tests/test_00_conftest.py
#
# `conftest.py` の動作確認用テストプログラム
#
# `cli_runner`: conftest.pyで定義されたフィクスチャー
#
import pytest

from tests.conftest import KEY_EOF

CMDNAME = "pyclibase"
CMDLINE = "uv run " + CMDNAME


class TestInteractive:
    """基本的なコマンドのテスト。"""

    @pytest.mark.parametrize(
        "opts, e_stdout, e_stderr, in_out, terminate_flag, e_ret",
        [
            (
                "",  # 起動時オプション
                [f"{CMDNAME}>"],
                [],  # 起動直後の出力
                [
                    {  # 入力とそれに対応する出力
                        "in": "aaa\n",
                        "out": ["result", "*** aaa ***"],
                    }
                ],
                True,  # 強制終了するかどうか
                143,  # returncode
            ),
            (
                "",
                [f"{CMDNAME}>"],
                [],
                [
                    {"in": "bbb\n", "out": ["result", "*** bbb ***"]},
                    {"in": KEY_EOF, "out": ["EOF"]},
                ],
                False,
                0,
            ),
            (
                "-d",
                ["DEBUG", f"{CMDNAME}>"],
                [],
                [
                    {
                        "in": "ccc\n",
                        "out": ["DEBUG", "result", "*** ccc ***"],
                    },
                    {
                        "in": KEY_EOF,
                        "out": ["EOF", "DEBUG", "EOFError", "done"],
                    },
                ],
                False,
                0,
            ),
        ],
    )
    def test_interactive(
        self,
        cli_runner,
        opts,
        e_stdout,
        e_stderr,
        in_out,
        terminate_flag,
        e_ret,
    ):
        """Test interactive."""
        cli_runner.test_interactive(
            CMDLINE, opts, e_stdout, e_stderr, in_out, terminate_flag, e_ret
        )
