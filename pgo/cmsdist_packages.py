from os.path import dirname, join
pgo_packages = ["geant4", "vecgeom", "OpenBLAS", "g4hepem", "dd4hep", "cmssw", "cmssw-patch", "cmssw-tool-conf"]

def packages(virtual_packages, *args):
  opts = args[0].options
  try:
    if (not opts.PGOGenerate) and (not opts.PGOUse): return
  except:
    return

  def process_pkg(vpkg, pkg):
    xindex = 0
    pkgspec = "%s.spec" % pkg
    spec = []
    if vpkg in virtual_packages:
      for line in virtual_packages[vpkg]:
        if not pkgspec in line:
          xindex += 1
          spec.append(line)
        else: break
    spec.append('%define pgo_path_prefix {0}'.format('@LOCALTOP@' if pkg in ["cmssw-tool-conf"] else '%{_builddir}'))
    spec.append('%define pgo_package_name {0}'.format('cmssw' if pkg in ["cmssw-tool-conf"] else vpkg))
    spec.append('%define {0} 1'.format('pgo_generate' if opts.PGOGenerate else 'pgo_use'))
    spec.append('## INCLUDE pgo/compilation_flags_pgo')
    if not vpkg in virtual_packages:
      spec.append("cmd: cat {0}/{1}".format(opts.cmsdist, pkgspec))
    else:
      spec +=  virtual_packages[vpkg][xindex:]
    virtual_packages[vpkg] = spec[:]
    return

  for pkg in pgo_packages:
    process_pkg(pkg, pkg)
    for v in opts.vectorization:
      vpkg = "%s_%s" % (pkg,v)
      if vpkg in virtual_packages:
          pgo_packages.append(vpkg)
          process_pkg(vpkg, pkg)
  return
