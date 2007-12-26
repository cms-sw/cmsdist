### RPM external frontier_client 2.7.6-CMS18
Source: http://edge.fnal.gov:8888/frontier/%{n}__%{realversion}__src.tar.gz
#Source: http://cern.ch/service-spi/external/tarFiles/%{n}__%{realversion}__src.tar.gz

Requires: expat

%if "%{?online_release:set}" != "set"
Requires: zlib openssl
%else
Requires: systemtools
%endif

%prep
%setup -n %{n}__%{realversion}__src
%build

%if "%{?online_release:set}" != "set"
make EXPAT_DIR=$EXPAT_ROOT \
     COMPILER_TAG=gcc_$GCC_VERSION \
     ZLIB_DIR=$ZLIB_ROOT \
     OPENSSL_DIR=$OPENSSL_ROOT
%else
make EXPAT_DIR=$EXPAT_ROOT \
     COMPILER_TAG=gcc_$CXXCOMPILER_VERSION
%endif

%install
mkdir -p %i/lib
mkdir -p %i/include
cp libfrontier_client.so.%{realversion} %i/lib
cp -r include %i
ln -s %i/lib/libfrontier_client.so.%{realversion} %i/lib/libfrontier_client.so
ln -s %i/lib/libfrontier_client.so.%{realversion} %i/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")

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
</Tool>
EOF_TOOLFILE

%post
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
%{relocateConfig}etc/scram.d/%n
