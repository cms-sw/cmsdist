def packages(virtual_packages):
  from os.path import dirname,join, exists
  pkg_dir = dirname(__file__)
  for ptype in ['cmssw-xmldata-build', 'data-build-github', 'data-build-github-new', 'data-cmssw-package-build', 'data-package-build']:
    req = join(pkg_dir,ptype+'.txt')
    if not exists(req): continue
    for line in [ l.replace(' ','') for l in open(req).readlines()]:
      if line.startswith('#'):continue
      if not '=' in line: continue
      (pkg, ver) = line.strip().split('=',1)
      virtual_packages['data-'+pkg]='%s/package.sh "data-%s" "%s" "%s"' % (pkg_dir, pkg, ver, ptype)
  return
