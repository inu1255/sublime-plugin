#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by inu1255
# Copyright (c) 2016 inu1255
#
# License: MIT
#

"""This module exports the Javalint plugin class."""

from SublimeLinter.lint import Linter, util


class Javalint(Linter):
    """Provides an interface to javalint."""

    syntax = 'java'
    executable = 'javac'
    version_args = '-version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 1.7'
    regex = (
        r'^(?P<file>.+?):(?P<line>\d+): '
        r'(?:(?P<error>错误)|(?P<warning>warning)): '
        r'(?:\[.+?\] )?(?P<message>[^\r\n]+)\r?\n'
        r'[^\r\n]+\r?\n'
        r'(?P<col>[^\^]*)\^'
    )
    multiline = True
    tempfile_suffix = '-'
    error_stream = util.STREAM_STDERR
    defaults = {
        'lint': ''
    }
    inline_settings = 'lint'
    comment_re = r'\s*/[/*]'

    def cmd(self):
        """
        Return the command line to execute.
        We override this because we have to munge the -Xlint argument
        based on the 'lint' setting.
        """

        xlint = '-Xlint'
        settings = self.get_view_settings()
        options = settings.get('lint')

        if options:
            xlint += ':' + options
        return (self.executable_path, xlint, '-encoding', 'UTF8')

    def split_match(self, match):
        """
        Return the components of the match.
        We override this because javac lints all referenced files,
        and we only want errors from the linted file.
        """

        if match:
            if match.group('file') != self.filename:
                match = None

        return super().split_match(match)