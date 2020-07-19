from setuptools import setup, find_packages

setup(
    name="aoe2-ai-fmt",
    version="0.1",
    packages=find_packages(),
    scripts=["format.py"],

    python_requires=">=3.6",
    install_requires=["antlr4-python3-runtime==4.8"],
)
