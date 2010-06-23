### RPM external frontier_client 2.7.15
Source: http://frontier.cern.ch/dist/%{n}__%{realversion}__src.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Requires: expat
%if "%online" == "true"
Requires: onlinesystemtools
%else
Requires: zlib openssl
%endif

%prep
%setup -n %{n}__%{realversion}__src

%if "%online" != "true"
%define makeargs "EXPAT_DIR=$EXPAT_ROOT COMPILER_TAG=gcc_$GCC_VERSION ZLIB_DIR=$ZLIB_ROOT  OPENSSL_DIR=$OPENSSL_ROOT"
%else
%define makeargs "EXPAT_DIR=$EXPAT_ROOT COMPILER_TAG=gcc_$CXXCOMPILER_VERSION"
%endif
perl -p -i -e 's|-lssl|-lssl -lcrypto|' Makefile

%build

export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS

%install
mkdir -p %i/lib
mkdir -p %i/include
export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS distdir=%i dist

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="frontier_client" version="%v">
    <lib name="frontier_client"/>
    <client>
      <environment name="FRONTIER_CLIENT_BASE" default="%i"/>
      <environment name="INCLUDE" default="$FRONTIER_CLIENT_BASE/include"/>
      <environment name="LIBDIR" default="$FRONTIER_CLIENT_BASE/lib"/>
    </client>
    <runtime name="FRONTIER_CLIENT" value="$FRONTIER_CLIENT_BASE/"/>
    <use name="zlib"/>
    <use name="openssl"/>
    <use name="expat"/>
  </tool>
EOF_TOOLFILE

%post
case $(uname) in 
  Darwin ) 
    so=dylib 
    ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.%{realversion}.$so $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.$so
    ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.$so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/").$so
    ;; 
  * ) 
    so=so 
    ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.$so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.$so
    ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.$so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.$so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
    ;; 
esac
%{relocateConfig}etc/scram.d/%n.xml
