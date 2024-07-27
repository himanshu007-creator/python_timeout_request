from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="your-package-name",
    version="0.1.0",
    author="Himanshu",
    author_email="addyjeridiq@gmail.com",
    description="A simple package to add timeout to requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/himanshu007-creator/request-timeout",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorlog>=6.7.0",
    ],
    extras_require={
        "test": ["pytest>=7.3.1", "pytest-asyncio>=0.21.0"],
    },
)