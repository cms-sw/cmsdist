def packages(virtual_packages):
  from re import match
  from os.path import dirname,join, exists
  import os, sys, platform
  pkg_dir = dirname(__file__)
  req = join(pkg_dir,'requirements.txt')
  if not exists(req): return
  extra_match = {}
  extra_match['platform_machine'] = platform.machine()
  extra_match['sys_platform'] = sys.platform
  extra_match['os_name'] = os.name
  for line in [ l.strip().replace(' ','') for l in open(req).readlines()]:
    if line.startswith('#'):continue
    if not '==' in line: continue
    items = line.strip().split(';')
    (pkg, ver) = items[0].strip().split('==',1)
    py = ""
    matched=True
    for item in items[1:]:
      m = match("^python_version(<|>|>=|==)'([^']+)'$", item)
      if m:
        if   m.group(1) in ['>', '>=', '=='] and int(float(m.group(2)))>=3: py='py3'
        elif m.group(1) in ['<']             and int(float(m.group(2)))>=3: py='py2'
        else: matched=False
        continue
      m = match("^("+"|".join(list(extra_match.keys()))+")(==|!=)'([^']+)'$", item)
      if m:
        if m.group(2)=='==' and extra_match[m.group(1)]!=m.group(3): matched=False
        if m.group(2)=='!=' and extra_match[m.group(1)]==m.group(3): matched=False
    if matched:
      if py:
        virtual_packages[py+'-'+pkg]='%s/package.sh "%s-%s" "%s" "%s"' % (pkg_dir, py, pkg, ver, py)
      else:
        virtual_packages['py2-'+pkg]='%s/package.sh "py2-%s" "%s"' % (pkg_dir, pkg, ver)
  return

