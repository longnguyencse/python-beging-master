import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

with open('./requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="Example numpy",
    version="0.0.1",
    author="Example",
    author_email="author@example.com",
    description="A small example package",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    # install_requires=install_requires,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# install_requires=read('requirements.txt').strip().splitlines(),