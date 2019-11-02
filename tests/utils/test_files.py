import pytest
from os import path as ospath
from impactlab_tools.utils import files as ufiles
import importlib


@pytest.mark.parametrize('use_shellvar,expectedval',
                         [(True, 'shellvar'), (False, 'moduledefault')])
def test_sharedpath(use_shellvar, expectedval, tmpdir, monkeypatch):
    """Test sharedpath() gives right path when shell variable set, and when not
    """
    # Need to reload `ufiles` because running files.sharedpath() has
    # key sideeffect on module attributes. Need `ufiles` to be fresh for tests.
    importlib.reload(ufiles)

    p = tmpdir.join('foobar.yml')
    # Monkeypatch tmpdir and files default server path for test to avoid
    # messing with local user dir.
    if use_shellvar:
        # Read from shell variable
        p.write('shareddir: shellvar\n')
        monkeypatch.setenv(str(ufiles.SERVER_SHELLVAR), str(p))
    else:
        # Normal behavior
        p.write('shareddir: moduledefault\n')
        monkeypatch.setattr(ufiles, 'default_server_config_path', str(p))

    expected = ospath.join(str(expectedval), '')
    victim = ufiles.sharedpath('')
    assert victim == expected
