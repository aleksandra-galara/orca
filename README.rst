OpenRCA
==============================================

.. image:: https://img.shields.io/travis/openrca/orca.svg
   :target: https://travis-ci.org/openrca/orca

.. image:: https://img.shields.io/github/license/openrca/orca
   :target: https://github.com/openrca/orca

.. image:: https://img.shields.io/gitter/room/openrca/community
   :target: https://gitter.im/openrca/community

.. raw:: html

    <h2 align="center">
        <img src="docs/images/orca-logo.png" alt="OpenRCA" height="200px">
    <br>
    Automated Root Cause Analysis for Kubernetes
    </h2>

Objectives
----------

- Holistic insight into application infrastructure (infra graph)
- Integration hub for telemetry projects (Prometheus, Elasticsearch, Falco)
- Time-based infrastructure analysis
- Automated diagnostic workflows for Kubernetes infra and workloads
- ML-supported root cause inference
- Policy-driven RCA instrumentation
- Novel approach for site reliability testing and chaos engineering

Installation
------------

Install using Helm chart:

::

    $ cd ./helm
    $ helm install ./orca --namespace rca --name orca

Usage
-----

TODO: Write usage instructions

Development
-----

Using Docker Compose:

::

    $ docker-compose build
    $ docker-compose up
    $ docker-compose down

Using Telepresence:

::

    $ telepresence \
        --namespace rca \
        --mount=/tmp/telepresence \
        --swap-deployment orca \
        --docker-run \
            --rm \
            -it \
            -v=/tmp/telepresence/var/run/secrets:/var/run/secrets \
            -v=/tmp/telepresence/etc/orca:/etc/orca \
            -v $(pwd):/app
