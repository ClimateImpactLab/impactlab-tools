
import subprocess as sp


def check_version(input_list, check_git=False):
    """
    Returns version information given a list of module dependencies

    Parameters
    ----------

    input_list: list
        list of strings, all module names

    check_git: bool
        True if the caller also wants to check the git hash of a repo
        (input_list contains its name) that's under the user's home dir.

    Returns
    -------

    dict:
        A dictionary of the modules: keys are the module names, each
        key has value of another dictionary, containing:

            - "source": how is the module installed ("pip", "local",
              "git", or None):

                - source is "pip" if it's an open-sourced python
                  package installed through pip.
                - source is "pip-local" if it's a self-made tool
                  installed through pip.
                - source is "git" if it's a git managed repo of
                  scripts, not installed through pip.
                - source is None if the module cannot be found.

            - "version": If it's an open source module (source: pip),
              this is the version numbers of it.
            - "git_hash": If it's a local module (source: local, or
              git).

    Example
    -------

    >>> input_list = [
    ...    "scipy", "numpy", "Cheetah", "computer",
    ...    "impact-calculations", "metacsv"]
    ...
    >>> check_version(input_list, check_git=True) # doctest: +SKIP
    {
        "scipy": {"source": "pip", "version": "0.19"},
        "numpy": {"source": "pip", "version": "1.12.1"},
        "Cheetah": {"source": "pip", "version": "2.4.4"},
        "computer": {
            "source": "git",
            "git_hash": "662870e0fa914b4fa958e78ebe02b858c31fe41d"},
        "impact-calculations": {
            "source": "git",
            "git_hash": "e7c1b53b1d9e6571c0555a560c919f9645693b45"},
        "metacsv": {"source": "pip", "version": "0.0.9"}
    }

    """
    # Read in all packages in pips
    pips = sp.check_output("pip freeze", shell=True).split("\n")[:-1]
    modules = {}
    for mod in pips:
        if ".git@" in mod:
            # Assume the format of a local repo in pip freeze looks
            # like this:
            #
            #     "-e git+https://github.com/<UserName>/
            #         <RepoName>.git@<Git_Hash>#egg=computer-master"
            #
            # We are interested in the <Git_Hash> part, saving in
            # the modules dictionary with <RepoName> as the key.
            ind = mod.index(".git@")
            end = mod.index("#")
            modules[mod[:ind].split("/")[-1]] = mod[ind+5:end]
        else:
            ind = mod.index("=")
            modules[mod[:ind]] = mod[ind:].rstrip("\n").lstrip("=")

    git = {}
    if check_git:
        # Read in all repos under my home directory
        repos = sp.check_output(
            "find ~/ -name '.git'", shell=True).split(".git\n")[:-1]

        for repo in repos:
            name = repo.split("/")[-2]
            git[name] = sp.check_output(
                "cd " + repo + " && git log --format='%H' -n 1",
                shell=True).rstrip("\n")

    if 'self' in input_list:
        version = sp.check_output("git log --format='%H' -n 1", shell=True).rstrip("\n")
        if "\n" not in version:
            git['self'] = version
            
    # Iterate through the input_list and find if the target is in
    # either the modules or the git dictionary, or not at all.
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

    return rtDict

if __name__ == '__main__':
    print(check_version(['self', 'impact-calculations', 'metacsv', 'impactlab-tools', 'scipy', 'open-estimate']))
    
