### RPM external meschach 1.2.pCMS1-CMS3
Source: http://www.math.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz
Patch: meschach-1.2-slc4

%prep
%setup -c -n meschach-1.2 -a 0
%patch -p0

%build
make
%install
mkdir -p %i/include
mkdir -p %i/lib
cp *.h %i/include
cp meschach.a %i/lib/libmeschach.a

