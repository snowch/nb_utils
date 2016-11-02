from distutils.core import setup

setup(
  name='cf_utils',
  version='0.1',
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/snowch/cf_utils/',
  packages=['cf_utils', 'ssh_utils'],
  install_requires=[
          'cloudfoundry-client',
          'paramiko',
          'scp'
      ],
)
