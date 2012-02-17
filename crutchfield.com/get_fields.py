# -*- coding: UTF-8 -*-
import urlparse
import lxml
import requests
import lxml.html
import sys
import os
import logging
import urllib
import urlparse
import random
import glob


# DELETE EMPTY LIST ELEMENTS



#def get_clean_overview(root):
#
#    for a in tree.xpath('//a'):
#        a.getparent().remove(a)
#    for foo in tree.getiterator(tag='li'):
#        print foo.tag, foo.text, len(list(foo.iterchildren()))
#        if not foo.text or len(list(foo.iterchildren())):
#            print "should delete", foo.tag

def get_breadcrumbs(root):
    ar = []
    for a in root.xpath("//div[@id='crumb-trail']/a"):
        ar.append([a.text, a.attrib['href']])
    return ar

def get_price(root):
    price = root.xpath("//span[@class='finalPrice']//child::text()")[0]
    return price


def get_overview(root):
    overview = root.xpath("//div[@id='OverviewPane']")[0]
    return lxml.html.tostring(overview).strip()

def get_overview_clean(root):
    overview = root.xpath("//div[@id='OverviewPane']")[0]
    #return lxml.html.tostring(overview).strip()
    r = lxml.html.fromstring(lxml.html.tostring(overview).strip())
    for script in r.xpath('//script'):
        script.drop_tree()
    for img in r.xpath('//img'):
        img.drop_tree()
    return lxml.html.tostring(r)


def get_overview_cleanest(root):
    overview = root.xpath("//div[@id='OverviewPane']")[0]

    r = lxml.html.fromstring(lxml.html.tostring(overview).strip())
    for script in r.xpath('//script'):
        script.drop_tree()
    for img in r.xpath('//img'):
        img.drop_tree()
    for bydiv in r.xpath("//div[@id='overviewByDiv']"):
        bydiv.drop_tree()

    for a in r.xpath('//a'):
        try:
            if a.getparent() is not None and a.getparent().tag == 'li':
                a.getparent().drop_tree()
            else:
                a.drop_tree()
        except:
            sys.stderr.write("warning...\n")
    for h3 in r.xpath('//h3'):
        if h3.text and h3.text.startswith("Our take on the"):
            h3.text = h3.text.replace("Our take on the ","")

    return lxml.html.tostring(r)


def get_shortdescription(root):
    try:
        desc = root.xpath("//span[@itemprop='description']")[0].text
        return desc.strip()
    except Exception, e:
        sys.stderr.write(str(e))
        return ""
#        sys.stderr.write("warning...")

def get_productname(root):
    name = root.xpath("//span[@itemprop='name']")[0].text
    return name.strip()

def get_canonical(root):
    #SKU

    link = root.xpath("//link[@rel='canonical']")[0]
    href = link.attrib['href']

    # href = "http://www.crutchfield.com/S-bag0SFvWQxF/p_20610C108/Kicker-10C108.html"

    return href.split('/')[-2]

def get_images(root):
    imgs = []
    for img in root.xpath("//div[@id='photoThumbHolder']/img"):
        imgs.append('http:%s' % img.attrib['src'])
    return imgs

def get_imageserver(root):
    for script in root.xpath('//script'):
        if script.text and 'imageserver' in script.text:
            s = script.text.strip().split("'")[1]
            imageserver = 'http:%s' % s
            return imageserver

def get_images2(root):
    imgs = []
    imageserver = ''
    for script in root.xpath('//script'):
        if script.text and 'imageserver' in script.text:
            s = script.text.strip().split("'")[1]
            imageserver = 'http:%s' % s

    for img in root.xpath("//div[@id='photoThumbHolder']/img"):
        url = img.attrib.get('data-cf-image-url','')
        imgurl = "%s%s" %(imageserver,url)
        imgs.append(imgurl)

    return imgs

def get_url_path(root):
    url = root.base_url
    parsed = urlparse.urlparse(url)
    return parsed.path

def get_url_key(root):
    url = root.base_url
    parsed = urlparse.urlparse(url)
    return parsed.path


def get_data(root):
    res = {}
    res['base_url'] = root.base_url
    res['breadcrumbs'] = get_breadcrumbs(root)
    res['price'] = get_price(root)
    res['overview'] = get_overview(root)
    res['overview_clean'] = get_overview_clean(root)
    res['overview_cleanest'] = get_overview_cleanest(root)
    res['shortdescription'] = get_shortdescription(root)
    res['productname'] = get_productname(root)
    res['canonical'] = get_canonical(root)
    res['images'] = get_images(root)
    res['images2'] = get_images2(root)
    res['imageserver'] = get_imageserver(root)
    res['url_key'] = get_url_key(root)
    res['url_path'] = get_url_path(root)
    res['list_images'] = list_images(root)
    return res


def save_images(root):
    res = test(root)

    savedir = 'content/%s' % res['canonical']
    os.path.basename(res['images2'][0])

    for img in res['images2']:
        imgdata = requests.get(img).content
        filename = os.path.basename(img)
        with open("%s/%s" %(savedir,filename),'wb') as ofile:
            ofile.write(imgdata)
            print "saved %s/%s" %(savedir,filename)

def list_images(root):

    images = get_images2(root)
    savedir = 'content/%s' % get_canonical(root)
    return [os.path.join(savedir,os.path.basename(i)) for i in images]


def test(url="http://www.crutchfield.com/p_575R2SD212/Rockford-Fosgate-R2SD2-12.html"):
    if url.startswith("http"):
        root = lxml.html.parse(url).getroot()
    else:
        root = lxml.html.parse(url).getroot()
    return get_data(root)

def testrandom(n=5):
    res = []
    files = glob.glob('content/*/*.html')
    shuffled = [str(w) for w in random.sample(files, len(files))]
    for f in shuffled[0:n]:
        root = lxml.html.parse(f).getroot()
        data = get_data(root)
        res.append(data)
    return res


def test5(n=5):
    res = []
    files = glob.glob('content/*/*.html')
    for f in files[0:n]:
        print f
        root = lxml.html.parse(f).getroot()
        data = get_data(root)
        res.append(data)
    return res

if __name__ == '__main__':
    import pprint
    pprint.pprint(testrandom(100))
