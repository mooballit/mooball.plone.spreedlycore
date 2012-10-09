==============================
Spreedly Configuration Wrapper
==============================

Plone Configlet to configure Spreedly Core.

License
-------

All material is Copyright Mooball IT

All code is licensed under the ZPL Licence (see LICENSE.txt)

Requirements
------------

* spreedly-core-python (http://github.com/mooballit/spreedly-core-python)

Installation
------------

To get started, download spreedly-core-python and place in directory below.
Create and add the following to mooball.plone.spreedlycore/buildout.cfg:

[buildout]
develop += ../spreedly-core-python/
eggs += spreedly-core-python
