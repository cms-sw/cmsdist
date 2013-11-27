### RPM external sherpa 1.4.2
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
Requires: icc icc-provides
%endif

Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz
Requires: hepmc lhapdf zlib
BuildRequires: autotools
Patch0: sherpa-1.4.0-lhapdf
Patch1: sherpa-1.4.2-fix-gcc47-cxx11
Patch2: sherpa-1.4.0-add-support-osx108

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
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

autoreconf -i --force

# Force architecture based on %%cmsplatf
case %cmsplatf in
  *_amd64_gcc*|*_mic_*) ARCH_CMSPLATF="-m64" ;;
  *_ia32_gcc*) ARCH_CMSPLATF="-m32" ;;
esac

case %cmsplatf in
  osx*)
    perl -p -i -e 's|-rdynamic||g' \
      configure \
      AddOns/Analysis/Scripts/Makefile.in
  ;;
esac

./configure --prefix=%i --enable-analysis --disable-silent-rules \
            --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT \
            --enable-multithread LDFLAGS="-ldl" \
%if "%mic" == "true"
           --host=x86_64-k1om-linux FC="ifort -mmic" CC="icc -mmic" CXX="icpc -mmic " CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF %cms_cxxflags -I${ZLIB_ROOT}/include" LDFLAGS="-L${ZLIB_ROOT}/lib"
%else
           CXX="%cms_cxx" CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF %cms_cxxflags"
%endif
%build
# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
find . -name Makefile -exec perl -p -i -e 's|/usr/lib64/libm.a||g;s|/usr/lib64/libc.a||g;' {} \;

make %{makeprocesses} 

%install
make install

