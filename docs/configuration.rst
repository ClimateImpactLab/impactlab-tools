Optional ``files`` configuration system
=======================================

The :code:`impactlab_tools` repository contains a general system for passing
configuration information to scripts, and this is used by a few of the
existing repositories.  New repositories are welcome to use it, if
they choose.  The features of the system are:

 - Individual jobs are run with configuration dictionaries, which
   specify the mode or targets of their work.
 - These configuration options are usually specified on the
   command-line, and can be read from :code:`.yml` files, from individual
   configuration arguments on the command line, or both.
 - Optionally, an additional "server configuration" file specifies a
   shared data directory on the job server, allowing files there to be
   accessed more easily.

Job configurations
------------------

The configuration options for individual jobs are usually specified on
the command-line, and accessed through the
:code:`files.get_allargv_config()` function.  The
:code:`files.get_allargv_config()` function builds a single configuration
dictionary from arguments according to the following rules:

 - :code:`FILE.yml`: a full configuration YaML file, merged into the result dictionary
 - :code:`--config=FILE.yml`: a full configuration YaML file, as above
 - :code:`--KEY=VALUE`: a single configuration value to be set
 - anything else: sets an entry in the config file for that anything to have a value of True

Alternatively, :code:`files.get_file_config(filepath)` can be used to just
read in a :code:`.yml` configuration file.

Shared directory handling
-------------------------

Typically, each job-running machine has a common root directory
containing data for multiple jobs and multiple users.  These
directories are as follows for the common GCP servers:

 - Sacagawea: :code:`/shares/gcp`
 - OSDC: :code:`/mnt/gcp`
 - BRC: :code:`/global/scratch/<username>`

Having a server-level configured shared data directory allows the same
job to be run on multiple servers without changes to either the job
code or job-level configuration.

Individual users and individual jobs can specify their own common data
root directories, though this is generally not efficient.  Below, the
"server configuration" refers to all options that are generally
thought of as bein shared across all users and jobs on a server, but
this need not be the case.

The server configuration currently supports only one server-level
configuration option: :code:`shareddir`, which is the root data directory
described above.

Once the server configuration is specified, the function
:code:`files.configpath(path)` can be used to construct absolute paths to
data files.  If :code:`path` is a relative path (not starting with a :code:`/`),
the path returned is given as relative to the server data directory.
Otherwise, it is returned unchanged.  (This second case occurs, for
example, when job confiuration files specify arbitrary output
directories, which may or may not be relative to the shared data
directory.)

The server configuration can be set by setting :code:`files.server_config`
to a dictionary containing the :code:`shareddir` key.  Alternatively, a file
titled :code:`server.yml` can be stored one directory above any job
repository directory; if :code:`files.server_config` is not set, this file
will be looked for.
