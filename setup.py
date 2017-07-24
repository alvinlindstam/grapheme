from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='grapheme',
      version='0.0.3',
      description=u"Unicode grapheme helpers",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Alvin Lindstam",
      author_email='alvin.lindstam@gmail.com',
      url='https://github.com/alvinlindstam/grapheme',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click'
      ],
      extras_require={
          'test': ['pytest', 'sphinx', 'sphinx-autobuild'],
      },
      entry_points="""
      [console_scripts]
      grapheme=grapheme.scripts.cli:cli
      """
      )
