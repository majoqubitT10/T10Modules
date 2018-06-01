from setuptools import setup, find_packages

setup(
    name='T10Modules',
    version='0.1',
    description='Classes and function for the convenience of T10 users',
    url='https://github.com/majoqubitT10/T10Modules',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Licence :: MIT Licence',
        'Topic :: Scientific/Engineering'
    ],
    license='MIT',
    packages=find_packages(),
    package_data={'qcodes': ['config/*.json']},
    install_requires=[
        'matplotlib>=2.0.2',
        'scipy>=1.1.0',
        'python-pptx>=0.6.9',
        'qcodes>=0.1.9',
    ],
    python_requires='>=3'
)