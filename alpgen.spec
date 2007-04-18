### RPM external alpgen 205
Requires: gcc-wrapper
Source: http://mlm.home.cern.ch/mlm/alpgen/V2.0/v%{v}.tgz
Source1: config.sub-amd64
%prep
%setup -c -n alpgen-%v

%build
## IMPORT gcc-wrapper
cd 2Qwork; make 2Qgen; cd ..
cd 4Qwork; make 4Qgen; cd ..
cd hjetwork; make hjetgen; cd ..
cd Njetwork; make Njetgen; cd ..
cd phjetwork; make phjetgen; cd ..
cd QQhwork; make QQhgen; cd ..
cd topwork; make topgen; cd ..
cd vbjetwork; make vbjetgen; cd ..
cd wcjetwork; make wcjetgen; cd ..
cd wjetwork; make wjetgen; cd ..
cd wqqwork; make wqqgen; cd ..
cd zjetwork; make zjetgen; cd ..
cd zqqwork; make zqqgen; cd ..

%install
mkdir -p %{i}/bin
mkdir -p %{i}/alplib
cp 2Qwork/2Qgen %{i}/bin/
cp 4Qwork/4Qgen %{i}/bin/
cp hjetwork/hjetgen %{i}/bin/
cp Njetwork/Njetgen %{i}/bin/
cp phjetwork/phjetgen %{i}/bin/
cp QQhwork/QQhgen %{i}/bin/
cp topwork/topgen %{i}/bin/
cp vbjetwork/vbjetgen %{i}/bin/
cp wcjetwork/wcjetgen %{i}/bin/
cp wjetwork/wjetgen %{i}/bin/
cp wqqwork/wqqgen %{i}/bin/
cp zjetwork/zjetgen %{i}/bin/
cp zqqwork/zqqgen %{i}/bin/
cp -R alplib/* %{i}/alplib/
#
