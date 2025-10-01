#
# (c) 2025 Yoichi Tanibayashi
#
"""CLI base"""

import os
import readline

from .my_logger import errmsg, get_logger


class CliBase:
    """CLI base class"""

    PROMPT_STR = "> "
    COMMENT_STR = "#"
    SPECIAL_COMMAND_PREFIX = ":"

    HIST_LEN = 500

    def __init__(
        self, prompt_prefix: str, history_file: str, infile=None, debug=False
    ):
        """Contractor."""
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug(
            "prompt_prefix=%s, history_file=%s, infile=%s",
            prompt_prefix,
            history_file,
            infile,
        )

        self.prompt_prefix = prompt_prefix

        self.history_file = os.path.expanduser(
            os.path.expandvars(history_file)
        )
        self.__log.debug("history_file=%a", self.history_file)

        if infile:
            self.infile = os.path.expanduser(os.path.expandvars(infile))
            self.__log.debug("infile=%a", self.infile)

        try:
            readline.read_history_file(self.history_file)
            readline.set_history_length(self.HIST_LEN)
            self.__log.debug("hist_len=%s", readline.get_history_length())
            self.__log.debug(
                "cur_hist_len=%s", readline.get_current_history_length()
            )
        except FileNotFoundError:
            self.__log.debug("no history file: %s", self.history_file)
        except OSError:
            self.__log.warning(
                "invalid history file .. remove: %s", self.history_file
            )
            # ヒストリーファイルが壊れていると思われるので削除する。
            os.remove(self.history_file)
        except Exception as _e:
            self.__log.error("%s: %s", type(_e).__name__, _e)

    def end(self):
        """End."""
        self.__log.debug("save history: %s", self.history_file)
        try:
            readline.write_history_file(self.history_file)
        except Exception as _e:
            self.__log.error(f"{self.history_file!r}: {errmsg(_e)}")
        self.__log.debug("done")

    def exec(self, line: str) -> str:
        """Send line.
        **TO BE OVERRIDE**

        エラー時には、""(空文字列)を返すようにすること。
        """
        self.__log.debug("line=%a", line)
        if line == "*** error ***":
            return ""

        return f"exec {line}"

    def parse_line(self, line: str) -> str:
        """Parse line.
        **TO BE OVERRIDE**
        """
        self.__log.debug("line=%a", line)
        return f"*** {line} ***"

    def handle_special(self, line: str):
        """Handle special command."""
        self.__log.debug("line=%a", line)
        self.__log.info("**WIP**: macro etc.")
        return

    def process_line(self, line: str):
        """Process the line."""
        self.__log.debug("line=%a", line)

        if not line:
            return True

        if line.startswith(self.COMMENT_STR):
            self.__log.debug("comment line: ignored")
            return True

        if line.startswith(self.SPECIAL_COMMAND_PREFIX):
            self.handle_special(line)
            return True

        _parsed_line = self.parse_line(line)
        self.__log.debug("parsed_line=%a", _parsed_line)
        if not _parsed_line:
            self.__log.warning("parse error: ignored")
            return True

        try:
            result = self.exec(_parsed_line)
            if not result:
                print("[ERROR]")
            else:
                print(result)
        except Exception as _e:
            self.__log.warning(errmsg(_e))
            return False

        return True

    def loop(self):
        """loop"""
        try:
            while True:
                try:
                    _line = input(self.prompt_prefix + self.PROMPT_STR)
                    _line = _line.strip()
                    self.__log.debug("line=%a", _line)
                    # readline.write_history_file(self.history_file)
                except EOFError as _e:
                    print(" [EOF]")
                    self.__log.debug(errmsg(_e))
                    break

                if self.process_line(_line):
                    continue
                else:
                    break

        except KeyboardInterrupt as _e:
            print("^C")
            self.__log.debug(errmsg(_e))

        finally:
            self.end()

    def run_file(self, infile=""):
        """Run command file."""
        if not infile:
            infile = self.infile
        self.__log.debug("infile=%a", self.infile)
        if not self.infile:
            return

        with open(self.infile, "r") as f:
            for _line in f:
                _line = _line.strip()
                self.__log.debug("line=%a", _line)

                if self.process_line(_line):
                    continue
                else:
                    break
        self.end()
