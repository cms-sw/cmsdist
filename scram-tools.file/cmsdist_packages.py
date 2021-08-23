def packages(virtual_packages, *args):
  from os.path import dirname, join, basename
  from glob import glob
  tools_dir = join(dirname(__file__), "tools")
  for tool in [basename(t) for t in glob(tools_dir+"/*")]:
    spec = "%s-toolfile" % tool
    virtual_packages[spec] = 'echo -e "### RPM cms %s 1.0\nRequires: %s\n## INCLUDE scram-tools.file/toolfile"' % (spec, tool)
  return
