from setuptools import setup, find_packages
from pathlib import Path

def read_requirements():
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        with open(requirements_file) as f:
            return f.readlines()
    return []

setup(
    name="tuna-sbn",
    version="1.1.2",
    description="A Python CLI for managin training/testing workflows application in ICARUS/SBN reconstruction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mattia Sotgia",
    author_email="mattia.sotgia@ge.infn.it",
    url="https://baltig.infn.it/msotgia/tuna.git",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tuna = tuna.cli:main", 
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    include_package_data=True,
    zip_safe=False,
)
