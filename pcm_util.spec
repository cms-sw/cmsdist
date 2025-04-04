### RPM external pcm_util 3.0
%define pcm_packages tbb py3-pybind11 clhep tinyxml2 hepmc fmt xerces-c dd4hep hls %{!?without_cuda:cuda}
Source98: scram/tools/dd4hep/dd4hep_flags
Source99: scram/tools/tbb/tbb_flags
Requires: root python3 %{pcm_packages}

%prep


%build
source %{_sourcedir}/tbb_flags
source %{_sourcedir}/dd4hep_flags
rm -rf build; mkdir build; cd build

touch empty.h
echo "module Dummy{}" > dummy.modulemap

HEPMC_MOD_NAME="HepMC"
PY3_PYBIND11_MOD_NAME="pybind11"
XERCES_C_MOD_NAME="xercesc"

CLHEP_MM_NAME="clhep.modulemap"
HEPMC_MM_NAME="hepmc.modulemap"

TBB_FLAGS="${CMS_TBB_CPPFLAGS}"
PYBIND11_FLAGS="-I$PYTHON3_ROOT/include/python%{cms_python3_major_minor_version}/"
DD4HEP_FLAGS="${CMS_DD4hEP_CPPFLAGS}"

function check_var() {
   var=$1
   default=$2
   if [ -z ${!var+x} ] ; then
      declare -g "${var}"=${default}
   fi
}

for pcm in %{pcm_packages} ; do
    uc_pcm="$(echo ${pcm} | tr [a-z-] [A-Z_])"
    pcm_name="${uc_pcm}_MOD_NAME"
    mod="${pcm}"
    [ -z ${!pcm_name+x} ] || mod="${!pcm_name}"
    uc_mod="$(echo ${mod} | tr [a-z-] [A-Z_])"
    rootvar="${uc_pcm}_ROOT"
    mm_name="${uc_mod}_MM_NAME"
    mm_flags="${uc_mod}_FLAGS"
    mm_incdir="${uc_mod}_INCDIR"
    mm_moddir="${uc_mod}_MODDIR"
    check_var $mm_name "module.modulemap"
    check_var $mm_flags ""
    check_var $mm_incdir "include"
    check_var $mm_moddir "include"
    mm_file=${!rootvar}/${!mm_moddir}/${!mm_name}
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 ${!mm_flags} -moduleMapFile=${mm_file} -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m $mod -mByproduct $mod  -I${!rootvar}/${!mm_incdir} empty.h
    mkdir ${pcm}
    ls *.pcm
    mv ${mod}.pcm ${pcm}/
    [ $(ls *.pcm 2>/dev/null | grep -v Dummy.pcm | wc -l) -gt 0 ] && exit 1
    rm -f Dummy.pcm
done

%install
mkdir %{i}/lib %{i}/modules
for pcm in %{pcm_packages} ; do
  mv build/${pcm} %{i}/modules/${pcm}
  for f in $(ls %{i}/modules/${pcm}) ; do
    ln -sf ../modules/${pcm}/$f %{i}/lib/$f
  done
done
