"""
extfslib is a library which contains Archive class to support writing extfs
plugins for Midnight Commander.

Tested against python 3.11 and mc 4.8.29

Changelog:
    1.4 Detect byts/string, and load config by default
    1.3 Added ability to read config from mc/ini file.
    1.2 Switch to python3
    1.1 Added item pattern, and common git/uid attrs
    1.0 Initial release

Author: Roman 'gryf' Dobosz <gryf73@gmail.com>
Date: 2023-10-22
Version: 1.4
Licence: BSD
"""
import argparse
import configparser
import os
import re
import subprocess
import sys

XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))


class Config:
    """An optional config class, a helper to get and parse MC ini file"""

    def __init__(self, caller):
        self._config = self._get_config()
        self._class_name = caller.__class__.__name__.lower()

    def _get_config(self):
        """Read MC main config file"""
        conf_file = os.path.join(XDG_CONF_DIR, 'mc/ini')
        conf_parser = configparser.ConfigParser()
        conf_parser.read(conf_file)
        return conf_parser

    def getboolean(self, name):
        try:
            return self._config.getboolean(self._class_name, name)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def getint(self, name):
        try:
            return self._config.getint(self._class_name, name)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def getfloat(self, name):
        try:
            return self._config.getfloat(self._class_name, name)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def get(self, name):
        return getattr(self, name)

    def __getattr__(self, name):
        try:
            return self._config.get(self._class_name, name)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass


class Archive(object):
    """Archive handle. Provides interface to MC's extfs subsystem"""
    LINE_PAT = re.compile(br"^(?P<size>)\s"
                          br"(?P<perms>)\s"
                          br"(?P<uid>)\s"
                          br"(?P<gid>)\s"
                          br"(?P<date>)\s+"
                          br"(?P<time>)\s"
                          br"(?P<fpath>)")
    ARCHIVER = b"archiver_name"
    CMDS = {"list": b"l",
            "read": b"r",
            "write": b"w",
            "delete": b"d"}
    ITEM = (b"%(perms)s   1 %(uid)-8s %(gid)-8s %(size)8s %(datetime)s "
            b"%(display_name)s\n")

    def __init__(self, fname):
        """Prepare archive content for operations"""
        if not os.path.exists(fname):
            raise OSError("No such file or directory `%s'" % fname)
        self._uid = os.getuid()
        self._gid = os.getgid()
        self._arch = fname
        self.name_map = {}
        self._contents = self._get_dir()
        self.config = Config(self)

    def _map_name(self, name):
        """MC still have a bug in extfs subsystem, in case of filepaths with
        leading space. This is workaround to this bug, which replaces leading
        space with tilda."""
        if isinstance(name, bytes):
            if name.startswith(b" "):
                new_name = b"".join([b"~", name[1:]])
                return new_name
        else:
            if name.startswith(" "):
                new_name = "".join(["~", name[1:]])
                return new_name
        return name

    def _get_real_name(self, name):
        """Get real filepath of the file. See _map_name docstring for
        details."""
        for item in self._contents:
            if isinstance(name, bytes):
                if item[b'display_name'] == name.encode('utf-8',
                                                        'surrogateescape'):
                    return item[b'fpath']
            else:
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

        for line in out.split(b"\n"):
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
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError:
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
    print("Usage: %(prg)s {copyin,copyout} ARCHNAME SOURCE DESTINATION\n"
          "or: %(prg)s list ARCHNAME\n"
          "or: %(prg)s {mkdir,rm,rmdir,run} ARCHNAME TARGET" %
          {"prg": sys.argv[0]})


def _parse_args(arch_class):
    """Use ArgumentParser to check for script arguments and execute."""

    CALL_MAP = {'list': lambda a: arch_class(a.arch).list(),
                'copyin': lambda a: arch_class(a.arch).copyin(a.src, a.dst),
                'copyout': lambda a: arch_class(a.arch).copyout(a.src, a.dst),
                'mkdir': lambda a: arch_class(a.arch).mkdir(a.dst),
                'rm': lambda a: arch_class(a.arch).rm(a.dst),
                'run': lambda a: arch_class(a.arch).run(a.dst)}

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='supported commands')
    parser_list = subparsers.add_parser('list', help="List contents of "
                                        "archive")
    parser_copyin = subparsers.add_parser('copyin', help="Copy file into "
                                          "archive")
    parser_copyout = subparsers.add_parser('copyout', help="Copy file out of "
                                           "archive")
    parser_rm = subparsers.add_parser('rm', help="Delete file from archive")
    parser_mkdir = subparsers.add_parser('mkdir', help="Create directory in "
                                         "archive")
    parser_run = subparsers.add_parser('run', help="Execute archived file")

    parser_list.add_argument('arch', help="Archive filename")
    parser_list.set_defaults(func=CALL_MAP['list'])

    parser_copyin.add_argument('arch', help="Archive filename")
    parser_copyin.add_argument('src', help="Source filename")
    parser_copyin.add_argument('dst', help="Destination filename (to be "
                               "written into archive)")
    parser_copyin.set_defaults(func=CALL_MAP['copyin'])

    parser_copyout.add_argument('arch', help="archive or image filename")
    parser_copyout.add_argument('src', help="Source filename (to be read from"
                                " archive")
    parser_copyout.add_argument('dst', help="Destination filename")
    parser_copyout.set_defaults(func=CALL_MAP['copyout'])

    parser_rm.add_argument('arch', help="archive or image filename")
    parser_rm.add_argument('dst', help="File inside archive to be deleted")
    parser_rm.set_defaults(func=CALL_MAP['rm'])

    parser_mkdir.add_argument('arch', help="archive filename")
    parser_mkdir.add_argument('dst', help="Directory name inside archive to "
                              "be created")
    parser_mkdir.set_defaults(func=CALL_MAP['mkdir'])

    parser_run.add_argument('arch', help="archive filename")
    parser_run.add_argument('dst', help="File to be executed")
    parser_run.set_defaults(func=CALL_MAP['run'])

    args = parser.parse_args()
    return args.func(args)


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
