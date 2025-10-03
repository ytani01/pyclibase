# tests/test_00_conftest.py
#
# `conftest.py` の動作確認用テストプログラム
#
# `cli_runner`: conftest.pyで定義されたフィクスチャー
#
import os
import pty
import select
import subprocess
import time

import pytest

CMDNAME = "pyclibase"
HISTFILE = "/tmp/hist"

CMDLINE = "uv run " + CMDNAME

KEY_EOF = "\x04"


class InteractiveSession:
    """Interactive session."""

    def __init__(self, master_fd, process):
        """Constractor."""
        self.master_fd = master_fd
        self.process = process
        self.output = ""

    def send_key(self, key: str):
        """Sends a key press to the process."""
        os.write(self.master_fd, key.encode())

    def expect(self, pattern: str | list[str], timeout: float = 5.0) -> bool:
        """Waits for a pattern to appear in the output."""
        if isinstance(pattern, str):
            pattern = [pattern]

        start_time = time.time()
        while time.time() - start_time < timeout:
            r, _, _ = select.select([self.master_fd], [], [], 0.1)
            if r:
                try:
                    data = os.read(self.master_fd, 1024).decode()
                    self.output += data
                    # print(f"### Current output: \n{self.output}")
                    print(f" >>> {data!r}")
                    true_count = 0
                    for p in pattern:
                        if p in self.output:
                            true_count += 1
                    if true_count == len(pattern):
                        return True
                except OSError:
                    break
        return False

    def close(self):
        """Terminates the process and closes the file descriptor."""
        ret = None
        for _ in range(3):
            print("* poll")
            ret = self.process.poll()
            if isinstance(ret, int):
                print(f"ret={ret}")
                break
            time.sleep(0.5)

        if ret is None:
            print("* terminate")
            self.process.terminate()
            ret = self.process.wait()
            print(f"ret={ret}")

        os.close(self.master_fd)
        return ret


class TestInteractive:
    """基本的なコマンドのテスト。"""

    @pytest.mark.parametrize(
        "opts, expected_stdout, expected_stderr, in_out, retcode",
        [
            (
                "",
                [f"{CMDNAME}>"],
                [],
                [
                    {"in": "aaa\n", "out": ["result", "*** aaa ***"]},
                ],
                143,  # terminate
            ),
            (
                "",
                [f"{CMDNAME}>"],
                [],
                [
                    {"in": "bbb\n", "out": ["result", "*** bbb ***"]},
                    {"in": KEY_EOF, "out": ["EOF"]},
                ],
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
                0,
            ),
        ],
    )
    def test_interactive(
        self, opts, expected_stdout, expected_stderr, in_out, retcode
    ):
        """Test interactive."""
        master_fd, slave_fd = pty.openpty()

        cmdline = CMDLINE + " " + opts
        print(f"\n\n# cmdline = {cmdline}")

        process = subprocess.Popen(
            cmdline.split(),
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
        )
        os.close(slave_fd)

        session = InteractiveSession(master_fd, process)

        if expected_stdout:
            print(f"## expected={expected_stdout}")
            assert session.expect(expected_stdout)

        if expected_stderr:
            print(f"## expected={expected_stderr}")
            assert session.expect(expected_stderr)

        for _inout in in_out:
            print(f"## in={_inout['in']!r}")
            session.send_key(_inout["in"])
            print(f"## expect={_inout['out']}")
            assert session.expect(_inout["out"])
            time.sleep(1)

        ret = session.close()
        if isinstance(retcode, int):
            assert ret == retcode
