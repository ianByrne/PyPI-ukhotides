from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ukhotides',
    version='1.0.0',
    description='Python library for interfacing with the UKHO Admiralty Tidal API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ianByrne/PyPI-ukhotides',
    download_url='https://github.com/ianByrne/PyPI-ukhotides/archive/v1.0.0.tar.gz',
    author='Ian Byrne',
    author_email='ian.byrne@burnsie.com.au',
    license='MIT',
    packages=['ukhotides'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ]
)
