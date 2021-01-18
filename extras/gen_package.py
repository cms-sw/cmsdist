#!/usr/bin/env python
package_names = {
  "cmsLHEtoEOSManager" : "https://api.github.com/repos/cms-sw/cmssw/commits?path=GeneratorInterface/LHEInterface/scripts/cmsLHEtoEOSManager.py&page=0&per_page=1",
  "dqmgui": None,
}

def main():
  from os.path import dirname, join, exists
  import os, sys, platform
  from json import loads
  from sys import version_info, argv
  if version_info[0] == 2:
    from urllib2 import urlopen
    from md5 import new as md5adder
  else:
    from urllib.request import urlopen
    from hashlib import md5 as md5adder

  pkg = argv[1]
  cmsdist = argv[2]
  tmpdir = argv[3]

  tmpl = join(cmsdist,  pkg+".tmpl")
  md5str = ""
  with open(tmpl) as ref:
    m = md5adder(ref.read())
    md5str = m.hexdigest()

  sfile = join (tmpdir, pkg+"."+md5str)
  if not exists(sfile):
    data = loads(urlopen(package_names[pkg]).read())
    commit = data[0]["sha"]
    version = data[0]["commit"]["author"]["date"][0:10].replace("-","")
    os.system("sed -e 's|@COMMIT@|%s|;s|@VERSION@|%s|' %s > %s" % (commit, version, tmpl, sfile))
  os.system("cat %s" % sfile)

if __name__ == '__main__':
    main()
