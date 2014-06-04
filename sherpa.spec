### RPM external sherpa 2.1.0
Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz
Requires: hepmc lhapdf blackhat sqlite fastjet openssl
Patch0: sherpa-2.1.0-lhapdf
Patch1: sherpa-2.1.0-disable-examples-manual

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n SHERPA-MC-%{realversion}
%patch0 -p1
%patch1 -p1

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

./configure --prefix=%i --enable-analysis --disable-silent-rules --enable-fastjet=$FASTJET_ROOT \
            --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT --enable-blackhat=$BLACKHAT_ROOT --with-sqlite3=$SQLITE_ROOT \
            CXX="%cms_cxx" \
            CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF %cms_cxxflags -I$LHAPDF_ROOT/include -I$BLACKHAT_ROOT/include -I$OPENSSL_ROOT/include" \
            LDFLAGS="-ldl -L$BLACKHAT_ROOT/lib/blackhat -L$QD_ROOT/lib -L$OPENSSL_ROOT/lib"
%build
# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
find . -name Makefile -exec perl -p -i -e 's|/usr/lib64/libm.a||g;s|/usr/lib64/libc.a||g;' {} \;

make %{makeprocesses}

%install
make install
