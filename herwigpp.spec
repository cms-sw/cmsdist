### RPM external herwigpp 2.3.2
Source: http://projects.hepforge.org/herwig/files/Herwig++-%{realversion}.tar.gz
Requires: thepeg
Requires: gsl
Requires: hepmc

Patch0: herwigpp-2.3.2-g77

%prep
%setup -q -n Herwig++-%{realversion}
case %gccver in
  3.*)
%patch0 -p1
  ;;
esac

./configure --with-hepmc=$HEPMC_ROOT --with-gsl=$GSL_ROOT --with-thepeg=$THEPEG_ROOT --prefix=%i CXXFLAGS="-O2 -fuse-cxa-atexit"
# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' Makefile
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' */Makefile
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' */*/Makefile
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' */*/*/Makefile

%build
make %makeprocesses 


%install
#tar -c -h lib include | tar -x -C %i
make install
rm %i/share/Herwig++/Doc/fixinterfaces.pl

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=herwigpp version=%v>
<Client>
 <Environment name=HERWIGPP_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$HERWIGPP_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$HERWIGPP_BASE/include"></Environment>
</Client>
<Runtime name=HERWIGPATH value="$HERWIGPP_BASE/share/Herwig++">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}share/Herwig++/HerwigDefaults.rpo
