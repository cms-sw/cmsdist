### RPM external frontier_client 2.7.2
Source: http://edge.fnal.gov:8888/frontier/%{n}__%{v}__src.tar.gz
#Source: http://cern.ch/service-spi/external/tarFiles/%{n}__%{v}__src.tar.gz
Requires: expat zlib openssl
%define realversion %(echo %v | cut -d_ -f1)                                              

%prep
%setup -n %{n}__%{v}__src
%build
make EXPAT_DIR=$EXPAT_ROOT \
     COMPILER_TAG=gcc_$GCC_VERSION \
     ZLIB_DIR=$ZLIB_ROOT \
     OPENSSL_DIR=$OPENSSL_ROOT
%install
mkdir -p %i/lib
mkdir -p %i/include
cp libfrontier_client.so.%{realversion} %i/lib                                            
cp -r include %i
ln -s %i/lib/libfrontier_client.so.%{realversion} %i/lib/libfrontier_client.so
ln -s %i/lib/libfrontier_client.so.%{realversion} %i/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
%post
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%{realversion} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
