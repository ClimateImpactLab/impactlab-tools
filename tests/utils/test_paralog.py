
from __future__ import absolute_import

import shutil
from impactlab_tools.utils import paralog

def test_claiming():
    statman1 = paralog.StatusManager('test', 'Testing process', 'testing-paralog', 60*60)
    print(statman1.logpath)
    if not statman1.claim("testing-paralog"):
        raise IOError("Cannot claim directory!")

    statman2 = paralog.StatusManager('test', 'Testing process', 'testing-paralog', 60*60)
    print(statman2.logpath)
    if statman2.claim("testing-paralog"):
        raise IOError("Accidentally claimed directory!")

    statman1.update("testing-paralog", "New status.")
    statman1.release("testing-paralog", "First pass complete.")

    if not statman2.claim("testing-paralog"):
        raise IOError("Cannot claim directory afterwards!")

    statman2.release("testing-paralog", "Second pass complete.")

    logpath1 = statman1.logpath
    logpath2 = statman2.logpath

    del statman2 # need to delete in opposite order for our test
    del statman1

    print(logpath1)
    print(logpath2)

    with open(paralog.StatusManager.globalstatus_filepath("testing-paralog"), 'r') as fp:
        print(fp.read())

    shutil.rmtree('testing-paralog')
