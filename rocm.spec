### RPM external rocm 5.4.2
## NOCOMPILER
Source: none
Provides: libamd_comgr.so.2()(64bit)
Provides: libhsa-runtime64.so.1()(64bit)
Provides: librocm-core.so.1()(64bit)
Provides: librocm_smi64.so.5()(64bit)

%prep

%build

%install
OSDIR=/cvmfs/patatrack.cern.ch/externals/%{_arch}/rhel%{rhel}
if ! [ -d $OSDIR ]; then
  OSDIR=/cvmfs/patatrack.cern.ch/externals/%{_arch}/unknown
fi
BASEDIR=${OSDIR}/amd/%{n}-%{realversion}

# symlink individual files from ${BASEDIR}/bin/
mkdir %{i}/bin
test -d ${BASEDIR}/bin
test -e ${BASEDIR}/bin/hipcc
ln -s ${BASEDIR}/bin/* %{i}/bin/
# remove the OpenCL extra files
rm -f %{i}/bin/clang-ocl
# remove the OpenMP extra files
rm -f %{i}/bin/{aompcc,gputable.txt,mygpu,mymcpu}
# remove the MIGraphX tools
rm -f %{i}/bin/migraphx-driver

# ROCm/HIP core tools
DIRECTORIES="amdgcn hip hipcub hsa hsa-amd-aqlprofile include lib libexec llvm rocthrust share"

# rocm-smi
DIRECTORIES+=" oam rocm_smi"

# hipBLAS / rocBLAS
DIRECTORIES+=" hipblas rocblas"

# hipSOLVER / rocSOLVER
DIRECTORIES+=" hipsolver rocsolver"

# hipSPARSE / rocSPARSE
DIRECTORIES+=" hipsparse rocsparse"

# hipFFT / rocFFT
DIRECTORIES+=" hipfft rocfft"

# hipRAND / rocRAND
DIRECTORIES+=" hiprand rocrand"

# ROCm Parallel Primitives (rocPRIM)
DIRECTORIES+=" rocprim"

# ROCm Tracer Callback/Activity Library (rocTRACER) and profiler library (ROC-profiler)
DIRECTORIES+=" rocprofiler roctracer"

# Asynchronous Task and Memory Interface (ATMI)
#DIRECTORIES+=" atmi"

# OpenCL support
#DIRECTORIES+=" opencl tests"

# ROCm Communication Collectives Library (RCCL)
#DIRECTORIES+=" rccl"

# iterative sparse solvers for ROCm platform (rocALUTION)
#DIRECTORIES+=" rocalution"

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
