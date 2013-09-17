### RPM external classlib 3.1.3
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
Source: http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc5_amd64_gcc472/external/classlib/3.1.3/classlib-3.1.3.tar.bz2
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Patch0: classlib-3.1.3-gcc46
Patch1: classlib-3.1.3-sl6
Patch2: classlib-3.1.3-fix-gcc47-cxx11
Patch3: classlib-3.1.3-fix-unwind-x86_64
Patch4: classlib-3.1.3-mic

Requires: bz2lib 
Requires: pcre 
Requires: xz
Requires: openssl
%if "%online" != "true"
Requires: zlib 
%else
Requires: onlinesystemtools
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n %n-%realversion
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%if "%mic" == "true"
%patch4 -p1
%endif

%build
%define xtra_make_opts CXX="%cms_cxx"
%define xtra_config_opts %{nil}
%define host %{nil}
%if "%mic" == "true"
%define xtra_make_opts CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" 
%define xtra_config_opts %{xtra_make_opts}
%define host --host=x86_64-k1om-linux
%endif
./configure --prefix=%i                         \
  --with-zlib-includes=$ZLIB_ROOT/include       \
  --with-zlib-libraries=$ZLIB_ROOT/lib          \
  --with-bz2lib-includes=$BZ2LIB_ROOT/include   \
  --with-bz2lib-libraries=$BZ2LIB_ROOT/lib      \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib          \
  --with-openssl-includes=$OPENSSL_ROOT/include \
  --with-openssl-libraries=$OPENSSL_ROOT/lib	\
  --with-lzma-includes=$XZ_ROOT/include         \
  --with-lzma-libraries=$XZ_ROOT/lib %{host} %{xtra_config_opts}

perl -p -i -e '
  s{-llzo2}{}g;
  !/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses %{xtra_make_opts} CXXFLAGS="-Wno-error=extra -ansi -pedantic -W -Wall -Wno-long-long -Werror %cms_cxxflags"

%install
make %makeprocesses install
