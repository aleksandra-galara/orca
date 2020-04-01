# Contributing to Open RCA

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to Open RCA and its packages, which are hosted in the [Open RCA Organization](https://github.com/openrca) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[How can I contribute?](#how-can-i-contribute)

[Workflow](#workflow)
  * [Development environment](#development-environment)
  * [Feature integration](#feature-integration)
  * [Pull requests](#pull-requests)
  * [Issues](#pull-requests)

[Styleguides](#styleguides)
  * [Git commit messages](#git-commit-messages)


## How can I contribute?

Open RCA is currently subjected to intense development. There are lots of features in the project
roadmap awaiting design, implementation or improvement. **If you feel ready to contribute, for sure,
you will find exciting features to carve!**

First, you can view the reported bugs and feature requests in
[Github issues](https://github.com/openrca/orca/issues). As a new contributor, give priority to
items labeled "*good first issue*". These tasks have a reasonable level of complexity intended for
newcomers, and at the same time, enable you to familiarize yourself with a significant part of the
codebase. They also allow going through the Github workflow and CI process for the first time.

If nothing caught your eye or you need a more individual approach, don't hesitate to contact us in
our Gitter chat. We will introduce you to the project and openly talk about other options in the
roadmap.

## Workflow

### Development environment

The following sections include instructions to prepare an environment to develop Open RCA
components.

#### Setting up Python

Many Open RCA components are written in the Python programming language. To build, you'll need a
Python development environment. If you haven't set up a Python development environment, please
follow [these](https://docs.python.org/3/using/index.html) instructions to install the Python tools.

Open RCA currently builds with Python 3.7.

#### Setting up Docker

TODO: Describe instructions to setup Docker

#### Setting up Kubernetes

TODO: Describe instructions to setup Kubernetes

#### Setting up Telepresence

TODO: Describe instructions to setup Telepresence

#### Installing Open RCA

TODO: Describe instructions to setup Open RCA for development

### Feature integration

TODO: Describe instructions for new feature integration

### Pull requests

If you're working on an existing issue, simply respond to the issue and express interest in working
on it. This helps other people know that the issue is active, and hopefully prevents duplicated
efforts.

To submit a proposed change:

- Fork the affected repository.
- Create a new branch for your changes.
- Develop the code/fix.
- Add new test cases. In the case of a bug fix, the tests should fail without your code changes.
  For new features try to cover as many variants as reasonably possible.
- Modify the documentation as necessary.
- Verify the entire CI process (building and testing) works.

While there may be exceptions, the general rule is that all PRs should be 100% complete - meaning
they should include all test cases and documentation changes related to the change.

### Issues

[GitHub issues](https://github.com/openrca/orca/issues/new) can be used to report bugs or
submit feature requests.

When reporting a bug please include the following key pieces of information:

- The version of the project you were using (e.g. version number, or git commit)
- The exact, minimal, steps needed to reproduce the issue. Submitting a 5 line script will get
  a much faster response from the team than one that's hundreds of lines long.

## Styleguides

### Git commit messages

* Use the present tense ("Add probe for..." not "Added probe for...").
* Use the imperative mood ("Add probe for..." not "Adds probe for...").
* Limit the first line to 72 characters or less.
* Reference issues and pull requests liberally after the first line.
