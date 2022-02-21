### RPM external glimpse 4.18.7
%define tag 49457116bb0796636fd1bc84f39006fb102bfafc
Source: git+https://github.com/gvelez17/glimpse.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: autotools
%prep
%setup -n glimpse-%realversion
%build
./configure --prefix=%{i} 
# Turn off this part, it causes problems for 32-bit-on-64-bit and is only
# needed for webglimpse
perl -p -i -e "s|dynfilters||g" Makefile
make 

%install
make install
