def packages(virtual_packages):
  from re import match
  from os.path import dirname,join, exists
  pkg_dir = dirname(__file__)
  req = join(pkg_dir,'requirements.txt')
  if not exists(req): return
  for line in [ l.replace(' ','') for l in open(req).readlines()]:
    if line.startswith('#'):continue
    if not '==' in line: continue
    items = line.strip().split(';',1)
    (pkg, ver) = items[0].strip().split('==',1)
    if len(items)==2:
      if match("^python_version>'3.0'$", items[1]):
        virtual_packages['py3-'+pkg]='%s/package.sh "py3-%s" "%s" "py3"' % (pkg_dir, pkg, ver)
      else:
        virtual_packages['py2-'+pkg]='%s/package.sh "py2-%s" "%s" "py3"' % (pkg_dir, pkg, ver)
    else:
      virtual_packages['py2-'+pkg]='%s/package.sh "py2-%s" "%s"' % (pkg_dir, pkg, ver)
  return
