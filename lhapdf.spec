### RPM external lhapdf 5.6.0
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: lhapdf-5.6.0-g77
Patch1: lhapdf-5.6.0-32bit-on-64bit-recheck-workaround
  
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
%patch1 -p2

%build
./configure --disable-pyext --enable-low-memory --prefix=%i --with-max-num-pdfsets=1

perl -p -i -e 's|/usr/lib64/libm.a||g' config.status
perl -p -i -e 's|/usr/lib64/libc.a||g' config.status
perl -p -i -e 's|/usr/lib64/libm.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
perl -p -i -e 's|/usr/lib64/libc.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
make 

%install
make install
# do another install-round for full libs
make distclean
%define fulllibpath %(echo %i"/full")
%define fullname %(echo %n"full")
./configure --disable-pyext --prefix=%fulllibpath --disable-pdfsets
perl -p -i -e 's|/usr/lib64/libm.a||g' config.status
perl -p -i -e 's|/usr/lib64/libc.a||g' config.status
perl -p -i -e 's|/usr/lib64/libm.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
perl -p -i -e 's|/usr/lib64/libc.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
make
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=lhapdf version=%v>
<lib name=LHAPDF>
<Client>
 <Environment name=LHAPDF_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LHAPDF_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LHAPDF_BASE/include"></Environment>
 <Environment name=LHAPATH default="$LHAPDF_BASE/share/lhapdf/PDFsets"></Environment>
</Client>
<Runtime name=LHAPATH value="$LHAPDF_BASE/share/lhapdf/PDFsets" type=path>
<use name=f77compiler>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdfwrap
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=lhapdfwrap version=%v>
<lib name=LHAPDFWrap>
<use name=lhapdf>
</Tool>
EOF_TOOLFILE

# SCRAM ToolBox toolfiles for full libs
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%fullname
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=lhapdffull version=%v>
<lib name=LHAPDF>
<Client>
 <Environment name=LHAPDF_BASE default="%i"></Environment>
 <Environment name=LHAPATH_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LHAPDF_BASE/full/lib"></Environment>
 <Environment name=INCLUDE default="$LHAPDF_BASE/include"></Environment>
 <Environment name=LHAPATH default="$LHAPATH_BASE/share/lhapdf/PDFsets"></Environment>
</Client>
<Runtime name=LHAPATH value="$LHAPATH_BASE/share/lhapdf/PDFsets" type=path>
<use name=f77compiler>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdfwrapfull
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=lhapdfwrap version=%v>
<lib name=LHAPDFWrap> 
<use name=lhapdffull>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/scram.d/%fullname
%{relocateConfig}lib/libLHAPDF.la
%{relocateConfig}lib/libLHAPDFWrap.la
