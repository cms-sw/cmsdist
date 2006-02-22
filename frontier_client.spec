### RPM external frontier_client 2.1.3
%define frontierv %(echo %v | tr . _)
Source: http://edge.fnal.gov:8888/frontier/%{n}_%{frontierv}.tar.gz
%prep
%setup -n %{n}_%{frontierv}
%build
make
%install
mkdir -p %i/lib
mkdir -p %i/include
cp libfrontier_client.so.%{v} %i/lib
ln -s %i/lib/libfrontier_client.so.%{v} %i/lib/libfrontier_client.so
ln -s %i/lib/libfrontier_client.so.%{v} %i/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
cp -r include %i
