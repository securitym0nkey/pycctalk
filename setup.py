from setuptools import setup

setup(name='pycctalk',
      version='0.1',
      description='Python implementation of the ccTalk protocol. Currently focused on coin acceptors.',
      url='http://',
      author='Julian Wecke',
      author_email='julian@net23.de',
      license='',
      packages=['cctalk','cctalk.tools'],
      install_requires=['pyserial'],
      zip_safe=False)

