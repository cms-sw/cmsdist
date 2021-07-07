### RPM cms cmssw-tool-conf 46.0
# With cmsBuild, change the above version only when a new tool is added

## NOCOMPILER
## INSTALL_DEPENDENCIES cmsLHEtoEOSManager gcc-fixincludes cmssw-osenv cms-git-tools
## UPLOAD_DEPENDENCIES dqmgui

BuildRequires: scram-tools
Requires: gcc
Requires: herwig
Requires: libpng
Requires: OpenBLAS
Requires: root
Requires: tbb
Requires: zlib
Requires: zstd
Requires: intel-vtune
Requires: das_client
Requires: llvm
Requires: boost

%define skipreqtools jcompiler icc-cxxcompiler icc-ccompiler icc-f77compiler rivet2 opencl opencl-cpp nvidia-drivers intel-vtune jemalloc-debug

# the vectorization flags/macroses will be available

## IMPORT scramv1-tool-conf
