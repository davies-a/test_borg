from typing import Iterator, Tuple
import os
import importlib
import re

_SLASHES_RE = re.compile(r'/')
_DOTS_RE = re.compile(r'\.')
_PACKAGE_BASE_DIRECTORY = os.getcwd()

def create_relative_modulename(dirpath: str, filename: str) -> str:
    """
    Create a module name from a directory path and filename;
    for example ('foo/bar', 'baz.py') -> 'foo.bar.baz'

    Args:
        dirpath (str): Directory name that the file is in.
        filename (str): File to import.

    Returns:
        str: A module name that may imported by importlib.
    """
    module_name = _SLASHES_RE.sub('.', dirpath)
    filename = filename.rstrip('.py')
    module_name += '.' + filename

    return module_name

def walk_module_files(module: str) -> Iterator[Tuple[str, str]]:
    """
    Get the relative directory name and filepath for all files in a module directory.

    Args:
        module (str): The module name, e.g. 'foo.bar'

    Yields:
        Tuple[str, str]: A tuple of the directory path and filename.
    """    
    directory = _DOTS_RE.sub('/', module)
    for dirpath, _, filenames  in os.walk(directory):
        dirpath = os.path.relpath(dirpath, _PACKAGE_BASE_DIRECTORY)
        for filename in filenames:
            yield (dirpath, filename)

def load_submodules(current_module: str):
    """
    Import all files contained within current_module into the current namespace.

    Once imported this will enable use of Borg-style patterns, where subclasses of
    a parent register themselves.

    Args:
        current_module (str): The current module's __name__ - e.g. 'foo.bar' if we
        were autoloading all subclasses of 'foo.bar.base.BaseModel'.
    """
    for dirpath, filename in walk_module_files(module=current_module):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = create_relative_modulename(dirpath=dirpath, filename=filename)
            importlib.import_module(module_name, package=current_module)
