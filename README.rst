=================================
ulha extfs for Midnight Commander
=================================

This is Midnight Commander extfs plugin for handling lha/lzh archives.
It requires `lha <http://lha.sourceforge.jp>`_ free LHA implementation to work.

Installation
------------
* copy ``ulha.py`` to ``~/.local/share/mc/extfs/ulha``
* add or change entry for lha/lzh files handle in ``~/.config/mc/mc.ext``::

    # lha
    regex/\.[lL]([Hh][aA]|[Zz][hH])$
         Open=%cd %p/ulha://
         View=%view{ascii} lha l %f
