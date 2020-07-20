from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="aoe2-ai-fmt",
    version="0.1",
    description="A formatter for AoE2 AI rule files (.per).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="George Field",
    author_email="george@cucurbit.dev",
    url="https://github.com/ks07/aoe2-ai-fmt",
    packages=find_packages(),
    scripts=["format.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Development Status :: 3 - Alpha",
    ],

    python_requires=">=3.6",
    install_requires=["antlr4-python3-runtime==4.8"],
)
