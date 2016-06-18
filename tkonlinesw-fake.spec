### RPM external tkonlinesw-fake 4.1.0-1

Source: http://davidlt.web.cern.ch/davidlt/vault/tkonlinesw-fake-v4.tar.bz2
%prep
%setup -n tkonlinesw-fake

%build
# NOP

%install
mkdir -p %{i}/lib

cp -r include %{i}

g++ -shared -fPIC -o libDeviceDescriptions.so DeviceDescriptions.cc
g++ -shared -fPIC -o libFed9UDeviceFactory.so Fed9UDeviceFactory.cc
g++ -shared -fPIC -o libICUtils.so ICUtils.cc
g++ -shared -fPIC -o libFed9UUtils.so Fed9UUtils.cc

cp *.so %{i}/lib
