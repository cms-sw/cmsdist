### RPM external python-tdb 0.0.6
Requires: gcc-wrapper
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}

Summary: Python binding for the Samba Trivial Database
Packager:Conrad Steenberg <conrad@hep.caltech.edu>
Vendor: Conrad Steenberg <conrad@hep.caltech.edu>

Source: http://julian.ultralight.org/clarens/devel/%n-%v.tar.gz
Requires: python tdb pyrex


%description

A Python binding for TDB. TDB is a Trivial Database. In concept, it is very
much like GDBM, and BSD's DB except that it allows multiple simultaneous
writers and uses locking internally to keep writers from trampling on each
other. TDB is also extremely small.

This binding exposes a low-level TDB interface class, as well as a dictionary
(mapping) class.

%prep
%setup -n %n-%v

%build
## IMPORT gcc-wrapper
mkdir build

export CFLAGS="-I$TDB_ROOT/include -I$LIBJIO_ROOT/include -D_FILE_OFFSET_BITS=64"
export LDFLAGS="-L$TDB_ROOT/lib -L$LIBJIO_ROOT/lib -ltdb -ljio"
python setup.py --build --prefix=%i
pwd
find build
echo $(find build -name tdb.so)
cp $(find build -name tdb.so) .

%install
mkdir -p %{i}/lib/python%{pythonv}
cp tdb.so %{i}/lib/python%{pythonv}

