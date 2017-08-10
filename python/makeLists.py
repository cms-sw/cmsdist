#!/usr/bin/env python

import os

def findFiles(baseDir,ending):
    l=[]
    for root, dirs, files in os.walk(baseDir):
        for file in files:
            if file.endswith(ending):
                l.append(os.path.join(root,file))

    return l


specs=findFiles('./CMSDIST','spec')

pips={}
for spec in specs:
    isPip=0
    pipInfo={'version':None,
             'name': 'None',
             'dependencies': []}

    for l in open(spec):
        if 'build-with-pip' in l: isPip=1
        if '### RPM' in l : 
#            print l,
            pipInfo['name']=l.strip().split()[3][4:] #remove the py2-
            pipInfo['version']=l.strip().split()[4]
        if 'define pip_name' in l:
            pipInfo['name']=l.strip().split()[2]
        if 'Requires' in l:
            sp=l.strip().split()[1:]
            for p in sp:
                if 'py2-' in p: continue
                pipInfo['dependencies'].append(p)

    if isPip>0:
        pips[pipInfo['name']]=(pipInfo)


#add numpy and matplotlib
pipInfo={'version':None,
         'name': 'numpy',
         'dependencies': []}

for l in open('./CMSDIST/py2-numpy.spec'):    
    if '### RPM' in l : 
        pipInfo['version']=l.strip().split()[4]
pips[pipInfo['name']]=(pipInfo)

pipInfo={'version':None,
         'name': 'matplotlib',
         'dependencies': []}

for l in open('./CMSDIST/py2-matplotlib.spec'):    
    if '### RPM' in l : 
        pipInfo['version']=l.strip().split()[4]
pips[pipInfo['name']]=(pipInfo)
    

for i in pips:
    pip=pips[i]
    print "'"+pip['name']+"=="+pip['version']+"', #",
    for d in pip['dependencies']:
        print d+' ',
    print ''


        
