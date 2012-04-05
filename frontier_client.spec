### RPM external frontier_client 2.8.4
Source: http://frontier.cern.ch/dist/%{n}__%{realversion}__src.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Requires: expat
%if "%online" != "true"
Requires: openssl
Requires: zlib
%else
Requires: onlinesystemtools
%endif

%prep
%setup -n %{n}__%{realversion}__src

%if "%online" != "true"
%define makeargs "EXPAT_DIR=$EXPAT_ROOT COMPILER_TAG=gcc_$GCC_VERSION ZLIB_DIR=$ZLIB_ROOT  OPENSSL_DIR=$OPENSSL_ROOT"
%else
%define makeargs "EXPAT_DIR=$EXPAT_ROOT COMPILER_TAG=gcc_$CXXCOMPILER_VERSION"
%endif

%build

export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS

%install
mkdir -p %i/lib
mkdir -p %i/include
export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS distdir=%i dist

case $(uname) in 
  Darwin ) 
    so=dylib 
    ln -sf libfrontier_client.%{realversion}.$so %i/lib/libfrontier_client.$so
    ln -sf libfrontier_client.$so.%{realversion} %i/libfrontier_client.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/").$so
    ;; 
  * ) 
    so=so 
    ln -sf libfrontier_client.$so.%{realversion} %i/lib/libfrontier_client.$so
    ln -sf libfrontier_client.$so.%{realversion} %i/lib/libfrontier_client.$so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
    ;; 
esac
