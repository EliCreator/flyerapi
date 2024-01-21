import os
import codecs

from setuptools import setup, find_packages


VERSION = '1.0.6'
DESCRIPTION = 'Asynchronous api of the Flyer service'

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='flyerapi',
    version=VERSION,
    author='Eli',
    author_email='<eli.dev.tg@gmail.com>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['aiohttp'],
    keywords=['python', 'flyer', 'async', 'asyncio', 'cache'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    url='https://github.com/EliCreator/flyerapi',
    project_urls={
        'Homepage': 'https://github.com/EliCreator/flyerapi',
        'Bug Tracker': 'https://github.com/EliCreator/flyerapi/issues',
    },
)