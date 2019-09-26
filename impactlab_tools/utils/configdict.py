"""Class for representing tool configuration files
"""
import inspect
# For python2 support:
try:
    from collections import UserDict
    import collections.abc as collections_abc
except ImportError:
    from UserDict import UserDict
    import collections as collections_abc


def gather_configtree(d, parse_lists=False):
    """Chains nested-dicts into a connected tree of ConfigDict(s)

    Parameters
    ----------
    d : dict or MutableMapping
        Cast to :py:class:`ConfigDict`. Nested dicts within are also
        recursively cast and assigned parents, reflecting their nested
        structure.
    parse_lists : bool, optional
        If `d` or its children contain a list of dicts, do you want to convert
        these listed dicts to ConfDicts and assign them parents. This is
        slow. Note this only parses lists, strictly, not all Sequences.

    Returns
    -------
    out : ConfigDict

    Examples
    --------
    .. code-block:: python

        >>> nest = {'a': 1, 'b': {'a': 2}, 'c': 3, 'd-4': 4, 'e_5': 5, 'F': 6}
        >>> tree = gather_configtree(nest)
        >>> tree['b']['a']
        2

    Returns the value for "a" in the *nested* dictionary "b". However, if we
    request a key that is not available in this nested "b" dictionary, it
    will search through all parents.

        >>> tree['b']['d-4']
        4

    A `KeyError` is only thrown if the search has been exhausted with no
    matching keys found.
    """
    out = ConfigDict(d)
    for k, v in out.data.items():
        # Replace nested maps with new ConfigDicts
        if isinstance(v, collections_abc.MutableMapping):
            out.data[k] = gather_configtree(v, parse_lists=parse_lists)
            out.data[k].parent = out

        # If list has mappings, replace mappings with new ConfigDicts
        if parse_lists and isinstance(v, list):
            for idx, item in enumerate(v):
                if isinstance(item, collections_abc.MutableMapping):
                    cd = gather_configtree(item, parse_lists=parse_lists)
                    cd.parent = out
                    out.data[k][idx] = cd

    return out


class ConfigDict(UserDict, object):
    """Chain-able dictionary to hold projection configurations.

    A ConfigDict is a dictionary-like interface to a chainmap/linked list.
    Nested dicts can be access like a traditional dictionary but it searches
    parent dictionaries for keys:values not found. All string keys normalized,
    by transforming all characters to lowercase, and all underscores to
    hyphens.

    Attributes
    ----------
    parent : ConfigDict or None
        Parent ConfigDict object to query for keys if not in ``self.data``.
    key_access_stack : dict
        Dictionary with values giving the :py:func:`inspect.stack()` from the
        most recent time a key was retrieved (via ``self.__getitem__()``).
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

        >>> cd.key_access_stack.keys() # doctest: +SKIP
        dict_keys(['b', 'f', 'e-5'])
    """
    def __init__(self, *args, **kwargs):
        super(ConfigDict, self).__init__(*args, **kwargs)
        self.parent = None

        for k, v in self.data.items():
            # Normalize string keys, only when needed
            if isinstance(k, str) and (k.isupper() or '_' in k):
                new_key = self._normalize_key(k)
                self.data[new_key] = self.pop(k)

        self.key_access_stack = dict()

    def __getitem__(self, key):
        key = self._normalize_key(key)
        out = super(ConfigDict, self).__getitem__(key)

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
        super(ConfigDict, self).__setitem__(key, value)

    @staticmethod
    def _normalize_key(key):
        """If `key` is str, make lowercase and replace underscores with hyphens
        """
        if isinstance(key, str):
            return key.lower().replace('_', '-')

    def accessed_all_keys(self, search='local', parse_lists=False):
        """Were all the keys used in the config tree?

        Parameters
        ----------
        search : {'local', 'parents', 'children'}
            What should the search cover? Options are:

            ``"local"``
                Only check whether keys were used locally (in `self`).

            ``"parents"``
                Recursively check keys in parents, moving up the tree, after
                checking local keys.

            ``"children"``
                Recursively check keys in children, moving down the tree, after
                checking local keys.
        parse_lists : bool, optional
            If True when `search` is "children", check if self or its children
            contain a list and check the list for ConfDicts and whether they
            used their keys. This is slow. Note this only parses lists,
            strictly, not all Sequences.

        Returns
        -------
        bool

        Examples
        --------
        .. code-block:: python

            >>> d = {'a': 1, 'b': {'a': 2}, 'c': 3, 'd-4': 4, 'e_5': 5, 'F': 6}
            >>> root_config = gather_configtree(d)
            >>> child_config = root_config['b']
            >>> child_config['a']
            2

            We can check whether all the keys in `child_config` have been
            accessed.

            >>> child_config.accessed_all_keys()
            True

            Same but also checking that all keys up the tree in parents have
            been used.

            >>> child_config.accessed_all_keys('parents')
            False

            Several keys in root_config were not accessed, so False is
            returned.

            Can also check key use locally and down the tree in nested, child
            ConfigDict instances.

            >>> root_config.accessed_all_keys('children')
            False

            ...which is still False in this case -- all keys in nested
            child_config have been used, but not all of the local keys in
            root_config have been used.

        """
        search = str(search)
        search_options = ('local', 'parents', 'children')
        if search not in search_options:
            raise ValueError('`search` must be in {}'.format(search_options))

        local_access = set(self.key_access_stack.keys())
        local_keys = set(self.data.keys())
        all_used = local_access == local_keys

        # Using a "fail fast" strategy...

        if all_used is False:
            return False

        if search == 'parents':
            # Recursively check parents keys, if any haven't been used,
            # immediately return False.
            if self.parent is not None:
                parent_used = self.parent.accessed_all_keys(
                    search=search,
                    parse_lists=parse_lists,
                )
                if parent_used is False:
                    return False

        elif search == 'children':
            # Recursively check children keys, if any haven't been used,
            # immediately return False.
            for k, v in self.data.items():
                if parse_lists and isinstance(v, list):
                    for item in v:
                        try:
                            child_used = item.accessed_all_keys(
                                search=search,
                                parse_lists=parse_lists,
                            )
                            if child_used is False:
                                return False
                        except AttributeError:
                            continue
                    continue

                try:
                    child_used = v.accessed_all_keys(search=search,
                                                     parse_lists=parse_lists)
                    if child_used is False:
                        return False
                except AttributeError:
                    continue

        return True

    def merge(self, x, xparent=False):
        """Merge, returning new copy

        Parameters
        ----------
        x : ConfigDict or dict
        xparent : bool, optional
            Attach ``x.parent`` to ``out.parent``? If False, attaches
            ``self.parent``. Only works if `x` is :py:class:`ConfigDict`.

        Return
        ------
        out : ConfigDict
            Merged ConfigDict, using copied values from ``self``.
        """
        out = self.copy()
        out.update(x)

        if xparent is True:
            out.parent = x.parent

        return out
