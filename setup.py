from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='grapheme',
      version='0.6.0',
      description=u"Unicode grapheme helpers",
      long_description=long_description,
      keywords='',
      author=u"Alvin Lindstam",
      author_email='alvin.lindstam@gmail.com',
      url='https://github.com/alvinlindstam/grapheme',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require={
          'test': ['pytest', 'sphinx', 'sphinx-autobuild', 'wheel', 'twine']
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
      ],
      )
