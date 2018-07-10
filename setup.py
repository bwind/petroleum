from setuptools import setup

setup(
    name='petroleum',
    version="1.0.0",
    author='Bas Wind',
    author_email='mailtobwind+petroleum@gmail.com',
    description='A pure workflow engine for Python',
    url='https://github.com/bwind/petroleum',
    packages=['petroleum'],
    install_requires=open('requirements.txt', 'r').readlines(),
    include_package_data=True,
    long_description=open('README.md').read(),
)
