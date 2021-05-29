### RPM external frontier_client 2.9.1
## INITENV +PATH PYTHON27PATH %{i}/python/lib
## INITENV +PATH PYTHON3PATH %{i}/python/lib

%define tag 888a611d4ab15d6ce03830c63b850539460dcda9
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: expat pacparser python zlib

%prep
%setup -n %{n}-%{realversion}

%define makeargs "EXPAT_DIR=${EXPAT_ROOT} PACPARSER_DIR=${PACPARSER_ROOT} COMPILER_TAG=gcc_$(gcc -dumpversion) ZLIB_DIR=${ZLIB_ROOT}"

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

