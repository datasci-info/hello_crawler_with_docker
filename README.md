# crawlers

## Using Guide
- ### Step1: install the package into your python environment:
```
python setup.py install 
```
- ### Step2: setting up your local_settings.py in the bin/ and /dev-ipynbs folders
```
cp .example.local_settings.py bin/local_settings.py
```
- ### Step3: use executable scripts in bin/ folder to get the data from website
   * https://github.com/datasci-info/hello_crawler_with_docker/tree/master/bin


## Development Guide:
- ### Step 0: start mongo by docker

```sh
docker-compose up -d 
```

- ### Step 1: find the data page and write trial script in dev-ipynbs/ folder, for examples:
   * https://github.com/datasci-info/hello_crawler_with_docker/blob/master/dev-ipynbs/Vanger/product_data___try.ipynb
   * https://github.com/datasci-info/hello_crawler_with_docker/blob/master/dev-ipynbs/Vanger/page_data___try.ipynb
   * write the product page first then the navigator (or category) pages 

- ### Step 2: pack your crawling script into functions, for examples: 
   * https://github.com/datasci-info/hello_crawler_with_docker/blob/master/dev-ipynbs/Vanger/product_data___pack_into_function.ipynb
   * https://github.com/datasci-info/hello_crawler_with_docker/blob/master/dev-ipynbs/Vanger/page_data___pack_into_function.ipynb
   
- ### Setp 3: write the draft of your executable script, for example:
   * https://github.com/datasci-info/hello_crawler_with_docker/blob/master/dev-ipynbs/Vanger/executable_script_try.ipynb
   
- ### Setp 4: seperate your draft of executable script into package part and executable script part:
   * [package part] https://github.com/datasci-info/hello_crawler_with_docker/blob/master/mystyle_crawlers/vanger/__init__.py
   * [executable script part] https://github.com/datasci-info/hello_crawler_with_docker/blob/master/bin/vander__get_data.py
   
