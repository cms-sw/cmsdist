### RPM external frontier_client 2.9.0
## INITENV +PATH PYTHON27PATH %{i}/python/lib
## INITENV +PATH PYTHON3PATH %{i}/python/lib

Source: http://frontier.cern.ch/dist/%{n}__%{realversion}__src.tar.gz
Requires: expat pacparser python zlib

Patch0: frontier_client-2.8.20-add-python-dbapi

%prep
%setup -n %{n}__%{realversion}__src

%define makeargs "EXPAT_DIR=${EXPAT_ROOT} PACPARSER_DIR=${PACPARSER_ROOT} COMPILER_TAG=gcc_$(gcc -dumpversion) ZLIB_DIR=${ZLIB_ROOT}"

%patch0 -p1

%build

export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS CXXFLAGS="-ldl" CFLAGS=""

%install
mkdir -p %i/lib
mkdir -p %i/include
export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS CXXFLAGS="-ldl" distdir=%i dist

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

cp -r python %i

