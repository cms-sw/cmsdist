### RPM external rocm 5.4.2
## NOCOMPILER
Source: none
Provides: libamd_comgr.so.2()(64bit)
Provides: libhsa-runtime64.so.1()(64bit)
Provides: librocm-core.so.1()(64bit)
Provides: librocm_smi64.so.5()(64bit)

# This rpm packages only symlinks to an installation that is already on CVMFS.
# Configure pkgtools to keep the static libraries, to avoid actually trying to
# delete them from CVMFS.
%define keep_archives true

%prep

%build

%install
OSDIR=/cvmfs/patatrack.cern.ch/externals/%{_arch}/rhel%{rhel}
if ! [ -d $OSDIR ]; then
  OSDIR=/cvmfs/patatrack.cern.ch/externals/%{_arch}/unknown
fi
BASEDIR=${OSDIR}/amd/%{n}-%{realversion}

# Symlink individual files from ${BASEDIR}/bin/
mkdir %{i}/bin
test -d ${BASEDIR}/bin
test -e ${BASEDIR}/bin/hipcc
ln -s ${BASEDIR}/bin/* %{i}/bin/
# Remove the OpenCL extra files
rm -f %{i}/bin/{clang-ocl,clinfo}
# Remove the OpenMP extra files
rm -f %{i}/bin/{aompcc,mygpu,mymcpu}
# Remove the Fortran files
rm -f %{i}/bin/hipfc
# Remove the MI tools
rm -f %{i}/bin/{MIOpenDriver,migraphx-driver,runvx}
# Remove the datacenter tools and validation suite binaries
rm -f %{i}/bin/{rdcd,rdci,rvs}
# Remove some of the prebuilt samples
rm -f %{i}/bin/{sgemmv,simple_dlrm,simple_gemm}

# ROCm/HIP core tools
DIRECTORIES="amdgcn hip hsa hsa-amd-aqlprofile include lib libexec llvm share"

# rocm-smi
DIRECTORIES+=" oam rocm_smi"

# ROCm Tracer Callback/Activity Library (rocTRACER) and profiler library (ROC-profiler)
DIRECTORIES+=" rocprofiler roctracer"

# Asynchronous Task and Memory Interface (ATMI)
#DIRECTORIES+=" atmi"

# OpenCL support
#DIRECTORIES+=" opencl tests"

# ROCm Communication Collectives Library (RCCL)
#DIRECTORIES+=" rccl"

# Machine Intelligence Libraries
#DIRECTORIES+=" miopen miopengemm"

# HIP Fortran interface (hipfort)
#DIRECTORIES+=" hipfort"

# ROCm Data Center Tool (RDC)
#DIRECTORIES+=" rdc"

# ROCm Validation Suite (RVS)
#DIRECTORIES+=" rvs"

# symlink the other directories from ${BASEDIR}/
for D in ${DIRECTORIES}; do
  ln -s ${BASEDIR}/${D} %{i}/
  test -L %{i}/${D}
done
