### RPM external millepede 03.00.00
# CAREFUL: NO VERSION IN TARBALL !!!
# Source: http://www.desy.de/~blobel/Mptwo.tgz
# Source: http://cmsrep.cern.ch/cmssw/millepede-mirror/millepede-2.0.tar.gz

%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://svnsrv.desy.de/public/MillepedeII/tags/V%svnTag/?scheme=http&module=V%svnTag&output=/millepede.tgz

Requires: castor

Patch: millepede_V02-00-01
Patch1: millepede_V02-00-01_64bit
Patch2: millepede_V02-00-01_gcc4
Patch3: millepede_V02-00-01_gcc45

%prep
%setup -n V%svnTag
%patch -p1

%if "%cpu" == "amd64"
%patch1 -p1
%endif

case %gccver in
  4.3.* | 4.4.*)
%patch2 -p1
  ;;
  4.5.*)
%patch3 -p1
  ;;
esac

perl -p -i -e "s!-lshift!-L$CASTOR_ROOT/lib -lshift!" Makefile
perl -p -i -e "s!C_INCLUDEDIRS =!C_INCLUDEDIRS = -I$CASTOR_ROOT/include!" Makefile

%build
make %makeprocesses

%install
make install
mkdir -p %i/bin
cp bin/* %i/bin

# Toolfile with only PATH
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# millepede tool file
cat << \EOF_TOOLFILE >%i/etc/scram.d/millepede.xml
  <tool name="millepede" version="%v">
    <info url="http://www.wiki.terascale.de/index.php/Millepede_II"/>
    <client>
      <environment name="MILLEPEDE_BASE" default="%i"/>
    </client>
    <runtime name="PATH" value="$MILLEPEDE_BASE/bin" type="path"/>
    <use name="sockets"/>
    <use name="pcre"/>
    <use name="zlib"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml


