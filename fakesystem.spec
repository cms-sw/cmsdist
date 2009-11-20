### RPM external fakesystem 1.0
## NOCOMPILER
Source: none
Provides: /bin/zsh
Provides: /bin/ksh
Provides: /bin/sed
Provides: /bin/bash
Provides: /usr/bin/awk
Provides: /usr/bin/python
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
Provides: ld-linux.so.2(GLIBC_PRIVATE)
Provides: ld-linux-x86-64.so.2(GLIBC_PRIVATE)(64bit)

%prep
%build
%install
echo 'This package provides fake Provides for a small set of things which
are technically required to satisfy dependencies of CMSSW. All of these things are needed only by (for example) single shell or perl scripts, used only for standalone work, and thus we do not want to add them to the full required system seeds list.'> %{i}/README 
