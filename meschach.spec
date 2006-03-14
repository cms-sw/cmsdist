### RPM external meschach 1.2
Source: http://www.math.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz

%prep
%setup -c -n meschach-1.2 -a 0
%build
make
%install
mkdir -p %i/include
mkdir -p %i/lib
cp *.h %i/include
cp meschach.a %i/lib/libmeschach.a

