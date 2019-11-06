try:
    # For py3.
    from importlib import reload
except ImportError:
    # In py27 so just use `reload()`.
    pass
import pytest
from os import path as ospath
from impactlab_tools.utils import files as ufiles


@pytest.mark.parametrize('use_shellvar,expectedval',
                         [(True, 'shellvar'), (False, 'moduledefault')])
def test_sharedpath(use_shellvar, expectedval, tmpdir, monkeypatch):
    """Test sharedpath() gives right path when shell variable set, and when not
    """
    # Need to reload `ufiles` because running files.sharedpath() has
    # key sideeffect on module attributes. Need `ufiles` to be fresh for tests.
    reload(ufiles)

    p = tmpdir.join('foobar.yml')
    # Monkeypatch tmpdir and files default server path for test to avoid
    # messing with local user dir.
    if use_shellvar:
        # Read from shell variable, this is the actual path in sharedir,
        # which is normally in server.yml but now in shell variable.
        p.write('shareddir: shellvar\n')
        monkeypatch.setenv(str(ufiles.SHAREDDIR_SHELLVAR), 'shellvar')
    else:
        # Legacy behavior
        p.write('shareddir: moduledefault\n')
        monkeypatch.setattr(ufiles, 'default_server_config_path', str(p))

    expected = ospath.join(str(expectedval), '')
    victim = ufiles.sharedpath('')
    assert victim == expected
