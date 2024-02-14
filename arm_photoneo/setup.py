from setuptools import setup, find_packages

setup(
    name='arm_photoneo',
    version='0.0.1',
    url='https://github.com/UM-ARM-Lab/arm_photoneo.git',
    author='Peter Mitrano',
    author_email='pmitrano@umich.edu',
    description='non-ros python package to make using our Photoneo easier',
    packages=find_packages(),    
    install_requires=[
        'harvesters>=1.4.0',
        'numpy>=1.22.4',
        'open3d>=0.16.0',
        'ppencv_python>=4.6.0.66',
    ]
)
