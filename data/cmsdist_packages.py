def packages(virtual_packages):
  from os.path import dirname,join, exists
  from sys import exit
  default_build_file = 'cmsswdata-github'
  pkg_dir = dirname(__file__)
  req = join(pkg_dir,'cmsswdata.txt')
  ptype=default_build_file
  for line in [ l.strip().replace(' ','') for l in open(req).readlines()]:
    if line.startswith('#') or line=='':continue
    if line[0]=='[' and line[-1]==']':
      ptype=line[1:-1]
      if ptype=='default': ptype=default_build_file
      continue
    if not '=' in line: continue
    (pkg, ver) = line.strip().split('=',1)
    data_pkg = 'data-'+pkg
    if data_pkg in virtual_packages:
      print ("ERROR: Duplicate data package definitions found in %s for package %s" % (req, pkg))
      exit(1)
    virtual_packages[data_pkg]='%s/package.sh "%s" "%s" "%s"' % (pkg_dir, data_pkg, ver, ptype)
  return
