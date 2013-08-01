### RPM external sherpampi 2.0.beta2
Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz
Requires: autotools hepmc lhapdf blackhat openmpi
#BuildRequires: autotools
Patch0: sherpa-2.0.beta2-lhapdf
Patch1: sherpa-1.4.2-fix-gcc47-cxx11
Patch2: sherpa-1.4.0-add-support-osx108
Patch3: sherpa-2.0.beta2-mpi

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%if "%{?cms_mpicxx:set}" != "set"
%define cms_mpicxx ${OPENMPI_ROOT}/bin/mpic++
%endif

%prep
%setup -q -n SHERPA-MC-%{realversion}
%patch0 -p0

# Apply C++11 / gcc 4.7.x fixes only if using a 47x architecture.
# See http://gcc.gnu.org/gcc-4.7/porting_to.html
case %cmsplatf in
  *gcc4[6789]*)
%patch1 -p1
  ;;
esac

if [[ %cmsplatf == osx108_* ]]; then
%patch2 -p1
fi
%patch3 -p1

autoreconf -i --force


# Force architecture based on %%cmsplatf
case %cmsplatf in
  *_amd64_gcc*) ARCH_CMSPLATF="-m64" ;;
  *_ia32_gcc*) ARCH_CMSPLATF="-m32" ;;
esac

case %cmsplatf in
  osx*)
    perl -p -i -e 's|-rdynamic||g' \
      configure \
      AddOns/Analysis/Scripts/Makefile.in
  ;;
esac

%build
# OpenMPI build

./configure --prefix=%i --enable-analysis --disable-silent-rules --enable-mpi \
            --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT --enable-blackhat=$BLACKHAT_ROOT \
            CXX="%cms_cxx" MPICXX="%cms_mpicxx" CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF %cms_cxxflags -I$BLACKHAT_ROOT/include/ -I$OPENMPI_ROOT/include/" LDFLAGS="-ldl -L$BLACKHAT_ROOT/lib/ -L$OPENMPI_ROOT/lib/ -lmpi -lmpi_cxx" 

# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
find . -name Makefile -exec perl -p -i -e 's|/usr/lib64/libm.a||g;s|/usr/lib64/libc.a||g;' {} \;

make %{makeprocesses} 

%install

make install
rm -f %{i}/lib/SHERPA-MC/*.la

%post
%{relocateRpmPkg}/bin/Sherpa-config
%{relocateRpmPkg}/share/SHERPA-MC/sherpa-completion
%{relocateRpmPkg}/include/SHERPA-MC/ATOOLS/Org/CXXFLAGS.H
