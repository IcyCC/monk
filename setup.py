from setuptools import setup, find_packages

setup(name='monk',

      version='0.0.1',

      url='https://github.com/IcyCC/monk',

      license='MIT',

      author='SuChang',

      author_email='sam.suchang@qq.com',

      description='https://github.com/IcyCC/monk',

      packages=find_packages(exclude=['monk']),

      long_description=open('README.md').read(),

      zip_safe=False,
)