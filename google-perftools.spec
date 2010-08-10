### RPM external google-perftools 1.4
Source: http://google-perftools.googlecode.com/files/%n-%{realversion}.tar.gz

%prep
%setup -n %n-%realversion

%build
case %cmsplatf in
  slc4_ia32* | slc5_ia32* | osx105_ia32* )
    ./configure --prefix=%i
    make %makeprocesses
  ;;
  slc4_amd64* | slc5_amd64*)
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
  ;;
esac

%install
case %cmsplatf in
  slc4_ia32* | slc5_ia32* | osx105_ia32* )
    make install
  ;;
  slc4_amd64* | slc5_amd64*)
    # Just copy over the dummy library
    mkdir -p %i/lib
    cp libgptmp.so %i/lib/libtcmalloc.so
    cp libgptmp.so %i/lib/libtcmalloc_minimal.so
  ;;
esac
