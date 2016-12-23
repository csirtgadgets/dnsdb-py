import os
import sys
from setuptools import setup, find_packages
import versioneer

# vagrant doesn't appreciate hard-linking
if os.environ.get('USER') == 'vagrant' or os.path.isdir('/vagrant'):
    del os.link

# https://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirements." % err_msg
        raise ImportError(msg)
    r = os.system('py.test test -v')
    if r == 0:
        sys.exit()
    else:
        raise RuntimeError('tests failed')

setup(
    name="csirtg_dnsdb",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="DNSDB Client",
    long_description="Software Development Kit for DNSDB",
    url="https://github.com/csirtgadgets/dnsdb-py",
    license='MPL2',
    classifiers=[
               "Topic :: System :: Networking",
               "Intended Audience :: Developers",
               "Programming Language :: Python",
               ],
    keywords=['security'],
    author="Wes Young",
    author_email="wes@csirtgadgets.org",
    packages=find_packages(),
    install_requires=[
        'requests>=2.6.0',
        'pytest>=2.8.0',
        'ujson>=1.35',
    ],
    scripts=[],
    entry_points={
        'console_scripts': [
            'dnsdb=csirtg_dnsdb.client:main',
        ]
    },
)
