import shutil
from impactlab_tools.utils import paralog

def test_claiming():
    statman1 = paralog.StatusManager('test', 'Testing process', 'testing-paralog', 60*60)
    print statman1.logpath
    assert statman1.claim("testing-paralog"), "Cannot claim directory!"

    statman2 = paralog.StatusManager('test', 'Testing process', 'testing-paralog', 60*60)
    print statman2.logpath
    assert not statman2.claim("testing-paralog"), "Accidentally claimed directory!"

    statman1.update("testing-paralog", "New status.")
    statman1.release("testing-paralog", "First pass complete.")

    assert statman2.claim("testing-paralog"), "Cannot claim directory afterwards!"

    statman2.release("testing-paralog", "Second pass complete.")

    logpath1 = statman1.logpath
    logpath2 = statman2.logpath

    del statman2 # need to delete in opposite order for our test
    del statman1

    print logpath1
    print logpath2

    with open(paralog.StatusManager.globalstatus_filepath("testing-paralog"), 'r') as fp:
        print fp.read()

    shutil.rmtree('testing-paralog')
