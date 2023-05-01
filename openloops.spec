## INCLUDE openloops-common
### RPM external openloops %{openloop_version}

BuildRequires: openloops-process

%define keep_archives true
%define runpath_opts -m proclib

%prep
%setup -n %{n}-%{realversion}

#process_src should be available via $OPENLOOPS_PROCESS_ROOT
echo 'import sys;print(sys.argv)' > download_dummy.py
sed -i -e 's|^ *process_download_script *=.*|process_download_script = download_dummy.py|' pyol/config/default.cfg

#Remove conditional processes
%ifarch aarch64
%define drop_process pplljj_ew
sed -i -e 's|^ *cmodel *=.*|cmodel = small|' pyol/config/default.cfg
%else
%define drop_process %{nil}
%endif

#Fix for GCC 10
gcc10_extra_flag=""
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then export gcc10_extra_flag=-fallow-invalid-boz ; fi

cat <<EOF > openloops.cfg
[OpenLoops]
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0 $gcc10_extra_flag
generic_optimisation = -O2
born_optimisation = -O2
loop_optimisation = -O0
link_optimisation = -O2
EOF

%build
export SCONSFLAGS="-j %{compiling_processes}"
cp %{_sourcedir}/openloops-user.coll openloops-user.coll
./openloops update --processes generator=0

#create process_src and delete any un-needed processes
rm -rf process_src
tar -xzf $OPENLOOPS_PROCESS_ROOT/process_src.tgz
for xproc in %{drop_process} ; do
  sed -i -e "/^${xproc}$/d" openloops-user.coll
  sed -i -e "/^${xproc} .*/d" process_src/downloaded.dat
  rm -rf process_src/${xproc}
done

./openloops libinstall openloops-user.coll

%install
mkdir %i/{lib,proclib}
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
