### RPM external glimpse 4.18.7-6
%define tag 23edbf54d45cefb1a5537598efe88d2b68470afb
Source: git+https://github.com/az143/glimpse.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

# Patches taken from Debian project
Patch1: glimpse-01-makefile
Patch2: glimpse-01-manpages
Patch3: glimpse-01-cross
Patch4: glimpse-12-manpage-hyphen
Patch5: glimpse-15-manpage-url
Patch6: glimpse-20-bin-spelling
Patch7: glimpse-25-fix-double-free
Patch8: glimpse-30-manpage-spelling

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
