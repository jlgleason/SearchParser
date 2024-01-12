from setuptools import setup, find_packages

setup(
    name="SearchParser",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4", "lxml", "pyppeteer"],
    author="Jeffrey Gleason",
    author_email="gleason.je@northeastern.edu",
    description="Simple web scraper/parser that can run searches on Bing/DuckDuckGo and extract ad/general results from their SERPs.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
