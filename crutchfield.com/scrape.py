# -*- coding: UTF-8 -*-
import lxml
import requests
import lxml.html
import sys
import os
import logging
import urllib
import urlparse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#logger.setLevel(logging.DEBUG)


if len(sys.argv) < 2:
    url = 'http://www.crutchfield.com/g_520/Component-Subwoofers.html?tp=111&showAll=Y'
else:
    url = sys.argv[1]


def crawl_category(root):


    for plink in root.xpath("//div/div[@id='productList-block-container']/div[@class='productList-block']/div[@class='productList-desc']/h3/a"):
        try:
            text = "%s\t%s\t%s" %(plink.sourceline, plink.attrib['href'], plink.text.strip())
            url = plink.attrib['href']

            download_item_page(url)
        except Exception, e:
            logger.exception('wtf')


def download_item_page(url):

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


    print "saved %s to %s" % (url, destination)


def main():

    content = requests.get(url).content.decode('utf-8')
    root = lxml.html.fromstring(content, base_url=url)
    root.make_links_absolute()

    crawl_category(root)

if __name__ == '__main__':
    main()


# http://www.crutchfield.com/g_51000/Powered-Subwoofers.html?tp=114&showAll=Y
# http://www.crutchfield.com/g_510/Enclosed-Subwoofers.html?tp=112&showAll=Y
# http://www.crutchfield.com/g_520/Component-Subwoofers.html?tp=111&showAll=Y
