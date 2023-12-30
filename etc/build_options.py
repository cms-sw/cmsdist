def get_build_options(options, *args):
  opts = {}
  boolean_opts = ["vecgeom", "lto", "warnings"]
  for opt in boolean_opts:
    opts[opt] = ["enable_%s=1" % opt]
    opts["no-"+opt] = ["enable_%s=0" % opt]
  for std in ["17", "20"]:
    opts["cpp"+std] = ["cms_cxx_standard=%s" % std]
  return opts
