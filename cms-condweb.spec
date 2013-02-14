### RPM cms cms-condweb CMS_CONDWEB_0_1

#
# to run/build:
# cvs -Q -d:ext:cmssw.cvs.cern.ch:/local/reps/CMSSW co  PKGTOOLS
# cvs -Q -d:ext:cmssw.cvs.cern.ch:/local/reps/CMSSW co -r CMS_CONDWEB_0_1 CMSDIST
# mkdir build; cd build
# ../PKGTOOLS/cmsBuild -c ../CMSDIST -a osx108_amd64_gcc472  build cms-condweb
#

Requires: cherrypy
Requires: py2-pyopenssl
Requires: py2-sqlalchemy
Requires: py2-sqlalchemy
Requires: py2-cx-oracle
Requires: py2-lint
Requires: py2-cjson
Requires: py2-pycurl
Requires: py2-jinja

%prep

%build

%install

