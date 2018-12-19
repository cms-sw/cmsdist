def packages(virtual_packages):
  from os.path import dirname,join, exists
  pkg_dir = dirname(__file__)
  req = join(pkg_dir,'requirements.txt')
  if not exists(req): return
  for line in [ l.replace(' ','') for l in open(req).readlines()]:
    if line.startswith('#'):continue
    if not '==' in line: continue
    (pkg, ver) = line.strip().split('==',1)
    virtual_packages['py2-'+pkg]='%s/package.sh "py2-%s" "%s"' % (pkg_dir, pkg, ver)
  return
