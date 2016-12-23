# Farsight dnsdb.info client
# Getting Started

## Commandline
```bash
$ export FARSIGHT_TOKEN=1234
$ pip install csirtg_dnsdb
$ dnsdb --search 172.217.6.206
$ dnsdb -q google.com
```

## SDK
```python
from pprint import pprint
import json
from csirtg_dnsdb.client import Client

p = ArgumentParser(
    description=textwrap.dedent('''\
    example usage:
        $ dnsdb -q 1.2.3.4
    '''),
    formatter_class=RawDescriptionHelpFormatter,
    prog='dnsdb',
)
p.add_argument('--token', help='specify api token', default=TOKEN)
p.add_argument('--search', '-q', help='search for something')
args = p.parse_args()

c = Client(token=args.token)

for r in c.search(args.search):
    print(json.dumps(r))
```

# Getting Involved
There are many ways to get involved with the project. If you have a new and exciting feature, or even a simple bugfix, simply [fork the repo](https://help.github.com/articles/fork-a-repo), create some simple test cases, [generate a pull-request](https://help.github.com/articles/using-pull-requests) and give yourself credit!

If you've never worked on a GitHub project, [this is a good piece](https://guides.github.com/activities/contributing-to-open-source) for getting started.

* [How To Contribute](contributing.md)

# Development
## Some of the tools we use:

* [PyCharm](https://www.jetbrains.com/pycharm/)
* [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
* [Vagrant](https://www.vagrantup.com/)

# COPYRIGHT AND LICENCE

Copyright (C) 2016 [the CSIRT Gadgets Foundation](http://csirtgadgets.org)

Free use of this software is granted under the terms of the Mozilla Public Licence v2 (MPL2). For details see the files `LICENSE` included with the distribution.
