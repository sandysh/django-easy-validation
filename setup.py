from setuptools import setup, find_packages

setup(
    name='django-easy-validation',
    version='1.0.0',
    description='Easy AJAX validation for Django projects, inspired by Laravel approach.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sandesh Satyal',
    author_email='sandeshsatyal@gmail.com',
    url='https://github.com/sandysh/django-easy-validation',
    packages=find_packages(),
    keywords='django-easy-validation validation form-validation form ajax ajax-validation easy-validation laravel django ajax laravel-django laravel-validation',
    install_requires=[
        'django>=3.2',
        'regex>=2020.11.13',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
)