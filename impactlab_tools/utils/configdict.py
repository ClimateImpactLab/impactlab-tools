"""Class for representing tool configuration files
"""

import collections
import inspect


def gather_configtree(d):
    """Chains nested-dicts into a connected tree of ConfigDict(s)

    Parameters
    ----------
    d : dict
        Cast to :py:class:`ConfigDict`. Nested dicts within are also
        recursively cast and assigned parents, reflecting their nested
        structure.

    Returns
    -------
    out : ConfigDict

    Examples
    --------
    .. code-block:: python

        >>> nest = {'a': 1, 'b': {'a': 2}, 'c': 3, 'd-4': 4, 'e_5': 5, 'F': 6}
        >>> tree = gather_configtree(nest)
        >>> tree['b']['d-4']
        4
    """
    out = ConfigDict(d)
    for k, v in out.data.items():
        # Replace nested maps with new ConfigDicts
        if isinstance(v, collections.abc.MutableMapping):
            out.data[k] = gather_configtree(v)
            out.data[k].parent = out
    return out


class ConfigDict(collections.UserDict):
    """Chain-able dictionary to hold projection configurations.

    A ConfigDict is a dictionary-like interface to a chainmap/linked list.
    Nested dicts can be access like a traditional dictionary but it searches
    parent dictionaries for keys:values not found. All string keys normalized,
    by transforming all characters to lowercase, and all underscores to
    hyphens.

    Attributes
    ----------
    parent : ConfigDict or None
        Parent ConfigDict object to query for keys if not in `self.data`.
    key_access_stack : dict
        Dictionary with values giving the :py:func:`inspect.stack()` from the
        most recent time a key was retrieved (via `self.__getitem__()`).
    data : dict
        The 'local' dictionary, not in parents.

    See Also
    --------
    gather_configtree : Chains nested-dicts into a connected tree of
        ConfigDict(s)

    Examples
    --------
    .. code-block:: python

        >>> d = {'a': 1, 'b': {'a': 2}, 'c': 3, 'd-4': 4, 'e_5': 5, 'F': 6}
        >>> cd = ConfigDict(d)
        >>> cd['b']
        {'a': 2}

        'F' key is now lowercase.

        >>> cd['f']
        6

        '_' is now '-'

        >>> cd['e-5']
        5

        Keys that have been accessed.

        >>> cd.key_access_stack.keys()
        dict_keys(['b', 'f', 'e-5'])
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None

        for k, v in self.data.items():
            # Normalize string keys, only when needed
            if isinstance(k, str) and (k.isupper() or '_' in k):
                new_key = self._normalize_key(k)
                self.data[new_key] = self.pop(k)

        self.key_access_stack = dict()

    def __getitem__(self, key):
        key = self._normalize_key(key)
        out = super().__getitem__(key)

        # We don't want to store in key_access_stack if __missing__() was used
        if key in self.data.keys():
            self.key_access_stack[key] = inspect.stack()
        return out

    def __missing__(self, key):
        if self.parent is None:
            raise KeyError
        return self.parent[key]

    def __setitem__(self, key, value):
        # Note we're not changing `value.parents` if `value` is ConfigDict.
        key = self._normalize_key(key)
        super().__setitem__(key, value)

    @staticmethod
    def _normalize_key(key):
        """If `key` is str, make lowercase and replace underscores with hyphens
        """
        if isinstance(key, str):
            return key.lower().replace('_', '-')

    def accessed_all_keys(self):
        """Where all the keys used in the config tree?

        Returns
        -------
        bool
        """
        local_access = set(self.key_access_stack.keys())
        local_keys = set(self.data.keys())
        all_used = local_access == local_keys

        if self.parent is not None:
            all_used = all_used and self.parent.accessed_all_keys()

        return all_used

    def merge(self, x, xparent=False):
        """Merge, returning new copy

        Parameters
        ----------
        x : ConfigDict
        xparent : bool, optional
            Do attach `x.parent` to `out.parent`? If False, attaches
            `self.parent`.

        Return
        ------
        out : ConfigDict
            Merged ConfigDict, using copied values from `self`.
        """
        out = self.copy()
        out.update(x)

        if xparent is True:
            out.parent = x.parent

        return out
