=============
 lazy-import
=============

And experiment in lazy import functionality for Python.


Usage
=====

This is by no means guaranteed to work :-)

Currently it has only beed tested with imports of the form::

    from lazy_import import lazy_import
    with lazy_import():
        import foo.bar.baz
