import subprocess as sp

def check_version(input_list, check_git=False):
    """
    Input:
        input_list: list of strings, all module names
        check_git: True if the caller also wants to check the git hash of a repo (input_list contains its name) that's under the user's home dir.
    Output:
        A dictionary of the modules: keys are the module names, each key has value of another dictionary, containing:
        "source": how is the module installed ("pip", "local", "git", or None):
            - source is "pip" if it's an open-sourced python package installed through pip.
            - source is "pip-local" if it's a self-made tool installed through pip.
            - source is "git" if it's a git managed repo of scripts, not installed through pip.
            - source is None if the module cannot be found.
        "version": If it's an open source module (source: pip), this is the version numbers of it.
        "git_hash": If it's a local module (source: local, or git).
    """
    # Read in all packages in pips
    pips = sp.check_output("pip freeze", shell=True).split("\n")[:-1]
    modules = {}
    for mod in pips:
        if ".git@" in mod:
            # Assume the format of a local repo in pip freeze looks like this:
            # "-e git+https://github.com/<UserName>/<RepoName>.git@<Git_Hash>#egg=computer-master"
            # We are interested in the <Git_Hash> part, saving in the modules dictionary with <RepoName> as the key.
            ind = mod.index(".git@")
            end = mod.index("#")
            modules[mod[:ind].split("/")[-1]] = mod[ind+5:end]
        else:
            ind = mod.index("=")
            modules[mod[:ind]] = mod[ind:].rstrip("\n").lstrip("=")

    # Read in all repos under my home directory
    repos = sp.check_output("find ~/ -name '.git'", shell=True).split(".git\n")[:-1]
    git = {}
    for repo in repos:
        name = repo.split("/")[-2]
        git[name] = sp.check_output("cd " + repo + " && git log --format='%H' -n 1", shell=True).rstrip("\n")

    # Iterate through the input_list and find if the target is in either the modules or the git dictionary, or not at all.
    rtDict = {}
    for tgt in input_list:
        info = {}
        if tgt in modules:
            if "." in modules[tgt]:
                info["source"] = "pip"
                info["version"] = modules[tgt]
            else:
                info["source"] = "pip-local"
                info["git_hash"] = modules[tgt]
        elif tgt in git:
                info["source"] = "git"
                info["git_hash"] = git[tgt]
        else:
            info["source"] = None
        rtDict[tgt] = info
    # print(rtDict)
    return rtDict

# Example:
# input_list = ["scipy", "numpy", "Cheetah", "computer", "impact-calculations", "metacsv"]
# check_version(input_list, check_git=True)
