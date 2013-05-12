========================
Midnight Commander extfs
========================

Those are Midnight Commander extfs plugins for handling several archive types.

Installation
============

See individual installation plugins below. Basically it comes down to:

* copying ``extfslib.py`` and plugin files to ``~/.local/share/mc/extfs/``
* installing binary handlers (lha, unlzx, xdms and unadf)
* adding an entry in ``~/.config/mc/mc.ext``::

    # arch
    regex/\.pattern$
         Open=%cd %p/handler_filename://

ULha
====

ULha is an extfs plugin which can be used with lha/lzh/lharc archives.
Personally, I've use it almost exclusively for archives created long time ago
on my Amiga. Both reading from and writing into archive was implemented.

Requirements
------------

ULha requires `free lha <http://lha.sourceforge.jp>`_ implementation to work.

Installation
------------

* copy ``extfslib.py`` and ``ulha`` to ``~/.local/share/mc/extfs/``
* add or change entry for files handle in ``~/.config/mc/mc.ext``::

    # lha
    regex/\.[lL]([Hh][aA]|[Zz][hH])$
         Open=%cd %p/ulha://
         View=%view{ascii} lha l %f

ULzx
====

ULzx is an extfs plugin which can be used to browse and extract lzx archives,
which are known almost exclusively from Amiga.

Due to limitations of
`unlzx <ftp://us.aminet.net/pub/aminet/misc/unix/unlzx.c.gz.readme>`_ tools,
only reading is supported. Also be aware, that
`unlzx <ftp://us.aminet.net/pub/aminet/misc/unix/unlzx.c.gz.readme>`_ cannot
extract files individually, so copying entire archive content is not
recommended, since on every single file a full archive extract would be
performed, which in the end would have impact on performance.

Requirements
------------

ULzx requires
`unlzx <ftp://us.aminet.net/pub/aminet/misc/unix/unlzx.c.gz.readme>`_ tool.

Installation
------------

* copy ``extfslib.py`` and ``ulzx`` to ``~/.local/share/mc/extfs/``
* add or change entry for files handle in ``~/.config/mc/mc.ext``::

    # lzx
    regex/\.[lL][zZ][xX]$
         Open=%cd %p/ulzx://
         View=%view{ascii} unlzx -v %f

UAdf
====

UAdf is an extfs plugin suitable for reading .adf, .adz and .dms Amiga floppy
disk images. Due to limitations of the
`unadf <http://freecode.com/projects/unadf>`_, file access inside disk image is
read only.

Note, that in case of no-dos images, directory listing will be empty.

Requirements
------------

It requires the `unadf <http://freecode.com/projects/unadf>`_ utility.
Unfortunately, the page containing original sources doesn't exists
anymore. Luckily, there is a copy of the source (and useful patches) in `Debian
repository <http://packages.debian.org/sid/unadf>`_.

There should be one change made to the source of unadf, though. While using
"-lr" switch, unadf by default also displays comments next to file name,
separated by the comma. If comment or filename contains comma sign, there is no
way to distinguish where filename ends and comment starts. In ``extras``
directory there is a patch for fixing this - no comments would be displayed by
default.

First, grab the sources and Debian patches. Apply them. To do this manually,
extract ``unadf_0.7.11a-3.debian.tar.gz`` and ``unadf_0.7.11a.orig.tar.gz`` into
some temporary directory. Apply patches in order like in debian/patches/series
file. Then apply patch from extras directory::

    $ mkdir temp
    $ cd temp
    $ tar zxf ~/Downloads/unadf_0.7.11a-3.debian.tar.gz
    $ tar zxf ~/Downloads/unadf_0.7.11a.orig.tar.gz
    $ cd unadf-0.7.11a
    $ for i in `cat ../debian/patches/series`; do
    > patch -Np1 < "../debian/patches/${i}"
    > done
    $ patch -Np1 < [path_to_this_repo]/extras/unadf_separate_comment.patch
    $ make
    $ cp Demo/unadf [destination_path]

``unadf`` binary should be placed in ``$PATH``.

For optional dms support, `xdms <http://zakalwe.fi/~shd/foss/xdms/>`_ utility is
needed.

Installation
------------

* copy ``extfslib.py`` and ``uadf`` to ``~/.local/share/mc/extfs/``
* add or change entry for files handle in ``~/.config/mc/mc.ext``::

    # adf
    type/^Amiga\ .* disk
        Open=%cd %p/uadf://
        View=%view{ascii} unadf -lr %f

    # adz
    regex/\.([aA][dD][zZ])$
        Open=%cd %p/uadf://

    # dms
    regex/\.([dD][mM][sS])$
        Open=%cd %p/uadf://
