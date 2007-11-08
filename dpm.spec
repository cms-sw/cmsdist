### RPM external dpm 1.6.5-5-CMS8
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac

%define baseVersion %realversion
%define patchLevel  %(echo %v | cut -d- -f2)
%define downloadv %{realversion}-%{patchLevel}
%define dpmarch     %(echo %cmsplatf | cut -d_ -f1 | sed 's/onl//')

Source: http://eticssoft.web.cern.ch/eticssoft/repository/org.glite/LCG-DM/%{realversion}/src/DPM-%{downloadv}sec.%{dpmarch}.src.rpm

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif
Provides: libdpm.so%{libsuffix}

%prep
rm -f %_builddir/DPM-%{realversion}.src.tar.gz
rpm2cpio %{_sourcedir}/DPM-%{downloadv}sec.%{dpmarch}.src.rpm | cpio -ivd DPM-%{realversion}.src.tar.gz
cd %_builddir ; rm -rf DPM-%{realversion}; tar -xzvf DPM-%{realversion}.src.tar.gz

%build
cd DPM-%{realversion}
cp h/patchlevel.in h/patchlevel.h
perl -pi -e "s!__PATCHLEVEL__!%patchLevel!;s!__BASEVERSION__!\"%baseVersion\"!;s!__TIMESTAMP__!%(date +%%s)!" h/patchlevel.h
perl -pi -e 's|ld\s+\$\(|ld -m elf_i386 \$\(|' shlib/Imakefile

for this in BuildDLI BuildDPMServer BuildNameServerDaemon BuildNameServerLibrary BuildRfioServer \
            BuildSRMv1Server BuildSRMv2Server BuildSRMv2_2Server BuildTest ; do
    perl -pi -e "s/\s+$this\s+YES/ $this\tNO/g" config/site.def
done

for this in BuildDPMClient BuildInterfaces BuildRfioClient; do
    perl -pi -e "s/\s+$this\s+NO/ $this\tYES/g" config/site.def
done
for this in Accounting HasNroff UseCupv UseKRB4 UseKRB5 UseMySQL UseOracle UseVirtualIds UseVOMS ; do
    perl -pi -e "s/\s+$this\s+YES/ $this\tNO/g" config/site.def
done
for this in SecMakeStaticLibrary BuildSecureRfio BuildSecureCns BuildSecureDpm ; do
    perl -pi -e "s/\s+$this\s+YES/ $this\tNO/g" config/site.def
done

mkdir -p %i/lib %i/include/dpm

./configure
cd shlib; make

%install
cd DPM-%{realversion}
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
