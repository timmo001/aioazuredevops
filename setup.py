"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()

setuptools.setup(
    name="aioazuredevops",
    version="1.3.3",
    author="Timmo",
    author_email="contact@timmo.xyz",
    description="Get data from the Azure DevOps API.",
    long_description=LONG,
    long_description_content_type="text/markdown",
    install_requires=[
        'aiohttp==3.6.2',
        'click==7.1.2'
    ],
    entry_points={
        'console_scripts': [
            'aioazuredevops = aioazuredevops.cli:cli'
        ]
    },
    url="https://github.com/timmo001/aioazuredevops",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
