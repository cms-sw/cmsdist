### RPM cms fakesystem 1.0
## REVISION 1000
## NOCOMPILER
## NO_VERSION_SUFFIX

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
Provides: perl(Carp)
Provides: perl(Cwd)
Provides: perl(Data::Dumper)
Provides: perl(Exporter)
Provides: perl(File::Path)
Provides: perl(File::Spec)
Provides: perl(File::Temp)
Provides: perl(Getopt::Long)
Provides: perl(Text::ParseWords)
Provides: perl(constant)
Provides: perl(Errno)
Provides: perl(Digest::MD5)
Provides: perl(File::Spec::Functions)
#needed by xrootd
Provides: perl(Socket)

%prep
%build
%install
echo 'This package provides fake Provides for a small set of things which
are technically required to satisfy dependencies of CMSSW. All of these things are needed only by (for example) single shell or perl scripts, used only for standalone work, and thus we do not want to add them to the full required system seeds list.'> %{i}/README 
