# Data Collection Pipeline

This project will involve the implementation of an industry grade data collection pipeline that runs scalably in the cloud.

## Table of Contents:
* [Technologies](#technologies)
* [Milestone 1](#milestone-1)
* [Milestone 2](#milestone-2)
* [Milestone 3](#milestone-3)
* [Milestone 4](#milestone-4)
* [Milestone 5](#milestone-5)
* [Milestone 6](#milestone-6)
* [Milestone 7](#milestone-7)

## Technologies
* Pycharm 
* BeautifulSoup/request library
* AWS (Amazon Webservices)

## Milestone 1
This mainly involved deciding which website to scrape. I decided that i will be scraping the website Arcade-World. The user will enter the product name which will then 
generate the results into both a pandas dataframe object as well as a json file type which can then be stored into the cloud via AWS (Amazon Web Services)

## Milestone 2
This section will involve creating the scraper class. The class will include a number of methods to allow the user to extract the dataset they need through manipulating
the html code. These are the methods that will be included within the class initially:
```python
def gui_search(query: str):
# Using tkinter will allow user to enter product on a gui object rather then the terminal
def get_status(self):
# using request library this method will get the status_code for the url
def search_product(self):
# User can enter their product which will then be processed onto the website
def return_soup(self):
# Method to return BeautifulSoup object
def print_html(self):
# Uses Bs4.prettify to print html in readable format
def pagination(self):
# Method for allowing us to later loop through each page to extract the data
def extract_into_list(self):
# Method extracts results into a list

```
The data will then be stored into a second class labelled "Data" this will be then converted into a dictionary for later use
```python

class Data:
    # constructor with datafields.
    def __init__(self, uuid, product_id, product_name=None, price=None, summary=None):
        self.product_name = product_name
        self.price = price
        self.summary = summary
        self.uuid = uuid
        self.product_id = product_id

    def __repr__(self):
        return f"Unique ID={self.uuid}, Product ID={self.product_id} Product={self.product_name}, " \
               f"Price={self.price}, Summary={self.summary}"

    def to_dict(self):
        return {"Unique iD": self.uuid, "Product ID": self.product_id, "Product": self.product_name,
                "Price": self.price, "Summary": self.summary}
```
## Milestone 3
The 5 data points that will be scraped on the site will be the following:
- Product ID
- Product Name
- Price
- Summary
- Image URL 

THis will include scraping using a combination of html tags as well as utilising the CSS selector for the extraction of some custom attributes. Using the UUIDv4 package, i will also generate a globally unique ID for each entry.

```python
import uuid as uid

def generate_id(results:list = None):
    unique_id = []
    for id in enumerate(results):
        uuidv4 = uid.uuid4()
        unique_id.append(str(uuidv4))
    return unique_id
```
There are two methods that will be used to extract the data being the "extract_into_list" method as well as the "extract_css_selector" method. These will take multiple parameters allowing the flexibility for customising the query. Once extracted it will then be stored into a dictionary which will map the feature name and value. This will be done via the "to_dict" method in the "Data" class.

The raw data will thus be stored in a json file via the store data method within the scraper class

```python
    def store_data(data: dict):
        # method stores raw data into a local directory
        path = "/home/hamza/PycharmProjects/AICoreProject_DataCollection/raw_data"
        is_exist = os.path.exists(path)

        if not is_exist:
            os.makedirs(path)
            print("New directory created!")
        if not isinstance(data, dict):
            raise TypeError
        else:
            with open(join(path, "data.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print("json file created!")

```
For extracting the image URL this will be embedded in my extract method. Due to the websites html structure the image urls are stored in custom attributes which i found utilising the CSS selector method to be the easiest. Using the with open method each image file will be stored in the images folder which will be named images followed by the index number as well as the extension e.g (images1.jpeg). 

```python
    def extract_css_selector(self, soup_obj=None, text: str = None, attribute=None):
        empty_list = []

        soup_obj = self.return_soup() if soup_obj is None else soup_obj

        css_selector = soup_obj.select(text)
        counter = 0

        for container in css_selector:
            if "http" in container[attribute]:
                counter += 1
                path = "/home/hamza/PycharmProjects/AICoreProject_DataCollection/images"
                img = container[attribute]
                with open(join(path, f"image{counter}.jpeg"), "wb") as f:
                    f.write(requests.get(img).content)
                    empty_list.append(container[attribute])
            else:
                empty_list.append(container[attribute])
        return empty_list
``````
## Milestone 4

## Milestone 5

## Milestone 6

## Milestone 7
