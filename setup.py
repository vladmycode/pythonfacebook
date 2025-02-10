from setuptools import find_packages, setup

setup(
    name="pythonfacebook",
    version="0.1.0",
    description="A Python library for interacting with Facebook API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vlad Andrei",
    author_email="contact@vlad.my",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
