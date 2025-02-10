from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

setup(
    name='alpao_simulator',
    version='0.1.0',
    author='INAF OAA-AO Group',
    author_email='pietro.ferraiuolo@inaf.it',
    description='A simulator for ALPAO deformable mirrors',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pietroferraiuolo/alpao_simulator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            # Add any command line scripts here
        ],
    },
)
