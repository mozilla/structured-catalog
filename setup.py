# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

PACKAGE_VERSION = '0.1'

deps = [
    'mozillapulse',
    'mozlog',
    'mozfile',
    'requests',
]

setup(name='structured-catalog',
      version=PACKAGE_VERSION,
      description='Downloads structured test logs and stores the result',
      long_description='See https://github.com/mozilla/structured-catalog',
      classifiers=['Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords='mozilla',
      author='Andrew Halberstadt',
      author_email='ahalberstadt@mozilla.com',
      url='https://github.com/mozilla/structured-catalog',
      license='MPL 2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points="""
        [console_scripts]
        catalog-listener = catalog.pulse.run_listener:cli
        catalog-worker = catalog.worker.run_worker:cli
      """)
