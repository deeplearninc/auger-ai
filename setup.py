from setuptools import setup
from setuptools import find_packages

install_requires = [
    'click',
    'requests',
    'shortuuid',
    'auger-hub-api-client>=0.5.6',
]

extras = {
    'testing': ['pytest', 'pytest-cov', 'pytest-xdist', 'flake8', 'mock']
}

# Meta dependency groups.
all_deps = []
for group_name in extras:
    all_deps += extras[group_name]
extras['all'] = all_deps

setup(
    name='auger.ai',
    version='0.1',
    description=('Auger python and command line interface package'),
    author='Deep Learn',
    author_email='augerai@dplrn.com',
    url='https://github.com/deeplearninc/auger-ai',
    license='MIT',
    install_requires=install_requires,
    extras_require=extras,
    entry_points={
        'console_scripts': [
            'auger=auger.cli:cli'
        ]
    },
    packages=['auger.api', 'auger.cli']
)
