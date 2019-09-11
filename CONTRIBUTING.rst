.. _Contributing:

.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ClimateImpactLab/impactlab-tools/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

impactlab-tools could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such.

To test the documentation you write, run the command::

  $ sphinx-build -W -b html -d docs/_build/doctrees docs/. docs/_build/html

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ClimateImpactLab/impactlab-tools/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Great! There are a couple steps to follow when contributing
code.

Setting up your development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install your local copy into a virtualenv. Assuming you have virtualenvwrapper
installed, this is how you set up your fork for local development::

    $ mkvirtualenv impactlab-tools
    $ cd impactlab-tools/
    $ python setup.py develop

Developing your feature
~~~~~~~~~~~~~~~~~~~~~~~

When making any changes to the impactlab-tools codebase, follow the following steps:

1.  Check for issues on our
    `issues <https://github.com/ClimateImpactLab/impactlab-tools/issues>`_ page. If no
    issue exists for the feature you would like to add, add one! Make sure
    the scope of the issue is limited and precise, so anyone can understand the
    behaviour/feature you would like to see.


2. Fork the `impactlab-tools <https://github.com/ClimateImpactLab/impactlab-tools>`_ repo on GitHub.

3. Clone your fork locally::

    $ git clone git@github.com:your_name_here/impactlab-tools.git

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5.  Write tests for your feature first. Think through all the use cases and
    make sure your tests cover all the ways your code might be used. Include
    the issue number you are addressing in the docstring of your tests:

    .. code-block:: python

        def test_my_new_feature():
            ''' Test my_new_feature. Addresses :issue:`1234` '''

            # test code

6.  Implement your feature, writing as little code as is required to satisfy the
    tests you just wrote. Run tests frequently to make sure you are maintaining
    compatibility with the rest of the package::

        $ python setup.py test
        $ flake8 impactlab-tools tests docs

    You can run only the tests you wrote using pytest's expression matching
    syntax, e.g.::

        $ pytest -k test_my_new_feature

7.  When you are passing all of your tests, run the full test suite.

8.  Make changes to the docs describing your new feature if necessary.

9.  Add an entry to the latest whatsnew document describing your changes. Make
    sure to reference the issue number in your entry.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Happy hunting!
