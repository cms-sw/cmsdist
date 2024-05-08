#!/usr/bin/env python3
from platform import machine
from sys import exit, argv

MULTI_TARGET_PACKAGES = []
VALID_TARGETS = {}
if machine() == "x86_64":
  ############ IMPORTANT NOTE #############
  # For any newly added vecrtorized packages here,
  # please also add scram-tools.file/tools/package/vectorized.tmpl file
  # and vectorized_packages list in cmssw-vectorization.file file
  #########################################
  MULTI_TARGET_PACKAGES = [
    "zlib",
    "fastjet",
    "tensorflow-sources",
    "tensorflow",
    "tensorflow-xla-runtime",
    "OpenBLAS",
    "rivet",
    "gbl",
    "lwtnn",
    "opencv",
    "pytorch",
  ]
  VALID_TARGETS = {
    "nehalem":     "-march=nehalem",
    "sandybridge": "-march=sandybridge",
    "haswell":     "-march=haswell",
    "skylake-avx512":"-march=skylake-avx512",
  }
  for v in range(2,5):
    psABI = "x86-64-v%s" % v
    VALID_TARGETS[psABI] = "-march=" + psABI

def packages(virtual_packages, *args):
  opts = args[0].options
  if not opts.vectorization: return
  for pkg in MULTI_TARGET_PACKAGES:
    err = False
    for v in opts.vectorization:
      if v not in VALID_TARGETS:
        print("Vectorization instructions %s not supported. Please update %s to generate specs for this vectorized instructions set." % (v, __file__))
        err = True
      vpkg = "%s_%s" % (pkg, v)
      spec =     ["%define vectorized_package {0}".format(v)]
      spec.append("%define override_microarch {0}".format(VALID_TARGETS[v]))
      spec.append("cmd:sed -e 's|\(^###  *RPM  *[^\s]*\)  *{0} |\\1 {1} |;s|%{{n}}|{0}|g;' {2}/{0}.spec".format(pkg, vpkg, opts.cmsdist))
      virtual_packages[vpkg] = spec[:]
    if err:
      exit(1)
  return

if __name__ == '__main__':
  print (VALID_TARGETS[argv[1]])
