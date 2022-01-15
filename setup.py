import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="genpyteal",
    version="1.0.0",
    description="Generate PyTeal with normal Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/runvnc/genpyteal",
    author="runvnc (Jason Livesay)",
    author_email="runvnc@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["redbaron", "pyteal"],
    scripts=['./genpyteal', './genteal', './showast', './niceout', './nicecat']
)
