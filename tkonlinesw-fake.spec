### RPM external tkonlinesw-fake 4.2.0-1_gcc7

%define tag 97afe74471b299148ac9ccdea21e9cda961ec885
Source: https://github.com/cms-externals/%{n}/archive/%{tag}.tar.gz

%prep
%setup -n %{n}-%{tag}

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
