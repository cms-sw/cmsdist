### RPM external glimpse 4.18.7-6
%define tag 5426ca983218befa4aeadf21cad2305d90c84adb
Source: git+https://github.com/cms-externals/glimpse.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%realversion
%build
./configure --prefix=%{i} 
# Turn off this part, it causes problems for 32-bit-on-64-bit and is only
# needed for webglimpse
perl -p -i -e "s|dynfilters||g" Makefile
# Notice: parallel build doesn't work
make -j1

%install
make install
