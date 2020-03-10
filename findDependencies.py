#!/usr/bin/env python

import sys, re, os, json, gzip
from argparse import ArgumentParser
from glob import glob

parser = ArgumentParser()
parser.add_argument('-rel')
parser.add_argument('-arch', dest = 'scramarch', default = os.environ.get("SCRAM_ARCH"))
parser.add_argument('-scramroot', default = os.environ.get("SCRAMV1_ROOT"))
args = parser.parse_args()

rel = args.rel
scramarch = args.scramarch
scramroot = args.scramroot

if scramroot is None:
  scramroot = os.popen("sh -v scram arch 2>&1 |  grep 'SCRAMV1_ROOT=' | sed 's|;.*||;s|SCRAMV1_ROOT=||;s|\"||g' | sed -e \"s|'||g\"").read()

global name, dir
uses = {}
usedby = {}
directory = rel + "/tmp" # root dir for traversing

def doexec():
  global uses
  getnext = 0
  depname = ""
  with open(name, 'r') as file:
    for l in file:
      l = l.rstrip('\n')
      if re.search(r'^[^:]+ :\s*$', l): break
      l = re.sub(r'\s*\\$', r'', l)
      sp1 = l.split()
      if len(sp1) == 0: continue
      if len(sp1[0]) < 4: continue
      sp2 = sp1[0].split('/')
      tsp1 = ""
      foundsrc = 0
      for t in sp2:
        if foundsrc == 1: tsp1 += "%s/" % t
        if t == "src": foundsrc = 1
      tsp1 = tsp1[:-1]
      if tsp1 == "": continue
      if getnext == 1:
        depname = tsp1
        getnext = 0
      else:
        getnext = 0
        if re.search( r'^tmp\/', sp1[0]):
          if re.search( r'(\.o|\/a\/xr+\.cc):$', sp1[0]):
            getnext = 1
        else:
          if re.search( r'^src', sp1[0]):
            if depname not in uses.keys():
              uses[depname] = "%s " % tsp1
            else: 
              uses[depname] += "%s " % tsp1
            if tsp1 not in usedby.keys():
              usedby[tsp1] = "%s " % depname
            else: 
              usedby[tsp1] += "%s " % depname

def write2File(path, data, type_=None):
  with open(path, 'w') as file:
    if type_:
      if re.search(r'^bf', path.split("/")[-1]):
        if not data.has_key("type_"): data["type_"] = {}
      for x in sorted(data[type_].keys()):
        file.write("%s %s\n" % (x, " ".join(sorted(data[type_][x].keys()))))
    else:
      for key, value in sorted(data.items()):
        file.write("%s %s\n" % (key,value))

def createCache(match, cache, file):
  for x in import2CMSSWDir(match.group(1), cache):
    if not cache.has_key("usedby"): cache["usedby"] = {}
    if not cache.has_key("uses"): cache["uses"] = {}
    if not cache["usedby"].has_key(x): cache["usedby"][x] = {}
    if not cache["uses"].has_key(file): cache["uses"][file] = {}
    if not cache["usedby"][x].has_key(file): cache["usedby"][x][file] = {}
    if not cache["uses"][file].has_key(x): cache["uses"][file][x] = {}
    cache["usedby"][x][file] = 1
    cache["uses"][file][x] = 1

def pythonDeps(rel):
  cache = {}
  for root, dirs, files in os.walk("%s/src/" % rel):
    for filename in files:
      fpath = os.path.join(root, filename)
      if re.search(r'.py$', fpath):
        fname = fpath
        file = fname
        file = re.sub(r"^%s\/+src\/+" % rel, r'', file)
        if not re.search(r'\/python\/', fname):
          continue
        with open(fname, 'r') as f:
          for line in f.readlines():
            if 'import ' in line:
              line = line.rstrip('\n')
              if re.search(r'^\s*#', line):
                continue
              match_from_import = re.search(r'^\s*from\s+([^\s]+)\s+import\s+', line)
              match_import = re.search(r'^\s*import\s+([^\s]+)\s*', line)
              if match_from_import:
                createCache(match_from_import, cache, file)
              elif match_import:
                createCache(match_import, cache, file)
  for type_ in ("uses","usedby"):
    write2File("%s/etc/dependencies/py%s.out" % (rel, type_), cache, type_)

def import2CMSSWDir(str, cache):
  pyfiles = []
  if not cache.has_key("pymodule"): cache["pymodule"] = {}
  if not cache.has_key("noncmsmodule"): cache["noncmsmodule"] = {}
  for s in str.split(","):
    s = re.sub(r'\.', r'/', s)
    if s in cache["pymodule"]:
      pyfiles.append(cache["pymodule"][s])
    elif s not in cache["noncmsmodule"]:
      if os.path.exists("%s/python/%s.py" % (rel, s)):
        match = re.search( r'^([^\/]+\/+[^\/]+)\/+(.+)$', s)
        if match:
          cache["pymodule"][s] = "%s/python/%s.py" % (match.group(1), match.group(2))
          pyfiles.append("%s/python/%s.py" % (match.group(1), match.group(2)))
      else: cache["noncmsmodule"][s] = 1
  return pyfiles

def data2json(infile):
  jstr = ""
  rebs=re.compile(',\s+"BuildSystem::[a-zA-Z0-9]+"\s+\)')
  revar=re.compile("^\s*\$[a-zA-Z0-9]+\s*=")
  reundef=re.compile('\s*undef,')
  lines = [l.strip().replace(" bless(","").replace("'",'"').replace('=>',' : ')  for l in
  gzip.open(infile).readlines()]
  lines[0] = revar.sub("",lines[0])
  lines[-1] = lines[-1].replace(";","")
  for l in lines:
    l =  reundef.sub(' "",',rebs.sub("", l.rstrip()))
    jstr += l
  return json.loads(jstr)

def updateBFDeps(dir, pcache, cache):
  bf = cache["dirs"][dir]
  if not cache.has_key("uses"): cache["uses"] = {}
  if bf in cache["uses"]: return 0
  cache["uses"][bf] = {}
  for pack in pcache["BUILDTREE"][dir]["RAWDATA"]["DEPENDENCIES"].keys():
    if pack in cache["packs"]:
      xdata = cache["packs"][pack]
      updateBFDeps(xdata, pcache, cache)
      xdata = cache["dirs"][xdata]
      cache["uses"][bf][xdata] = 1
      if not cache.has_key("usedby"): cache["usedby"] = {}
      if not cache["usedby"].has_key(xdata): cache["usedby"][xdata] = {}
      cache["usedby"][xdata][bf] = 1
      for xdep in cache["uses"][xdata].keys():
        cache["uses"][bf][xdep] = 1
        cache["usedby"][xdep][bf] = 1

def buildFileDeps(rel, arch, scramroot):
  pcache = data2json("%s/.SCRAM/%s/ProjectCache.db.gz" % (rel, arch))
  cache = {}
  for dir in sorted(pcache["BUILDTREE"].keys()):
    if pcache["BUILDTREE"][dir]["SUFFIX"] != "": continue
    if len(pcache["BUILDTREE"][dir]["METABF"]) == 0: continue
    bf = pcache["BUILDTREE"][dir]["METABF"][0]
    bf = re.sub(r'src\/', r'',bf)
    if not cache.has_key("dirs"): cache["dirs"] = {}
    if not cache["dirs"].has_key(dir): cache["dirs"][dir] = {}
    cache["dirs"][dir] = bf
    pack = dir
    class_ = pcache["BUILDTREE"][dir]["CLASS"]
    if re.search( r'^(LIBRARY|CLASSLIB)$', class_):
      pack = pcache["BUILDTREE"][dir]["PARENT"]
      if not cache.has_key("packs"): cache["packs"] = {}
      if not cache["packs"].has_key(pack): cache["packs"][pack] = {}
    cache["packs"][pack] = dir
  for dir in cache["dirs"].keys():
    updateBFDeps(dir, pcache, cache)
  for type_ in ("uses","usedby"):
    write2File("%s/etc/dependencies/bf%s.out" % (rel, type_), cache, type_)

for root, dirs, files in os.walk(directory):
  for filename in files:
    name = os.path.join(root, filename)
    if re.search( r'^.*(\.dep|\/a\/xr+\.cc\.d)', name): doexec()

write2File(rel + "/etc/dependencies/uses.out", uses)
write2File(rel + "/etc/dependencies/usedby.out", usedby)
pythonDeps(rel)
buildFileDeps(rel, scramarch, scramroot)
sys.exit()
