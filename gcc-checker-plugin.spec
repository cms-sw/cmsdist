### RPM external gcc-checker-plugin 1.0
Source0:	https://gitlab.cern.ch/atlas/atlasexternals/-/archive/2.0.9/atlasexternals-2.0.9.tar.gz

Requires: gcc

%prep
%setup -n atlasexternals-2.0.9

%build
  plugindir=`gcc --print-file-name plugin`
  compilerdir=`gcc --print-file-name include`


  for f in External/CheckerGccPlugins/src/*.cxx; do
    g++ -c -g --std=c++11 -fPIC -O2 -fno-rtti -I${plugindir}/include -I${compilerdir} $f -o `basename $f`.o
  done
  g++ -shared -o libchecker_gccplugins.so *.o


%install
mkdir -p %{i}/lib
cp -p libchecker_gccplugins.so %{i}/lib
cp -rp External/CheckerGccPlugins/* %{i}
