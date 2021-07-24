import setuptools

long_description=""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blackscholes", 
    version="1.0.0",
    author="Flios",
    author_email="yantengxiao@gmail.com",
    description="Black Scholes model for option pricing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)