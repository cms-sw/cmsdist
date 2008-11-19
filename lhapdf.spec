### RPM external lhapdf 5.6.0
%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: lhapdf-5.6.0-g77

%prep
%setup -q -n %{n}/%{realversion}
# This applies both old and new fixes, probably the gcc4 ones can go (to check)
case %gccver in
  4.*)
    # Switch to gfortran
    perl -p -i -e 's|^export F77\=g77|export F77=gfortran|' .scripts/platform_functions
    perl -p -i -e 's| -Wno-globals||' configure
  ;;
  3.*)
%patch0 -p2
  ;;
esac
./configure --disable-pyext --enable-low-memory

%build
cp Makefile Makefile.orig
perl -p -i -e "s:\/usr\/lib64\/libc\.a::g" ./Makefile
perl -p -i -e "s:\/usr\/lib64\/libm\.a::g" ./Makefile
make 

%install
tar -c lib include PDFsets | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=lhapdf version=%v>
<lib name=lhapdf>
<lib name=lhapdf_dummy>
<Client>
 <Environment name=LHAPDF_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LHAPDF_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LHAPDF_BASE/include"></Environment>
 <Environment name=LHAPATH default="$LHAPDF_BASE/PDFsets"></Environment>
</Client>
<Runtime name=LHAPATH value="$LHAPDF_BASE/PDFsets" type=path>
<use name=f77compiler>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
