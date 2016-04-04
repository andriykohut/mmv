import setuptools

setuptools.setup(
    name="mmv",
    version="0.0.1",
    url="https://github.com/andriykohut/mmv",

    author="Andriy Kogut",
    author_email="kogut.andriy@gmail.com",

    description="Small script to enforce some directory structure on my music",

    packages=setuptools.find_packages(),

    install_requires=['tinytag'],

    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    entry_points={
        'console_scripts': [
            'mmv=mmv.mmv:main',
        ],
    },
)
