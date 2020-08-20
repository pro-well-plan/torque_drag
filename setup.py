from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='torque_drag',
    packages=['torque_drag'],
    version='0.0.2',
    license='LGPL v3',
    description='Torque and Drag Calculation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Pro Well Plan AS',
    author_email='juan@prowellplan.com',
    url='https://github.com/pro-well-plan/torque_drag',
    keywords='drilling',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Natural Language :: English',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Software Development',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'],
)
