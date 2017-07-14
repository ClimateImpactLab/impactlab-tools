Optional `files` configuration system
=====================================

The `impactlab_tools` repository contains a general system for passing
configuration information to scripts, and this is used by a few of the
existing repositories.  New repositories are welcome to use it, if
they choose.  The features of the system are:

 - Individual jobs are run with configuration dictionaries, which
   specify the mode or targets of their work.
 - These configuration options are usually specified on the
   command-line, and can be read from `.yml` files, from individual
   configuration arguments on the command line, or both.
 - Optionally, an additional "server configuration" file specifies a
   shared data directory on the job server, allowing files there to be
   accessed more easily.

Job configurations
------------------

The configuration options for individual jobs are usually specified on
the command-line, and accessed through the
`files.get_allargv_config()` function.  The
`files.get_allargv_config()` function builds a single configuration
dictionary from arguments according to the following rules:

 - `FILE.yml`: a full configuration YaML file, merged into the result dictionary
 - `--config=FILE.yml`: a full configuration YaML file, as above
 - `--KEY=VALUE`: a single configuration value to be set
 - anything else: sets an entry in the config file for that anything to have a value of True

Alternatively, `files.get_file_config(filepath)` can be used to just
read in a `.yml` configuration file.

Shared directory handling
-------------------------

Typically, each job-running machine has a common root directory
containing data for multiple jobs and multiple users.  These
directories are as follows for the common GCP servers:

 - Sacagawea: `/shares/gcp`
 - OSDC: `/mnt/gcp`
 - BRC: `/global/scratch/<username>`

Having a server-level configured shared data directory allows the same
job to be run on multiple servers without changes to either the job
code or job-level configuration.

Individual users and individual jobs can specify their own common data
root directories, though this is generally not efficient.  Below, the
"server configuration" refers to all options that are generally
thought of as bein shared across all users and jobs on a server, but
this need not be the case.

The server configuration currently supports only one server-level
configuration option: `shareddir`, which is the root data directory
described above.

Once the server configuration is specified, the function
`files.configpath(path)` can be used to construct absolute paths to
data files.  If `path` is a relative path (not starting with a `/`),
the path returned is given as relative to the server data directory.
Otherwise, it is returned unchanged.  (This second case occurs, for
example, when job confiuration files specify arbitrary output
directories, which may or may not be relative to the shared data
directory.)

The server configuration can be set by setting `files.server_config`
to a dictionary containing the `shareddir` key.  Alternatively, a file
titled `server.yml` can be stored one directory above any job
repository directory; if `files.server_config` is not set, this file
will be looked for.
