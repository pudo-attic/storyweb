from setuptools import setup, find_packages

setup(
    name='storyweb',
    version='0.1',
    description="Create story networks out of text snippets.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='sql influence networks journalism ddj entities',
    author='Annabel Church, Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://granoproject.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={},
    tests_require=[]
)
