### RPM external dpm 1.7.0.6
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
# for x86_64 this was false, but it causes problems on installation at least with cmsBuild
 
%define baseVersion %(echo %v | cut -d- -f1 | cut -d. -f1,2,3)
%define patchLevel  %(echo %v | cut -d- -f1 | cut -d. -f4)
%define downloadv %{baseVersion}-%{patchLevel}
#%define dpmarch     %(echo %cmsplatf | cut -d_ -f1 | sed 's/onl//')
%define dpmarch slc4

Source: http://eticssoft.web.cern.ch/eticssoft/repository/org.glite/LCG-DM/%{baseVersion}/src/DPM-%{downloadv}sec.%{dpmarch}.src.rpm
# Source: http://cmsrep.cern.ch/cms/cpt/Software/download/cms.ap/SOURCES/%{cmsplatf}/external/dpm/%{downloadv}/DPM-%{downloadv}.src.rpm

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif
Provides: libdpm.so%{libsuffix}

%prep
rm -f %_builddir/DPM-%{downloadv}.src.tar.gz
rpm2cpio %{_sourcedir}/DPM-%{downloadv}sec.%{dpmarch}.src.rpm | cpio -ivd LCG-DM-%{baseVersion}.tar.gz
cd %_builddir ; rm -rf LCG-DM-%{baseVersion}; tar -xzvf LCG-DM-%{baseVersion}.tar.gz

%build
cd LCG-DM-%{baseVersion}
cp h/patchlevel.in h/patchlevel.h
perl -pi -e "s!__PATCHLEVEL__!%patchLevel!;s!__BASEVERSION__!\"%baseVersion\"!;s!__TIMESTAMP__!%(date +%%s)!" h/patchlevel.h
%if "%cpu" != "amd64"
perl -pi -e 's|ld\s+\$\(|ld -m elf_i386 \$\(|' shlib/Imakefile
%endif

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
cd LCG-DM-%{baseVersion}
cp ./shlib/lib%n.so %i/lib/lib%n.so.%realversion
cp ./h/*.h          %i/include/dpm
ln -s lib%n.so.%realversion %i/lib/lib%n.so
