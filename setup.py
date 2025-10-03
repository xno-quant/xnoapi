from setuptools import find_packages, setup

setup(
    name="xnoapi",
    version="0.1.26",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
    ],
    author="xno_project",
    description="XNO API Library for Financial Data",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
)
