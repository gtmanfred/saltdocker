# -*- coding: utf-8 -*-
import asyncio
import distutils.version
import signal

import aiohttp
import aiodocker

MINVER = distutils.version.LooseVersion('2017.7.0')


class SaltVersion(object):

    loop = asyncio.get_event_loop()
    versions = []

    def __init__(self, version):
        self.version = version

    async def __call__(self):
        print(self.version)
        await asyncio.sleep(1)

    @classmethod
    async def get_versions(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://pypi.org/pypi/salt/json') as response:
                data = await response.json()
        versions = sorted(map(distutils.version.LooseVersion, data['releases'])) 
        for version in versions:
            if version < MINVER or 'rc' in version.version:
                continue
            cls.versions.append(cls.loop.create_task(SaltVersion(version)()))
        await asyncio.gather(*cls.versions, loop=cls.loop)


def main():
    loop = asyncio.get_event_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), loop.stop)

    try:
        loop.run_until_complete(SaltVersion.get_versions())
    finally:
        loop.close()


if __name__ == '__main__':
    main()
