from os.path import dirname, join
pgo_packages = ["geant4", "vecgeom", "g4hepem", "dd4hep", "cmssw", "cmssw-patch", "cmssw-tool-conf"]

def packages(virtual_packages, *args):
  opts = args[0].options
  try:
    if (not opts.PGOGenerate) and (not opts.PGOUse): return
  except:
    return
  for pkg in pgo_packages:
    spec  = "  echo '%%define pgo_path_prefix  %s'" % ('@LOCALTOP@' if pkg in ["cmssw-tool-conf"] else '%{_builddir}')
    spec += "; echo '%%define pgo_package_name %s'" % ('cmssw' if pkg in ["cmssw-tool-conf"] else pkg)
    spec += "; echo '%%define %s 1'" % ('pgo_generate' if opts.PGOGenerate else 'pgo_use')
    spec += "; echo '## INCLUDE pgo/compilation_flags_pgo'"
    spec += "; cat %s/%s.spec" % (opts.cmsdist, pkg)
    virtual_packages[pkg] = spec
  return
