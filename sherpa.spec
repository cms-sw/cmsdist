### RPM external sherpa 2.1.1
%define tag ddb788ce152c8626876466d471eb7593ffd7ed9b
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: hepmc lhapdf blackhat sqlite fastjet openssl

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
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
./configure --prefix=%i --enable-analysis --disable-silent-rules --enable-fastjet=$FASTJET_ROOT \
            --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT --enable-blackhat=$BLACKHAT_ROOT --with-sqlite3=$SQLITE_ROOT \
            CXX="%cms_cxx" \
            CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF %cms_cxxflags -I$LHAPDF_ROOT/include -I$BLACKHAT_ROOT/include -I$OPENSSL_ROOT/include" \
            LDFLAGS="-ldl -L$BLACKHAT_ROOT/lib/blackhat -L$QD_ROOT/lib -L$OPENSSL_ROOT/lib"

make %{makeprocesses}

%install
make install
