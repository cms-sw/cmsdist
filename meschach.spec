### RPM external meschach 1.2.pCMS1
Source: http://www.math.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz
Patch: meschach-1.2-slc4
Patch1: meschach-1.2b-fPIC

%define keep_archives true


%prep
%setup -c -n meschach-1.2 -a 0
%patch -p0
%patch1 -p0

%build
# Just fix this by hand for MacOSX (the configure probably needs to be updated)
%ifarch darwin
perl -p -i -e "s|define HAVE_MALLOC_H 1|undef MALLOCDECL|g" machine.h
%endif
make
%install
mkdir -p %i/include
mkdir -p %i/lib
cp *.h %i/include
cp meschach.a %i/lib/libmeschach.a
