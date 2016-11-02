from distutils.core import setup

setup(
  name='nb_utils',
  version='0.1',
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/snowch/nb_utils/',
  packages=['cf_utils', 'ssh_utils', 'mh_utils'],
  install_requires=[
          'cloudfoundry-client',
          'paramiko',
          'scp',
          'kafka-python'
      ],
)
