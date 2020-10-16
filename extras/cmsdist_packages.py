from os.path import dirname, join
from gen_package import package_names

def packages(virtual_packages, *args):
  opts = args[0].options
  pkg_dir = dirname(__file__)
  for pkg in package_names:
    virtual_packages[pkg] = "%s/gen_package.py %s %s %s" % (pkg_dir, pkg, opts.cmsdist, join(opts.workDir, opts.tempDirPrefix))
  return
