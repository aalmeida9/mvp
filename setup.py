from setuptools import setup

#not currently working
setup(
    name='Project',
    packages=['frontend', 'bc'],	#package directory 'frontend' does not exist
    include_package_data=True,
    install_requires=[
        'flask', 'requests'
    ],
)
#Flask~=1.1 and requests~=2.22
