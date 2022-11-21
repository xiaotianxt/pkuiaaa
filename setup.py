import unittest
from setuptools import find_packages, setup


if __name__ == "__main__":
    setup(
        name='pkuiaaa',
        packages=find_packages(include=['pkuiaaa']),
        version='0.1.2',
        description='Returns you a iaaa.pku.edu.cn logged in session.',
        author='xiaotianxt',
        license='MIT',
        requires=['requests'],
        test_suite='tests',
    )
