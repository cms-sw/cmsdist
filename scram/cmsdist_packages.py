SCRAM_PROJECT = ["coral", "cmssw", "cmssw-patch", "fwlite"]

def packages(virtual_packages, *args):
  from os.path import dirname, join, basename, exists
  from glob import glob
  tools_dir = join(dirname(__file__), "tools")
  for tool in [basename(t) for t in glob(tools_dir+"/*")]:
    pkg = "%s-toolfile-src" % tool
    spec = ["### RPM cms %s 1.0" % pkg]
    spec.append("BuildRequires: %s" % tool)
    spec.append("## INCLUDE scram/toolfile-src")
    virtual_packages[pkg] = spec[:]
    pkg = "%s-toolfile" % tool
    spec = ["### RPM cms %s 1.0" % pkg]
    spec.append("BuildRequires: %s-src" % pkg)
    spec.append("Requires: %s" % tool)
    spec.append("## INCLUDE scram/toolfile")
    virtual_packages[pkg] = spec[:]

  for tool in SCRAM_PROJECT:
    pkg = "%s-tool-conf" % tool
    spec = ["### RPM cms %s 100.0" % pkg]
    spec.append("Requires: %s-tools" % tool)
    if exists(join(args[0].options.cmsdist, pkg+".file")):
      spec.append("## INCLUDE %s" % pkg)
    spec.append("## INCLUDE scram/tool-conf")
    virtual_packages[pkg] = spec[:]

  return
