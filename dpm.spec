### RPM external dpm 1.8.0.1
 
%define baseVersion %(echo %v | cut -d- -f1 | cut -d. -f1,2,3)
%define patchLevel  %(echo %v | cut -d- -f1 | cut -d. -f4)
%define downloadv %{baseVersion}-%{patchLevel}
#%define dpmarch     %(echo %cmsplatf | cut -d_ -f1 | sed 's/onl//')
%define dpmarch sl5

Source: http://eticssoft.web.cern.ch/eticssoft/repository/org.glite/LCG-DM/%{baseVersion}/src/DPM-mysql-%{downloadv}sec.%{dpmarch}.src.rpm
# Source: http://cmsrep.cern.ch/cms/cpt/Software/download/cms.ap/SOURCES/%{cmsplatf}/external/dpm/%{downloadv}/DPM-%{downloadv}.src.rpm
Patch0: dpm-1.7.4.7-ld
Patch1: dpm-1.7.4.7-macosx
Patch2: dpm-1.8.0-shlib-macosx

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif
Provides: libdpm.so%{libsuffix}

%prep
rm -f %_builddir/DPM-%{downloadv}.src.tar.gz
rpm2cpio %{_sourcedir}/DPM-mysql-%{downloadv}sec.%{dpmarch}.src.rpm | cpio -ivd LCG-DM-%{baseVersion}.tar.gz
cd %_builddir ; rm -rf LCG-DM-%{baseVersion}; tar -xzvf LCG-DM-%{baseVersion}.tar.gz

perl -p -i -e 's|SHLIBREQLIBS = -lc|SHLIBREQLIBS = -lc /usr/lib/dylib1.o|' LCG-DM-%{baseVersion}/config/darwin.cf
perl -p -i -e 's|FC = g77|FC = gfortran|' LCG-DM-%{baseVersion}/config/darwin.cf
cd LCG-DM-%{baseVersion}
%patch0 -p1
case %cmsos in 
  osx*) 
%patch1 -p2
%patch2 -p2
;;
esac

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

./configure dpm --with-client-only
cd shlib; make

%install
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

cd LCG-DM-%{baseVersion}
cp ./shlib/lib%n.$SONAME %i/lib/lib%n.$SONAME.%realversion
# RPM 4.4.2.2 didn't seem to be happy with the dependencies if a symlink
# and realversion was used for liblcgdm.so, so just leave it with the original
# name
cp ./shlib/liblcgdm.$SONAME %i/lib/
cp ./h/*.h          %i/include/dpm
ln -s lib%n.$SONAME.%realversion %i/lib/lib%n.$SONAME
# bla bla
