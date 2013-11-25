### RPM external pcre-host 7.9__8.33
%define generic_version 7.9
%define fc_version 8.33
Source0: http://downloads.sourceforge.net/pcre/pcre-%{generic_version}.tar.bz2
Source1: http://downloads.sourceforge.net/pcre/pcre-%{fc_version}.tar.bz2

Requires: bz2lib-bootstrap readline-host

%define isonline %(case %{cmsplatf} in (*onl_*_*) echo 1 ;; (*) echo 0 ;; esac)
%define isfc %(case %{cmsplatf} in (fc*) echo 1 ;; (*) echo 0 ;; esac)


%if %isonline
Requires: onlinesystemtools
%else
Requires: zlib-bootstrap
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++ -std=c++0x
%endif

%prep
%if %isfc
%setup -b 1 -n pcre-%{fc_version}
%else
%setup -b 0 -n pcre-%{generic_version}
%endif

%build
BZ2LIB_ROOT=$BZ2LIB_BOOTSTRAP_ROOT
READLINE_ROOT=$READLINE_HOST_ROOT
ZLIB_ROOT=$ZLIB_BOOTSTRAP_ROOT
CPPFLAGS="-I${BZ2LIB_ROOT}/include -I${ZLIB_ROOT}/include -I${READLINE_ROOT}/include"
LDFLAGS="-L${BZ2LIB_ROOT}/lib -L${ZLIB_ROOT}/lib -L${READLINE_ROOT}/lib"
./configure --enable-unicode-properties --enable-pcregrep-libz --enable-pcregrep-libbz2 --prefix=%i \
   CXX="%cms_cxx" CPPFLAGS="${CPPFLAGS}" LDFLAGS="${LDFLAGS}"
make

%install
make install
# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
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
