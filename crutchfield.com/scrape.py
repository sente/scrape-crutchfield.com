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



#for p in root.xpath("//div/div[@id='productList-block-container']"):
#    print 'outer loop'
#    for c in p.xpath('./div/div/a'):
#        print '\tinner loop'
#        print c.sourceline,c.tag,c.attrib.get('href','')
#    for c in p.xpath('./div/div/a/child::text()'):
#        print c



def crawl_category(root):


    for plink in root.xpath("//div/div[@id='productList-block-container']/div[@class='productList-block']/div[@class='productList-desc']/h3/a"):
        try:
            text = "%s\t%s\t%s" %(plink.sourceline, plink.attrib['href'], plink.text.strip())
            print text.encode('utf-8')
            url = plink.attrib['href']

            download_item_page(url)
        except Exception, e:
            print plink.sourceline
            logger.exception('wtf')


def download_item_page(url):



    destination = urlparse.urlsplit(url).path
    destination = "./content%s" % destination
    dest_dir = os.path.dirname(destination)
    print dest_dir, destination
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    #requests.get(url).content
    root = lxml.html.parse(url).getroot()
    with open(destination,'w') as ofile:
        ofile.write(lxml.html.tostring(root))

    print "saved %s to %s" % (url, destination)


def main():

    content = requests.get(url).content.decode('utf-8')
    root = lxml.html.fromstring(content, base_url=url)
    root.make_links_absolute()

    crawl_category(root)

if __name__ == '__main__':
    main()



#
#
#
#for alink in root.xpath("//div/div[@id='productList-block-container']/div[@class='productList-block']/div[@class='productList-desc']/a"):
#    print alink
#
#
#
#


# http://www.crutchfield.com/g_51000/Powered-Subwoofers.html?tp=114&showAll=Y
# http://www.crutchfield.com/g_510/Enclosed-Subwoofers.html?tp=112&showAll=Y
# http://www.crutchfield.com/g_520/Component-Subwoofers.html?tp=111&showAll=Y
