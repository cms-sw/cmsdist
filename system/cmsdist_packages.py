def packages(virtual_packages, *args):
  from os.path import dirname, join, basename
  from glob import glob
  opts = None
  if hasattr(args[0], "useSystemTools"):
    opts = args[0]
  else:
    opts = args[0].options
  overrideSysTools = list(opts.useSystemTools) + list(opts.overrideSystemTools)
  if not overrideSysTools:
    return
  for spec in glob(join(dirname(__file__), "*.spec")):
    pkg = basename(spec)[:-5]
    if pkg in overrideSysTools:
      virtual_packages[pkg] = "cat %s" % spec
  return
