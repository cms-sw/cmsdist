### RPM external alpgen 213
Source: http://mlm.home.cern.ch/mlm/alpgen/V2.1/v%{v}.tgz
Source1: config.sub-amd64
%prep
%setup -c -n alpgen-%v

%build
cd 2Qwork; make gen; cd ..
cd 4Qwork; make gen; cd ..
cd hjetwork; make gen; cd ..
cd Njetwork; make gen; cd ..
cd phjetwork; make gen; cd ..
cd QQhwork; make gen; cd ..
cd topwork; make gen; cd ..
cd vbjetwork; make gen; cd ..
cd wcjetwork; make gen; cd ..
cd wjetwork; make gen; cd ..
cd wqqwork; make gen; cd ..
cd zjetwork; make gen; cd ..
cd zqqwork; make gen; cd ..

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
