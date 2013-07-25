### RPM external pcre 7.9
Source: http://downloads.sourceforge.net/%n/%n-%{realversion}.tar.bz2
Requires: bz2lib

%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%if "%online" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++ -std=c++0x
%endif

%prep
%setup -n %n-%{realversion}
%build
CPPFLAGS="-I${BZ2LIB_ROOT}/include -I${ZLIB_ROOT}/include"
LDFLAGS="-L${BZ2LIB_ROOT}/lib -L${ZLIB_ROOT}/lib"
./configure --enable-unicode-properties --enable-pcregrep-libz --enable-pcregrep-libbz2 --prefix=%i \
  CXX="%cms_cxx" CPPFLAGS="${CPPFLAGS}" LDFLAGS="${LDFLAGS}"
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
