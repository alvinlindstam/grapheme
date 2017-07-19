from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='grapheme',
      version='0.0.1',
      description=u"Skeleton of a Python package",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Sean Gillies",
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/grapheme',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      grapheme=grapheme.scripts.cli:cli
      """
      )
