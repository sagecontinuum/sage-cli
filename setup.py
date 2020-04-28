#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='sage-cli',
    version='0.1',
    description='SAGE command line interface',
    url='https://github.com/sagecontinuum/sage-cli',
    install_requires=[
        'sage-storage-py @ git+https://github.com/sagecontinuum/sage-storage-py.git',
                        
        #'git+https://github.com/sagecontinuum/sage-storage-py.git',
        #'sage_storage @ git+https://github.com/sagecontinuum/sage-storage-py.git',
        'click',
    ],
    #dependency_links=['http://github.com/sagecontinuum/sage-storage-py/tarball/master#egg=sage_storage-0.1'],
    # pip install  git+https://github.com/sagecontinuum/sage-storage-py.git
    scripts=['sage-cli.py'],
    include_package_data=True,
)