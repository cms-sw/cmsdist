### RPM external dpm 1.6.5-5
# DPM-%{realversion}.src.tar.gz file was actually extracted by hand using the 
# http://eticssoft.web.cern.ch/eticssoft/repository/org.glite/LCG-DM/1.6.5/src/DPM-%{v}sec.slc4.src.rpm
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac

%define baseVersion %realversion
%define patchLevel %(echo %v | cut -d- -f2)

Source: http://grid-deployment.web.cern.ch/grid-deployment/distribution/RpmBuild/i386-cel3/other/SOURCES/DPM-%{realversion}.src.tar.gz

%prep
%setup -n DPM-%{realversion}
%build
cp h/patchlevel.in h/patchlevel.h
perl -pi -e "s!__PATCHLEVEL__!%patchLevel!;s!__BASEVERSION__!\"%baseVersion\"!;s!__TIMESTAMP__!%(date +%%s)!" h/patchlevel.h
perl -pi -e 's|ld\s+\$\(|ld -m elf_i386 \$\(|' shlib/Imakefile

for this in BuildDLI BuildDPMServer BuildNameServerClient BuildNameServerDaemon BuildNameServerLibrary BuildRfioServer BuildSecurity \
            BuildSRMv1Server BuildSRMv2Server BuildSRMv2_2Server BuildTest ; do
    perl -pi -e "s/\s+$this\s+YES/ $this\tNO/g" config/site.def
done

for this in BuildDPMClient BuildInterfaces BuildRfioClient; do
    perl -pi -e "s/\s+$this\s+NO/ $this\tYES/g" config/site.def
done
for this in Accounting HasNroff UseCupv UseGSI UseKRB4 UseKRB5 UseMySQL UseOracle UseVirtualIds UseVOMS ; do
    perl -pi -e "s/\s+$this\s+YES/ $this\tNO/g" config/site.def
done
for this in SecMakeStaticLibrary BuildSecureRfio BuildSecureCns BuildSecureDpm ; do
    perl -pi -e "s/\s+$this\s+YES/ $this\tNO/g" config/site.def
done

mkdir -p %i/lib %i/include/dpm

./configure
cd shlib; make

%install
cp ./shlib/lib%n.so %i/lib/lib%n.so.%realversion
cp ./h/*.h          %i/include/dpm
ln -s lib%n.so.%realversion %i/lib/lib%n.so

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=dpm>
<Client>
 <Environment name=DPM_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$DPM_BASE/include"></Environment>
 <Environment name=LIBDIR default="$DPM_BASE/lib"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
