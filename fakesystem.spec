### RPM external fakesystem 1.0
## NOCOMPILER

# Various system scripts
Provides: /bin/zsh
Provides: /bin/ksh
Provides: /bin/sed
Provides: /bin/bash
Provides: /usr/bin/awk
Provides: /usr/bin/python
# Various perl modules/dependencies that are needed only for specialized
# scripts
Provides: perl(Date::Format)
Provides: perl(Term::ReadKey)
Provides: perl(full)
Provides: perl(LWP::UserAgent)
Provides: perl(Template)
Provides: perl(CMSDBA)
Provides: perl(Tk) >= 804
Provides: perl(Tk::ROText)
Provides: perl(Tk::DialogBox)
Provides: perl(DBI)
# These appear to be needed by Iguana/Utilities once we moved to SLC5
# Add them here, but why they are needed should be understood. 
Provides: ld-linux.so.2(GLIBC_PRIVATE)
Provides: ld-linux-x86-64.so.2(GLIBC_PRIVATE)(64bit)
# The following are for oracle 11.2.0.1.0, which apparently needs libaio.
# Since oracle in principle is only used at CERN, don't require this 
# everywhere, use instead fake provides
Provides: libaio.so.1
Provides: libaio.so.1(LIBAIO_0.1)
Provides: libaio.so.1(LIBAIO_0.4)
Provides: libaio.so.1()(64bit)
Provides: libaio.so.1(LIBAIO_0.1)(64bit)
Provides: libaio.so.1(LIBAIO_0.4)(64bit)

%prep
%build
%install
echo 'This package provides fake Provides for a small set of things which
are technically required to satisfy dependencies of CMSSW. All of these things are needed only by (for example) single shell or perl scripts, used only for standalone work, and thus we do not want to add them to the full required system seeds list.'> %{i}/README 
# bla bla
