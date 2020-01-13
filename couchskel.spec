### RPM cms couchskel 1.3.0.pre2
Source0: git://github.com/dmwm/WMCore?obj=master/%realversion&export=%n&output=/%n.tar.gz

# External javascripts
Source1: http://datatables.net/releases/DataTables-1.9.1.zip
Source2: https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.18/jquery-ui.min.js
Source3: http://code.jquery.com/jquery-1.7.2.min.js
Source4: http://d3js.org/d3.v2.min.js
Source5: https://raw.github.com/mbostock/protovis/v3.3.1/protovis.min.js
Requires: yui3

%prep
%setup -b 1 -n DataTables-1.9.1
%setup -b 0 -n %n

%build

%install
dst=%i/data/couchapps/%n
mkdir -p $dst
cp -rp %_builddir/%n/src/couchapps/couchskel/* $dst/

# jquery
mkdir -p $dst/vendor/jquery/_attachments
cp %_sourcedir/jquery-ui.min.js     $dst/vendor/jquery/_attachments/
cp %_sourcedir/jquery-[0-9]*.min.js $dst/vendor/jquery/_attachments/jquery.min.js

# protovis
mkdir -p $dst/vendor/protovis/_attachments
cp %_sourcedir/protovis.min.js      $dst/vendor/protovis/_attachments/

# D3
mkdir -p $dst/vendor/d3/_attachments
cp %_sourcedir/d3.v2.min.js         $dst/vendor/d3/_attachments/

# DataTables
mkdir -p $dst/vendor/datatables/_attachments
cp %_builddir/DataTables*/{media/js/jquery.dataTables.min,extras/ColVis/media/js/ColVis.min}.js \
   $dst/vendor/datatables/_attachments/

# Yui3 - add only the pieces you need
mkdir -p $dst/vendor/yui3/_attachments
cp -rp $YUI3_ROOT/build/{yui-base,panel}/*min.js $dst/vendor/yui3/_attachments/
