

import shutil
from impactlab_tools.utils import paralog
import os

def test_claiming():
    statman1 = paralog.StatusManager(
        'test',
        'Testing process',
        'testing-paralog',
        60 * 60,
    )
    print(statman1.logpath)
    if not statman1.claim("testing-paralog"):
        raise OSError("Cannot claim directory!")

    statman2 = paralog.StatusManager(
        'test',
        'Testing process',
        'testing-paralog',
        60 * 60,
    )
    print(statman2.logpath)
    if statman2.claim("testing-paralog"):
        raise OSError("Accidentally claimed directory!")

    statman1.update("testing-paralog", "New status.")
    statman1.release("testing-paralog", "First pass complete.")

    if not statman2.claim("testing-paralog"):
        raise OSError("Cannot claim directory afterwards!")

    statman2.release("testing-paralog", "Second pass complete.")

    logpath1 = statman1.logpath
    logpath2 = statman2.logpath

    del statman2 # need to delete in opposite order for our test
    del statman1

    print(logpath1)
    print(logpath2)

    with open(paralog.StatusManager.globalstatus_filepath("testing-paralog")) as fp:
        print(fp.read())

    shutil.rmtree('testing-paralog')

def test_log_message():

    '''
    test that both normal print messages go to the log and log_message
    calls go to the log.

    This test creates files that have to be deleted for the test to run
    sucessfully again. The test deletes these files at the end, but if
    it fails before, the user should manually delete these files after
    fixing the test.
    '''

    statman = paralog.StatusManager(
        jobname='test',
        jobtitle='Testing process',
        logdir='testing-paralog',
        timeout=60 * 60,
    )
    print("Printed message")
    statman.log_message(msg='Log-only message')
    assert statman.logpath == "testing-paralog/test-0.log"

    del statman

    assert os.path.exists("testing-paralog/test-0.log")
    with open("testing-paralog/test-0.log") as fp:
        assert fp.readline() == "Printed message\n"
        assert fp.readline() == "Log-only message\n"


    shutil.rmtree('testing-paralog')

