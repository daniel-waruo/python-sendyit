import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-sendy-it",  # Replace with your own username
    version="0.0.1",
    author="Daniel Waruo",
    author_email="waruodaniel@gmail.com",
    description="A python wrapper for the Sendy IT API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniel-waruo/python-sendy-it",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
