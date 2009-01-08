#!/usr/bin/env python

from distutils.core import setup
import queues
setup(name='queues',
      version='0.2',
      description='A lowest-common-denominator API for interacting with lightweight queue services.',
      author='Matt Croydon',
      author_email='mcroydon@gmail.com',
      url='http://postneo.com', # TODO: Fixme
      packages=['queues', 'queues.backends'],
      package_dir={'queues': 'queues'},
     )
