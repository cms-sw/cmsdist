### RPM external tkonlinesw-fake 2.7.0

Source: http://davidlt.web.cern.ch/davidlt/vault/final_fake/tkonlinesw-fake.tar.bz2
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
