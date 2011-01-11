### RPM external sqlite 3.6.10
Source: http://www.sqlite.org/sqlite-%{realversion}.tar.gz
Patch1: sqlite_%{realversion}_readline_for_32bit_on_64bit_build

%prep
%setup -n %n-%{realversion}
# The following hack and patch are there because the libreadline.so soft
# link is missing from the 32-bit compatibility area on the 64-bit build
# machines and apparently they don't have a -devel build with it. It
# definitely should be reviewed at some point.
%patch1 -p1 
mkdir .libs

%build
./configure --prefix=%i --disable-tcl
make %makeprocesses

%install
make install
rm -rf %i/lib/pkgconfig
