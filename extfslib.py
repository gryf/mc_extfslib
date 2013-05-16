"""
extfslib is a library which contains Archive class to support writing extfs
plugins for Midnight Commander.

Tested against python 2.7 and mc 4.8.7

Changelog:
    1.1 Added item pattern, and common git/uid attrs
    1.0 Initial release

Author: Roman 'gryf' Dobosz <gryf73@gmail.com>
Date: 2013-05-12
Version: 1.1
Licence: BSD
"""
import os
import sys
import re
from subprocess import check_output, CalledProcessError


class Archive(object):
    """Archive handle. Provides interface to MC's extfs subsystem"""
    LINE_PAT = re.compile("^(?P<size>)\s"
                          "(?P<perms>)\s"
                          "(?P<uid>)\s"
                          "(?P<gid>)\s"
                          "(?P<date>)\s+"
                          "(?P<time>)\s"
                          "(?P<fpath>)")
    ARCHIVER = "archiver_name"
    CMDS = {"list": "l",
            "read": "r",
            "write": "w",
            "delete": "d"}
    ITEM = ("%(perms)s   1 %(uid)-8s %(gid)-8s %(size)8s %(datetime)s "
            "%(display_name)s\n")

    def __init__(self, fname):
        """Prepare archive content for operations"""
        if not os.path.exists(fname):
            raise OSError("No such file or directory `%s'" % fname)
        self._uid = os.getuid()
        self._gid = os.getgid()
        self._arch = fname
        self._contents = self._get_dir()

    def _map_name(self, name):
        """MC still have a bug in extfs subsystem, in case of filepaths with
        leading space. This is workaround to this bug, which replaces leading
        space with tilda."""
        if name.startswith(" "):
            new_name = "".join(["~", name[1:]])
            return new_name
        return name

    def _get_real_name(self, name):
        """Get real filepath of the file. See _map_name docstring for
        details."""
        for item in self._contents:
            if item['display_name'] == name:
                return item['fpath']
        return None

    def _get_dir(self):
        """Prepare archive file listing. Expected keys which every entry
        should have are: size, perms, uid, gid, date, time, fpath and
        display_name."""
        contents = []

        out = self._call_command("list")
        if not out:
            return

        for line in out.split("\n"):
            match = self.LINE_PAT.match(line)
            if not match:
                continue
            entry = match.groupdict()
            contents.append(entry)

        return contents

    def _call_command(self, cmd, src=None, dst=None):
        """
        Return status of the provided command, which can be one of:
            write
            read
            delete
            list
        """
        command = [self.ARCHIVER, self.CMDS.get(cmd), self._arch]

        if src and dst:
            command.append(src)
            command.append(dst)
        elif src or dst:
            command.append(src and src or dst)

        try:
            output = check_output(command)
        except CalledProcessError:
            sys.exit(1)
        return output

    def list(self):
        """Output contents of the archive to stdout"""
        sys.stderr.write("Not supported")
        return 1

    def run(self, dst):
        """Execute file out of archive"""
        sys.stderr.write("Not supported")
        return 1

    def copyout(self, src, dst):
        """Copy file out of archive"""
        sys.stderr.write("Not supported")
        return 1

    def rm(self, dst):
        """Remove file from archive"""
        sys.stderr.write("Not supported")
        return 1

    def mkdir(self, dst):
        """Create empty directory in archive"""
        sys.stderr.write("Not supported")
        return 1

    def rmdir(self, dst):
        """Removes directory from archive"""
        sys.stderr.write("Not supported")
        return 1

    def copyin(self, dst, src=None):
        """Copy file to the archive"""
        sys.stderr.write("Not supported")
        return 1


def usage():
    """Print out usage information"""
    print ("Usage: %(prg)s {copyin,copyout} ARCHNAME SOURCE DESTINATION\n"
           "or: %(prg)s list ARCHNAME\n"
           "or: %(prg)s {mkdir,rm,rmdir,run} ARCHNAME TARGET" %
           {"prg": sys.argv[0]})


def parse_args(arch_class):
    """Retrive and parse arguments from commandline and apply them into passed
    arch_class class object."""
    try:
        if sys.argv[1] not in ('list', 'copyin', 'copyout', 'rm', 'mkdir',
                               "run", "rmdir"):
            usage()
            sys.exit(2)
    except IndexError:
        usage()
        sys.exit(2)

    arch = src = dst = None
    try:
        arch = sys.argv[2]
        if sys.argv[1] in ('copyin', 'copyout'):
            src = sys.argv[3]
            dst = sys.argv[4]
        elif sys.argv[1] in ('rm', 'rmdir', 'run', 'mkdir'):
            dst = sys.argv[3]
    except IndexError:
        usage()
        sys.exit(2)

    call_map = {'copyin': lambda a, s, d: arch_class(a).copyin(s, d),
                'copyout': lambda a, s, d: arch_class(a).copyout(s, d),
                'list': lambda a, s, d: arch_class(a).list(),
                'mkdir': lambda a, s, d: arch_class(a).mkdir(d),
                'rm': lambda a, s, d: arch_class(a).rm(d),
                'rmdir': lambda a, s, d: arch_class(a).rmdir(d),
                'run': lambda a, s, d: arch_class(a).run(d)}

    return call_map[sys.argv[1]](arch, src, dst)
