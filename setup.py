from setuptools import setup, find_packages

setup(
    name='mystyle_crawlers',
    version='0.0.1',
    description='myStyle Crawlers',
    author='George Chang',
    author_email='George Chang <george@mystyle.design>',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'pyquery'
    ],
)