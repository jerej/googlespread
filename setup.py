from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='googlespread',
      version='0.1',
      description='Simplify access to Google Spreadsheets API',
      long_description=readme(),
      keywords='google spreadsheet openauth oauth',
      url='http://github.com/julianje',
      author='Jere Julian',
      author_email='github@StageRigger.com',
      license='BSD',
      packages=['googlespread'],
      zip_safe=False,
      install_requires=[
          'gdata',
          'python-gflags',
          'oauth2client'
      ])
