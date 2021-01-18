from os.path import dirname, join
from gen_package import package_names

def packages(virtual_packages, *args):
  opts = args[0].options
  pkg_dir = dirname(__file__)
  for pkg in package_names:
    if pkg == "dqmgui":
      virtual_packages[pkg] = 'v=$(grep "^###  *RPM " %s/root.spec|sed "s|.* root *||");sed -e "s|@ROOT_VERSION@|$v|" %s/dqmgui.tmpl' % (opts.cmsdist, opts.cmsdist)
    else:
      virtual_packages[pkg] = "%s/gen_package.py %s %s %s" % (pkg_dir, pkg, opts.cmsdist, join(opts.workDir, opts.tempDirPrefix))
  return
