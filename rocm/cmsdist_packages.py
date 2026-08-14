def packages(virtual_packages, *args):
  from glob import glob
  from os.path import dirname, basename
  for spec in glob("%s/*.spec" % dirname(__file__)):
    pkg = basename(spec)[:-5]
    virtual_packages[pkg] = 'cat %s' % spec
  return
