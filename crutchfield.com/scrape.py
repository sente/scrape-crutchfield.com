# -*- coding: UTF-8 -*-
import lxml
import time
import requests
import lxml.html
import sys
import os
import logging
import urllib
import urlparse


from scrapelogging import get_scrape_logger
#logger = get_scrape_logger('stu')





def logging(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    def wrapper(*args, **kwargs):

        declog = open("logs/decorator.log","a")
        declog.write('%s\t%s\t%s\n' %(func.__name__, str(args), str(kwargs)))
        declog.close()

        res = func(*args, **kwargs)
#        print func.__name__, args, kwargs
        return res
    return wrapper


@logging
def crawl_category(root,logger):


    for plink in root.xpath("//div/div[@id='productList-block-container']/div[@class='productList-block']/div[@class='productList-desc']/h3/a"):
        try:
            text = "%s\t%s\t%s" %(plink.sourceline, plink.attrib['href'], plink.text.strip())
            url = plink.attrib['href']

            logger.info('DOWN\t%s' % url)
            download_item_page(url,logger)
        except Exception, e:
            logger.exception('wtf %s' % url)
            time.sleep(1)

@logging
def download_item_page(url,logger):

    content = requests.get(url).content

    destination = urlparse.urlsplit(url).path
    destination = "./content%s" % destination
    dest_dir = os.path.dirname(destination)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    #requests.get(url).content
    root = lxml.html.parse(url).getroot()
    with open(destination,'w') as ofile:
        ofile.write(lxml.html.tostring(root))

    root.make_links_absolute()

    with open(destination.replace('html','abs'),'w') as ofile:
        ofile.write(lxml.html.tostring(root))

    with open(destination.replace('html','orig'),'w') as ofile:
        ofile.write(content)

    logger.info("SAVED\t%s" % destination)
#    logger.info("SAVED:\t%s\t%s\t%s" % (sku, destination, url))


@logging
def scrape_data(count,section,category,subcategory,url):
    sku = url.split('/')[4]
    logger = get_scrape_logger("%d:%s:%s:%s" %(count,section,category,subcategory))
    logger.debug('BEGIN\t%s' % url)

    content = requests.get(url).content.decode('utf-8')
    root = lxml.html.fromstring(content, base_url=url)
    root.make_links_absolute()
    logger.warn('SAVED\t%d %s' %(len(content),url))

    crawl_category(root,logger)
    logger.debug('END\t%s' %url)


def main():

    ifile = open('info/product_listing.dat','r')

    for count,line in enumerate(ifile):
        if count <= 20:
            continue
        section,category,subcategory,url = line.strip().split('\t')
        url=url+"&showAll=Y"
        scrape_data(count,section,category,subcategory,url)
        time.sleep(1)


if __name__ == '__main__':
    main()


# http://www.crutchfield.com/g_51000/Powered-Subwoofers.html?tp=114&showAll=Y
# http://www.crutchfield.com/g_510/Enclosed-Subwoofers.html?tp=112&showAll=Y
# http://www.crutchfield.com/g_520/Component-Subwoofers.html?tp=111&showAll=Y
