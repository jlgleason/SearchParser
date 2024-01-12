# SearchParser
Simple web scraper/parser that can run searches on Bing/DuckDuckGo and extract ad/general results from their SERPs

## Installation

`pip3 install git+https://github.com/jlgleason/SearchParser`

## Usage

### Test with 1 query: 

``python3 test.py -s bing -q "hello world"``

### Crawl multiple queries: 

``python3 main.py -s ddg --fp_qrys qrys.txt --fp_parsed results.json``

