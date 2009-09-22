### RPM external frontier_client 2.7.11
Source: http://frontier.cern.ch/dist/%{n}__%{realversion}__src.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo flase;; esac)

Patch0: frontier-2.7.11-dist-tarfile

Requires: expat
%if "%online" == "true"
Requires: onlinesystemtools
%else
Requires: zlib openssl
%endif

%prep
%setup -n %{n}__%{realversion}__src
%patch0 -p1
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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=frontier_client>
<client>
 <Environment name=FRONTIER_CLIENT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$FRONTIER_CLIENT_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$FRONTIER_CLIENT_BASE/lib"></Environment>
</client>
<use name=zlib>
<use name=openssl>
<use name=expat>
<Runtime name=FRONTIER_CLIENT_BASE value="$FRONTIER_CLIENT_BASE/">
</Tool>
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
%{relocateConfig}etc/scram.d/%n
