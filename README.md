# test_borg

Testing out the Borg python design pattern; with autoregistration of submodules

Typically modules get registered in a conventional format; e.g. a base class `BaseClass` from 'foo/bar/base.py' gets extended by `SubClass`
in 'foo/bar/sub.py' and `OtherClass` in 'foo/bar/other.py'; the motivation behind this repo is that subclasses can self-register into the parent's
`__subclasses__` attr if the module itself has been imported at some point.

## Components:

A base class must be defined - an example being the `RegisteredType` class defined in the `borg.registered_type.base` module.

The `__init__.py` for the package with the base in then imports `util.borg.load_submodules` and calls it with `__name__`.

Then any classes that subclass RegisteredType will be imported into the runtime by importlib; which means that they will be registered into
`RegisteredType.__subclasses__`.

This pattern would prevent us having to maintain `__init__.py` files and directories of submodules.

## Implementations:

This has been implemented for the `borg.registered_type.base.RegisteredType` and the `borg.sub_borg.borg.registered_type.base.RegisteredType` classes
to prove that it works for submodules as well.
