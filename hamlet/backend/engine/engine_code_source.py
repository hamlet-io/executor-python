import shutil
import subprocess


class EngineCodeSourceBuildData:
    """
    Provides utility functions that generate version details about
    an engine source as part of its build process
    """

    def _git_path(self):
        return shutil.which("git")

    def __init__(self, path):
        self.path = path

    def _is_git_repo(self):
        try:
            subprocess.check_output(
                [
                    self._git_path(),
                    "rev-parse",
                    "--is-inside-work-tree",
                ],
                cwd=self.path,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            return False

        return True

    def _git_current_revision(self):
        return subprocess.check_output(
            [
                self._git_path(),
                "rev-parse",
                "HEAD",
            ],
            cwd=self.path,
            text=True,
        ).strip()

    def _git_current_tag(self):
        return subprocess.check_output(
            [
                self._git_path(),
                "tag",
                "--points-at",
                "HEAD",
            ],
            cwd=self.path,
            text=True,
        ).strip()

    def _git_current_origin(self):
        return subprocess.check_output(
            [
                self._git_path(),
                "remote",
                "get-url",
                "origin",
            ],
            cwd=self.path,
            text=True,
        ).strip()

    @property
    def details(self):

        details = {}

        if self._is_git_repo():
            details["code_source"] = {
                "provider": "git",
                "revision": self._git_current_revision(),
                "tag": self._git_current_tag(),
                "origin": self._git_current_origin(),
            }

        return details
