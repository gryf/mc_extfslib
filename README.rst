===========================
Midnight Commander extfslib
===========================

.. image:: https://img.shields.io/pypi/v/extfslib.svg
    :target: https://pypi.python.org/pypi/extfslib

Midnight Commander extfslib helper library for writing extfs archive plugins.


Description
===========

Extfslib help with building Midnight Commander extfs plugins, especially for
those which operates on different kind of archives.

Simplest plugin built on top of this lib would be:

.. code:: python

   import extfslib


   class MyArchive(extfslib.Archive):

       ARCHIVER = "fancyarch"

       def list(self):
           if not self._contents:
               return 1

           for item in self._contents:
               sys.stdout.buffer.write(self.ITEM % item)


   arch = MyArchive('/path/to/file.fancyarch')
   arch.list()


In this example class instance should be able to be called with ``list``
method.  All methods:

- ``list``
- ``copyin``
- ``copyout``
- ``rm``
- ``mkdir``
- ``rmdir``
- ``run``

should be implemented if needed, since by default all of them are just defined,
but not implemented.

Of course, real life example can be a little bit more complicated, since there
would be possible need for adapting ``LINE_PAT`` which is regular expression
for getting attributes for the list compatible with MC along with the ``ITEM``
which holds the output pattern and utilizes dictionary from ``LINE_PAT``,
``CMD`` which maps between class and archiver commands. Possibly there might be
needed some other adjustments.

Additionally there is an optional ``Config`` class, which might be used for
reading Midnight Commander ini file (ususally located in ``~/.config/mc/ini``),
so that for the example above:

.. code:: python

   import extfslib


   class MyArchive(extfslib.Archive):

       ARCHIVER = "fancyarch"

       def __init__(self):
           super().__init__()
           self.conf = extfslib.Config(self)
           if self.conf,getint('config_key'):
               # do something

where the ``ini`` config file would contain:

.. code:: ini

   …
   [myarchive]
   config_key = 300
   …

So, section name ``[myarchive]`` must match class name in lower case, and name
of the option is arbitrary string folowed by value. Note, the section and
options must be added manually.


Installation
============

Install from Pypi

.. code:: shell-session

   # pip install extfslib

or, as a user:

.. code:: shell-session

   $ pip install extfslib --user

or use virtualenv:

.. code:: shell-session

   $ git clone https://github.com/gryf/mc_extfslib
   $ cd mc_extfslib
   $ virtualenv venv
   $ source venv/bin/activate
   (venv) $ pip install


License
=======

This software is licensed under 3-clause BSD license. See LICENSE file for
details.
