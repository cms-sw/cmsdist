### RPM external sherpa 2.2.2
%define tag 337787e09a2cc4bb6a68fd165f3f87f80631e0a0
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: hepmc lhapdf blackhat sqlite fastjet openssl openmpi
BuildRequires: mcfm

%if "%(case %cmsplatf in (slc*) echo true ;; (*) echo false ;; esac)" == "true"
Requires: openloops
%endif

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
            ${OPENLOOPS_ROOT+--enable-openloops=$OPENLOOPS_ROOT}\
            --enable-mpi=$OPENMPI_ROOT \
            --with-sqlite3=$SQLITE_ROOT \
            CXX="g++" \
            MPICXX="${OPENMPI_ROOT}/bin/mpic++" \
            CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF -O2 -std=c++0x -I$LHAPDF_ROOT/include -I$BLACKHAT_ROOT/include -I$OPENSSL_ROOT/include -I$OPENMPI_ROOT/include/" \
            LDFLAGS="-ldl -L$BLACKHAT_ROOT/lib/blackhat -L$QD_ROOT/lib -L$OPENSSL_ROOT/lib -L$OPENMPI_ROOT/lib/"

make %{makeprocesses}

%install
make install
