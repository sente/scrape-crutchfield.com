import formatter
import glob
files = glob.glob('content/p_*/*.html')
for f in files:
    print f
    formatter.add_record(f)
len(formatter.ds)
open('ds.csv','w').write(formatter.ds.csv)
open('ds.xls','w').write(formatter.ds.xls)
open('ds.xlsx','w').write(formatter.ds.xlsx)
open('ds.json','w').write(formatter.ds.json)
open('ds.html','w').write(formatter.ds.html)
