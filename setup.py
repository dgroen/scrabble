"""Setup file for the Scrabble game package."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrabble",
    version="0.1.0",
    author="scrabble",
    description="An online Scrabble game with official rules validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dgroen/scrabble",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "tox>=4.0",
            "black>=23.1",
            "isort>=5.10",
            "flake8>=5.0",
            "mypy>=1.0",
            "pre-commit>=3.0",
        ],
    },
)
