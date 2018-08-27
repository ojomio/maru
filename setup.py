import codecs
import os
import re
import sys
import shutil

import setuptools

PACKAGE = 'maru'
ROOT = os.path.dirname(os.path.abspath(__file__))


def get_path(filename):
    return os.path.join(ROOT, filename)


def get_version():
    pattern = re.compile(r'__version__\s*=\s*\'(?P<version>\d+\.\d+\.\d+)\'')
    with codecs.open(get_path('{}/__init__.py'.format(PACKAGE))) as f:
        match = pattern.search(f.read())
        if match is not None:
            return match.group('version')

        raise ValueError('Version not found for package "{}"'.format(PACKAGE))


def get_description():
    with codecs.open(get_path('README.rst'), encoding='utf-8') as f:
        return '\n' + f.read()


def get_requirements():
    requirements = []

    with codecs.open(get_path('requirements.txt'), encoding='utf-8') as f:
        for requirement in f:
            if '#' in requirement:
                requirement, _, _ = requirement.partition('#')

            requirement = requirement.strip()
            if requirement and not requirement.startswith('-r '):
                requirements.append(requirement)

    return requirements


def get_extra_requirements():
    return {
        'gpu': [
            'tensorflow-gpu',
        ]
    }


def print_in_bold(text: str):
    print(f'\033[1m{text}\033[0m')


class UploadCommand(setuptools.Command):
    """
    Support setup.py upload
    """
    description = 'Build the package and upload it to PyPI'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print_in_bold('Removing previous builds...')
        shutil.rmtree('dist', ignore_errors=True)

        print_in_bold('Building source distribution...')
        os.system(f'{sys.executable} setup.py sdist bdist_wheel')

        print_in_bold('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        print_in_bold('Pushing git tags...')
        os.system(f'git tag v{get_version()}')
        os.system('git push --tags')

        sys.exit()


setuptools.setup(
    name=PACKAGE,
    version=get_version(),
    description='Morphological Analyzer for Russian',
    long_description=get_description(),
    author='Vladislav Blinov',
    author_email='cunningplan@yandex.ru',
    url='https://github.com/chomechome/maru',
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=get_requirements(),
    extras_require=get_extra_requirements(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
