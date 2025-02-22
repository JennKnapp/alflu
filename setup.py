from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='alflu',
    version='0.1.2',
    description='Identify frequencies of mutations from aligned reads',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jenn Knapp', 
    author_email='jenn.knapp@uwaterloo.ca',
    packages=['alflu'],
    url='https://github.com/JennKnapp/alflu',
    install_requires=[
        'fire',
        'numpy',
        'pandas',
        'scikit-learn>=0.24',
        'matplotlib',
        'seaborn',
        'pysam',
    ],
    entry_points={
        'console_scripts': ['alflu=alflu.command_line:main'],
    }
)
