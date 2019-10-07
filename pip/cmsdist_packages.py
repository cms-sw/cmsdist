def packages(virtual_packages):
  from  platform import machine
  from re import match
  from os.path import dirname,join, exists
  pkg_dir = dirname(__file__)
  req = join(pkg_dir,'requirements.txt')
  if not exists(req): return
  sys_platform = machine()
  for line in [ l.replace(' ','') for l in open(req).readlines()]:
    if line.startswith('#'):continue
    if not '==' in line: continue
    items = line.strip().split(';')
    (pkg, ver) = items[0].strip().split('==',1)
    py = "py2"
    if len(items)>1:
      matched=True
      for item in items[1:]:
        m = match("^\s*(python_version|sys_platform)\s*(<|<=|>|>=|==|!=)\s*'([^']+)'\s*$", item.strip().replace(" ",""))
        if m:
          if m.group(1)=='python_version':
            if   m.group(2) in ['>', '>=', '=='] and int(float(m.group(3)))>=3: py='py3'
            elif m.group(2) in ['<']             and int(float(m.group(3)))>=3: py='py2'
            else: matched=False
          elif m.group(1)=='sys_platform':
            if   m.group(2)=='==' and sys_platform!=m.group(3): matched=False
            elif m.group(2)=='!=' and sys_platform==m.group(3): matched=False
      if matched:
        virtual_packages[py+'-'+pkg]='%s/package.sh "%s-%s" "%s" "%s"' % (pkg_dir, py, pkg, ver, py)
    else:
      virtual_packages[py+'-'+pkg]='%s/package.sh "%s-%s" "%s"' % (pkg_dir, py, pkg, ver)
  return
