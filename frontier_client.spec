### RPM external frontier_client 2.4.2
Source: http://edge.fnal.gov:8888/frontier/%{n}__%{v}_cms__src.tar.gz
Requires: expat
%prep
%setup -n %{n}__%{v}_cms__src
%build 
make CXXOPT_APP="-Wall -g -O2 -DFRONTIER_DEBUG -DFNTR_USE_NAMESPACE -DFNTR_USE_EXCEPTIONS -fPIC -DPIC" \
     EXPAT_DIR=$EXPAT_ROOT \
     COMPILER_TAG=gcc_$GCC_VERSION
%install
mkdir -p %i/lib
mkdir -p %i/include
cp libfrontier_client.so.%{v} %i/lib
cp -r include %i
ln -s %i/lib/libfrontier_client.so.%{v} %i/lib/libfrontier_client.so
ln -s %i/lib/libfrontier_client.so.%{v} %i/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
%post
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%{v} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%{v} $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")

