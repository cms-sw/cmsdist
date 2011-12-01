### RPM external google-perftools 1.6
Source: http://google-perftools.googlecode.com/files/%n-%{realversion}.tar.gz

%prep
%setup -n %n-%realversion

%build
# Make a fake library for now to keep everything happy. Actually building
# for 64bit requires building libunwind, which we are not yet doing at
# the moment.
    cat << \EOF_TMPFILE > tmpgp.cc
namespace gptmp {
  void foo(void*) {
  }
}
EOF_TMPFILE
g++ -c -o tmp.o -fPIC tmpgp.cc
g++ -shared -o libgptmp.so tmp.o

%install
# Just copy over the dummy library
mkdir -p %i/lib
cp libgptmp.so %i/lib/libtcmalloc.so
cp libgptmp.so %i/lib/libtcmalloc_minimal.so
