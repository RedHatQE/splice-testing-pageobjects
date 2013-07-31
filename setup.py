from setuptools import setup, find_packages

setup(name='pageobjects',
    version=0.1,
    description='Page objects of Splice WebUI for test automation',
    author='dparalen',
    license='GPLv3+',
    install_requires=['selenium_wrapper'],
    package_data = {
        'pageobjects': ['data/*.yml']
    },
    classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Operating System :: POSIX',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
    ],
    packages = find_packages(exclude=['tests']),
    )
