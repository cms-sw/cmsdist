### RPM external sherpa 2.2.6
%define tag ea0b6f6f50f77d2f7479ba81d0715e23b69eabee
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: hepmc lhapdf blackhat sqlite fastjet openssl scons python openmpi
BuildRequires: mcfm swig

%define islinux %(case $(uname -s) in (Linux) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

%if %islinux
%if %isamd64
Requires: openloops
%endif # isamd64
%endif # islinux

%prep
%setup -q -n %{n}-%{realversion}

autoreconf -i --force

# Force architecture based on %%cmsplatf
case %cmsplatf in
  *_amd64_gcc*) ARCH_CMSPLATF="-m64" ;;
esac

case %cmsplatf in
  osx*)
    perl -p -i -e 's|-rdynamic||g' \
      configure \
      AddOns/Analysis/Scripts/Makefile.in
  ;;
esac

%build
./configure --prefix=%i --enable-analysis --disable-silent-rules \
            --enable-fastjet=$FASTJET_ROOT \
            --enable-mcfm=$MCFM_ROOT \
            --enable-hepmc2=$HEPMC_ROOT \
            --enable-lhapdf=$LHAPDF_ROOT \
            --enable-blackhat=$BLACKHAT_ROOT \
            --enable-pyext \
            --enable-ufo \
            ${OPENLOOPS_ROOT+--enable-openloops=$OPENLOOPS_ROOT} \
            --enable-mpi \
            --with-sqlite3=$SQLITE_ROOT \
            --disable-automake.info \
            CC="mpicc" \
            CXX="mpicxx" \
            MPICXX="mpicxx" \
            FC="mpifort" \
            CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF -O2 -std=c++0x -I$LHAPDF_ROOT/include -I$BLACKHAT_ROOT/include -I$OPENSSL_ROOT/include" \
            LDFLAGS="-ldl -L$BLACKHAT_ROOT/lib/blackhat -L$QD_ROOT/lib -L$OPENSSL_ROOT/lib"

make %{makeprocesses}

%install
make install
# circumvent search for makeinfo, used to generate docs. other way of doing the same - patch the makefile as sugested here https://sourceware.org/bugzilla/show_bug.cgi?id=18113
ln -s /usr/bin/true makeinfo
export PATH=${PWD}:${PATH}
find %{i}/lib -name '*.la' -delete
sed -i -e 's|^#!/.*|#!/usr/bin/env python|' %{i}/bin/Sherpa-generate-model

%post
%{relocateConfig}lib/python2.7/site-packages/ufo_interface/sconstruct_template
%{relocateConfig}bin/make2scons
%{relocateConfig}share/SHERPA-MC/makelibs
%{relocateConfig}bin/Sherpa-config
%{relocateConfig}bin/Sherpa-generate-model
%{relocateConfig}include/SHERPA-MC/ATOOLS/Org/CXXFLAGS.H
