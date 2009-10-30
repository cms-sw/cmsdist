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

%prep
%setup -n V%svnTag
%patch -p1

%if "%cpu" == "amd64"
%patch1 -p1
%endif

case %gccver in
  4.*)
%patch2 -p1
  ;;
esac

perl -p -i -e "s!-lshift!-L$CASTOR_ROOT/lib -lshift!" Makefile

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
cat << \EOF_TOOLFILE >%i/etc/scram.d/millepede
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=millepede version=%v>
<info url="http://www.wiki.terascale.de/index.php/Millepede_II"></info>
<Client>
 <Environment name=MILLEPEDE_BASE default="%i"></Environment>
</Client>
<use name=sockets>
<use name=pcre>
<use name=zlib>
<Runtime name=PATH value="$MILLEPEDE_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n


