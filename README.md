# imovirtual-scrapper
 **What does this do?**
 
 It scrapes imovirtual.com
 
 **How do I install it?**
 
 1 - Clone repository
 
 2 - Run 
 
    pipenv sync
 
 3 - Cd into 
 
    imovirtual/imovirtual
 
 4 - Run 
       
    scrapy crawl imo 
 
If you want to save the scrapped items to disk in one of the default formats supported by scrapy run:
      
      scrapy crawl imo --output=OUTPUT_FILENAME --output-format=FORMAT [xml/json/jsonlines/csv]