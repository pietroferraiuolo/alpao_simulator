import os
from setuptools import setup, find_packages
from setuptools.command.install import install

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

# class CustomInstallCommand(install):
#     def run(self):
#         install.run(self)
#         bashrc = os.path.expanduser("~/.bashrc")
#         try:
#             response = input("Would you like to add the `alpy` function to your `.bashrc`? (y/n) ")
#             positives = ['y', 'Y', 'yes', 'YES', 'Yes', '']
#             if response not in positives:
#                 return
#             with open(bashrc, "a") as f:
#                 f.write(
# """
# # Added by the alpao_simulator installation
# alpy() {
#     if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
#             cat << EOF
# ALPY: 
# ipython alias to initialize the Alpao Simulator, comprehensive of a simulated alpao DM and an interferometer to acquire wavefronts.

# Arguments
# ---------
# '-97'  : initializes Alpao DM 97
# '-277' : initializes Alpao DM 277
# '-468' : initializes Alpao DM 468
# '-820' : initializes Alpao DM 820
# EOF
#     elif [ "$1" == "-88" ]; then
#         ipython3 --gui='qt' --pylab='qt' -i "/home/pietrof/git/alpao_simulator/alpao_simulator/initSimulator.py" -- --actuators 88
#     elif [ "$1" == "-97" ]; then
#         ipython3 --gui='qt' --pylab='qt' -i "/home/pietrof/git/alpao_simulator/alpao_simulator/initSimulator.py" -- --actuators 97
#     elif [ "$1" == "-277" ]; then
#         ipython3 --gui='qt' --pylab='qt' -i "/home/pietrof/git/alpao_simulator/alpao_simulator/initSimulator.py" -- --actuators 277
#     elif [ "$1" == "-468" ]; then
#         ipython3 --gui='qt' --pylab='qt' -i "/home/pietrof/git/alpao_simulator/alpao_simulator/initSimulator.py" -- --actuators 468
#     elif [ "$1" == "-820" ]; then
#         ipython3 --gui='qt' --pylab='qt' -i "/home/pietrof/git/alpao_simulator/alpao_simulator/initSimulator.py" -- --actuators 820
#     fi
# }
# """)
#             print("Updated .bashrc with the `alpy` function.")
#         except Exception as e:
#             print(f"Could not update .bashrc: {e}")

setup(
    name='alpao_simulator',
    version='0.5.0',
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
