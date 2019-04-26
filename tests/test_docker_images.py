# -*- coding: utf-8 -*-


def test_check_all_versions_built(date, versions, docker):
    tags = set()
    for image in docker.images.list():
        tags.update(image.tags)
    expected_tags = {'saltstack/salt:latest'}
    for version in versions:
        expected_tags.update([version, f'{version}-{date}'])

    assert expected_tags.issubset(tags)
