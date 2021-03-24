#!/usr/bin/env python
from platform import machine
from sys import exit, argv

DEFAULT_TARGET_FLAG="-msse3"
MULTI_TARGET_PACKAGES = []
VALID_TARGETS = {}
if machine() == "x86_64":
  MULTI_TARGET_PACKAGES = [
    "zlib",
    "fastjet",
    "mkfit",
    "vecgeom",
    "tensorflow-sources",
    "tensorflow",
    "OpenBLAS",
  ]
  VALID_TARGETS = {
    "nehalem":     "-march=nehalem",
    "sandybridge": "-march=sandybridge",
    "haswell":     "-march=haswell",
    "skylake-avx512":"-march=skylake-avx512",
  }

def fix_tensorflow_sources(vec, value):
  return [(DEFAULT_TARGET_FLAG,"%s %s" % (value, "--distinct_host_configuration=true"))]

def fix_vecgeom(vec, value):
  return [(DEFAULT_TARGET_FLAG.replace("-m", ""), value.replace("-m", ""))]

def fix_OpenBLAS(vec, value):
  if vec=="skylake-avx512": vec="SKYLAKEX"
  return [("TARGET=CORE2", "TARGET=%s" % vec.upper())]

def packages(virtual_packages, *args):
  opts = args[0].options
  if not opts.vectorization: return
  for pkg in MULTI_TARGET_PACKAGES:
    err = False
    for v in opts.vectorization:
      if v not in  VALID_TARGETS:
        print("Vectorization instructions %s not supported. Please update %s to generate specs for this vectorized instructions set." % (v, __file__))
        err = True
      vpkg = "%s_%s" % (pkg, v)
      rdata = [(DEFAULT_TARGET_FLAG, VALID_TARGETS[v])]
      try:
        ndata = eval('fix_%s' % pkg.replace("-","_").replace(".","_"))(v, rdata[0][1])
        if ndata is not None: rdata = ndata
      except:
        pass
      xregexp = ""
      for item in rdata:
        xregexp = "s|%s|%s|g;" % (item[0], item[1])
      spec = "echo -e '%%define vectorized_package %s\n%%define vectorized_flags  %s'; sed -e '%ss|\(^###  *RPM  *[^\s]*\)  *%s |\\1 %s |;s|%%{n}|%s|g;' %s/%s.spec"
      virtual_packages[vpkg] = spec % (v, rdata[0][1], xregexp, pkg, vpkg, pkg, opts.cmsdist, pkg)
    if err:
      exit(1)
  return

if __name__ == '__main__':
  if len(argv)==2:
    if argv[1] in VALID_TARGETS:
      print (VALID_TARGETS[argv[1]])
  else:
    print (DEFAULT_TARGET_FLAG)
