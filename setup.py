from setuptools import setup, find_packages

#not currently working
setup(
    name='Project',
    #packages=['frontend', 'bc'],	#package directory 'frontend' does not exist
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'requests', 'pytest'
    ]
)
#Flask~=1.1 and requests~=2.22
