### RPM external pcre 7.9__8.33
%define generic_version 7.9
%define fc_version 8.33
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source0: http://downloads.sourceforge.net/%{n}/%{n}-%{generic_version}.tar.bz2
Source1: http://downloads.sourceforge.net/%{n}/%{n}-%{fc_version}.tar.bz2

Requires: bz2lib readline

%define isonline %(case %{cmsplatf} in (*onl_*_*) echo 1 ;; (*) echo 0 ;; esac)
%define isfc %(case %{cmsplatf} in (fc*) echo 1 ;; (*) echo 0 ;; esac)


%if %isonline
Requires: onlinesystemtools
%else
Requires: zlib
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++ -std=c++0x
%endif

%prep
%if %isfc
%setup -b 1 -n %{n}-%{fc_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
CPPFLAGS="-I${BZ2LIB_ROOT}/include -I${ZLIB_ROOT}/include -I${READLINE_ROOT}/include"
LDFLAGS="-L${BZ2LIB_ROOT}/lib -L${ZLIB_ROOT}/lib -L${READLINE_ROOT}/lib"
case %{cmsplatf} in
   *_mic_* )
     CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --enable-unicode-properties --enable-pcregrep-libbz2 --enable-pcregrep-libbz --prefix=%i \
     CPPFLAGS="${CPPFLAGS}" LDFLAGS="${LDFLAGS}" --host=x86_64-k1om-linux
     ;;
   * )
     ./configure --enable-unicode-properties --enable-pcregrep-libz --enable-pcregrep-libbz2 --prefix=%i \
     CXX="%cms_cxx" CPPFLAGS="${CPPFLAGS}" LDFLAGS="${LDFLAGS}"
     ;;
esac
make

%install
make install
# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries.
%define strip_files %i/lib

# Do not need to keep the archives.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
%define drop_files %i/share

%post
%{relocateConfig}bin/pcre-config

# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
