#!/usr/bin/env python
"""Setup script for agri-data-toolkit."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agri-data-toolkit",
    version="0.1.0",
    author="Clayton Young",
    author_email="claytoneyoung+github@gmail.com",
    description="Agricultural Data Analytics Course - Python toolkit for US row crop data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/borealBytes/agri-data-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/borealBytes/agri-data-toolkit/issues",
        "Documentation": "https://github.com/borealBytes/agri-data-toolkit/tree/main/docs",
        "Source Code": "https://github.com/borealBytes/agri-data-toolkit",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "agri-download=agri_toolkit.cli:download",
            "agri-validate=agri_toolkit.cli:validate",
            "agri-report=agri_toolkit.cli:report",
        ],
    },
)
