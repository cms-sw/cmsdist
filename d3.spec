### RPM external d3 2.7.4
## NOCOMPILER

Source: https://github.com/mbostock/d3/tarball/v%{realversion}

%prep
%setup -n mbostock-d3-0a6ad07

%build

%install
mkdir -p %i/data/d3
cp LICENSE *.js %i/data/d3
find lib \( -name '*.css' -o -name '*.js' \) | while read name; do
  dir=$(dirname $name)
  destdir=%i/data/${dir#lib/}
  mkdir -p $destdir
  cp $name $destdir/$(basename $name)
  cp $dir/LICENSE $destdir/LICENSE
done
find %i/data -type f -exec chmod 644 {} \;
