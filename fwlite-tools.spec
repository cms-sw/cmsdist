### RPM cms fwlite-tools 1.0
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $FWLITE_TOOL_CONF_ROOT

%{!?without_rocm:Requires: rocm}
%{!?without_cuda:Requires: cuda cuda-compatible-runtime}

Requires: alpaka
Requires: eigen
Requires: fmt
Requires: tbb
Requires: boost
Requires: clhep
Requires: fakesystem
Requires: fwlitedata
Requires: hepmc
Requires: hepmc3
Requires: hls
Requires: python3
Requires: root
Requires: sigcpp
Requires: libuuid
Requires: xerces-c
Requires: zlib
Requires: vdt
Requires: tinyxml2
Requires: md5
Requires: py3-pybind11
Requires: fwlite_python_tools
Requires: utm
Requires: llvm

## INCLUDE cmssw-drop-tools
## INCLUDE scram/tool-conf-src
