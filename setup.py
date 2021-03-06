from setuptools import setup


setup(
    name="Flask-StatHat",
    version='0.1.0',
    url='https://github.com/marksteve/flask-stathat',
    license='MIT',
    author="Mark Steve Samson",
    author_email='hello@marksteve.com',
    zip_safe=False,
    description="StatHat extension for Flask",
    py_modules=['flask_stathat'],
    install_requires=[
        'requests>=2.0,<3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
