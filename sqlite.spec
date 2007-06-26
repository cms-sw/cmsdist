### RPM external sqlite 3.3.5-XXXX
Source: http://www.sqlite.org/%{n}-%{realversion}.tar.gz
Patch1: sqlite_3.3.5_readline_for_32bit_on_64bit_build

%prep
%setup -n %n-%{realversion}
# The following hack and patch are there because the libreadline.so soft
# link is missing from the 32-bit compatibility area on the 64-bit build
# machines and apparently they don't have a -devel build with it. It
# definitely should be reviewed at some point.
%patch1 -p1
mkdir .libs
ln -s /usr/lib/libreadline.so.4.3 .libs/libreadline.so

%build
./configure --prefix=%i --disable-tcl
make %makeprocesses
