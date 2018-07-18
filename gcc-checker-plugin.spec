### RPM external gcc-checker-plugin 1.1
Source0:	https://github.com/gartung/CheckerGccPlugins/archive/1.1.tar.gz

Requires: gcc

%prep
%setup -n CheckerGccPlugins-1.1

%build
make 

%install
cp -rp * %{i}
