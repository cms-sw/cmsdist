### RPM external tdb 1.0.6

Summary: Trivial Database
Group: System Environment/Libraries
URL: http://sourceforge.net/projects/tdb/

Packager:Conrad Steenberg <conrad@hep.caltech.edu>
Vendor: Conrad Steenberg <conrad@hep.caltech.edu>

Source: http://surfnet.dl.sourceforge.net/sourceforge/tdb/tdb-%{v}.tar.gz
Patch0: tdb-1.0.6-gcc33
Patch1: tdb-1.0.6-libjio
Requires: libjio gcc


%description
TDB is a Trivial Database. In concept, it is very much like GDBM, 
and BSD's DB except that it allows multiple simultaneous writers 
and uses locking internally to keep writers from trampling on 
each other. TDB is also extremely small.

%prep
%setup -n tdb-%{v}
%patch0 -b .gcc3
%patch1 -p1 -b .jio

%build
echo LIBJIO_ROOT=$LIBJIO_ROOT
export CFLAGS="-I%{i}/include -I$LIBJIO_ROOT/include -D_FILE_OFFSET_BITS=64"\
  LDFLAGS="-L%{i}/lib -L$LIBJIO_ROOT/lib -ljio -lpthread"
./configure --prefix %{i}
make TDBTEST="" LDFLAGS="-L%{i}/lib -L$LIBJIO_ROOT/lib -ljio -lpthread"

%install
rm -rf %{buildroot}
make install TDBTEST=""

### Clean up buildroot
#%{__rm} -f %{buildroot}%{_libdir}/*.la

docdir=%{i}/doc/%{n}-%{v}
mkdir -p $docdir

cp AUTHORS ChangeLog COPYING NEWS README TODO $docdir


%files
%defattr(-, root, root, 0755)
%{i}/lib/*.so.*
%{i}/bin 
%{i}/etc 
%{i}/doc
%{i}/lib/*.a
%{i}/include 
#%{i}/man
