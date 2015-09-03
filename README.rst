========================
Midnight Commander extfs
========================

Those are Midnight Commander extfs plugins for handling several archive types
mostly known from AmigaOS - like **lha**, **lzx** and disk images like **adf**
and **dms**.

Installation
============

See individual installation plugins below. Basically it comes down to:

* copying ``extfslib.py`` and plugin files to ``~/.local/share/mc/extfs.d/``
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

* copy ``extfslib.py`` and ``ulha`` to ``~/.local/share/mc/extfs.d/``
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

* copy ``extfslib.py`` and ``ulzx`` to ``~/.local/share/mc/extfs.d/``
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

In case of corrupted or no-dos images, message will be shown.

Requirements
------------

It requires ``unadf`` utility from `ADFlib <https://github.com/lclevy/ADFlib>`_
repository, with included `that commit
<https://github.com/lclevy/ADFlib/commit/d36dc2f395f3e8fcee81f66bc86994e166b6140f>`_
in particular, which introduced separation between filename and comment
attribute on Amiga Fast File System.

If it turns out that your distribution doesn't provide proper version of ADFlib,
there will be a need for building it by hand.

It may be done by using following steps:

#. Grab the `sources
   <http://http.debian.net/debian/pool/main/u/unadf/unadf_0.7.11a.orig.tar.gz>`_
   and `patches
   <http://http.debian.net/debian/pool/main/u/unadf/unadf_0.7.11a-3.debian.tar.gz>`_
   from `Debian repository <http://packages.debian.org/sid/unadf>`_.
#. Extract ``unadf_0.7.11a-3.debian.tar.gz`` and ``unadf_0.7.11a.orig.tar.gz``
   into some temporary directory::

   $ mkdir temp
   $ cd temp
   $ tar zxf ~/Downloads/unadf_0.7.11a-3.debian.tar.gz
   $ tar zxf ~/Downloads/unadf_0.7.11a.orig.tar.gz
   $ cd unadf-0.7.11a

#. Apply Debian patches::

    $ for i in `cat ../debian/patches/series`; do
    > patch -Np1 < "../debian/patches/${i}"
    > done

#. Apply the patch from extras directory::

   $ patch -Np1 < [path_to_this_repo]/extras/unadf_separate_comment.patch
   $ make
   $ cp Demo/unadf [destination_path]

#. Place ``unadf`` binary under directory reachable by ``$PATH``.

For optional dms support, `xdms <http://zakalwe.fi/~shd/foss/xdms/>`_ utility is
needed.

Installation
------------

* copy ``extfslib.py`` and ``uadf`` to ``~/.local/share/mc/extfs.d/``
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

License
=======

This software is licensed under 3-clause BSD license. See LICENSE file for
details.
