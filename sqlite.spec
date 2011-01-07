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
# Workaround for the lack of a 32bit readline-devel rpm for SL4
# Given that the 64bit readline-devel is there, the headers are there,
# the only thing missing is the libreadline.so symlink. This is not
# a problem for SL5.
case %cmsos in
  slc4*ia32 )
    ln -s /usr/lib/libreadline.so.4.3 .libs/libreadline.so
  ;;
esac

%build
./configure --prefix=%i --disable-tcl
make %makeprocesses

%install
make install
