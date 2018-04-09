#!/usr/bin/env python

import sys,os

if len(sys.argv)< 2:
    print "Usage: makeTool.py <package-name> ..."
    sys.exit(1)


thisDir=os.path.dirname(sys.argv[0])

for p in sys.argv[1:]:
    print "Making "+p+"-toolfile.spec"
    fIn=open(os.path.join(thisDir,"toolfile_template.txt"))
    fOut=open(p+"-toolfile.spec","w")
    pCaps=p.upper()
    pCaps='_'.join(pCaps.split('-'))
    for l in fIn:
        l=l.replace("<toolname>",p)
        l=l.replace("<capsname>",pCaps)
        print l,
        fOut.write(l)
    fOut.close()
    fIn.close()

