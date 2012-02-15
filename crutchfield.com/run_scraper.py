
ifile = open('info/product_listing.dat','r')

for line in ifile:
    section,category,subcategory,url = line.strip().split('\t')
#    print section,category, subcategory, url
    sku = url.split('/')[3]
    print 'python scrape.py "%s" "%s"' % (sku, url)
