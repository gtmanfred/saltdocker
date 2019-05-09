# -*- coding: utf-8 -*-
import datetime
import distutils.version
import json
import urllib.request

import docker as dockermod
import pytest

from saltdocker import SaltVersion


@pytest.fixture
def date():
    return SaltVersion.date()


@pytest.fixture
def versions():
    data = json.load(urllib.request.urlopen('https://pypi.org/pypi/salt/json'))
    SaltVersion.data = data
    def make_name(version):
        return f'saltstack/salt:{version}'
    return map(make_name, sorted(filter(SaltVersion._check_version, map(distutils.version.LooseVersion, data['releases']))))


@pytest.fixture
def docker():
    return dockermod.DockerClient()
