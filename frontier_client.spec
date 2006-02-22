### RPM external frontier_client 2.4.2
Source: http://edge.fnal.gov:8888/frontier/%{n}__%{v}_cms__src.tar.gz
%prep
%setup -n %{n}__%{v}_cms__src
%build
make
%install
mkdir -p %i/lib
mkdir -p %i/include
cp libfrontier_client.so.%{v} %i/lib
ln -s %i/lib/libfrontier_client.so.%{v} %i/lib/libfrontier_client.so
ln -s %i/lib/libfrontier_client.so.%{v} %i/lib/libfrontier_client.so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
cp -r include %i
