### RPM cms fakesystem 1.0
## REVISION 1009
## NOCOMPILER
## NO_VERSION_SUFFIX

# Various perl modules/dependencies that are needed only for specialized scripts
# One should install these on host system to run perl part of these tools
####################################
# Needed by autotools
####################################
#  Carp, Cwd, Data::Dumper, Errno, Exporter
#  File::Path, File::Spec, File::Temp
#  Getopt::Long, Text::ParseWords, constant
####################################
# Needed by git
####################################
# Carp, Cwd, DBI, Data::Dumper, Digest::MD5, Exporter
# File::Path, File::Spec, File::Spec::Functions, File::Temp
# Getopt::Long, Text::ParseWords, constant
####################################
# Needed by xrootd
####################################
# Cwd, Exporter, Socket

Provides: perl(CMSDBA)
Provides: perl(Carp)
Provides: perl(Cwd)
Provides: perl(DBI)
Provides: perl(Data::Dumper)
Provides: perl(Date::Format)
Provides: perl(Digest::MD5)
Provides: perl(Errno)
Provides: perl(Exporter)
Provides: perl(File::Path)
Provides: perl(File::Spec)
Provides: perl(File::Spec::Functions)
Provides: perl(File::Temp)
Provides: perl(Getopt::Long)
Provides: perl(LWP::UserAgent)
Provides: perl(Socket)
Provides: perl(Template)
Provides: perl(Term::ReadKey)
Provides: perl(Text::ParseWords)
Provides: perl(Tk) >= 804
Provides: perl(Tk::DialogBox)
Provides: perl(Tk::ROText)
Provides: perl(constant)
Provides: perl(full)

#################################
# Needed by git on SLC7
#################################
Provides: perl(CGI)
Provides: perl(CGI::Carp)
Provides: perl(CGI::Util)
Provides: perl(Encode)
Provides: perl(SVN::Core)
Provides: perl(SVN::Delta)
Provides: perl(SVN::Ra)
Provides: perl(Scalar::Util)
Provides: perl(Storable)
Provides: perl(Time::HiRes)
Provides: perl(Time::Local)
Provides: perl(YAML::Any)

#################################
# Needed by madgraph5amcatnlo
#################################
Provides: perl(Compress::Zlib)
Provides: perl(List::Util)

#################################
# Needed by cmssw
#################################
Provides: perl(Switch)

#################################
# Needed by git on CC8
#################################
Provides: perl(Memoize)
Provides: perl(Net::Domain)
Provides: perl(Net::SMTP)
Provides: perl(Term::ANSIColor)
Provides: perl(IO::File)

#################################
# Needed by git on CS9
#################################
Provides: perl(Fcntl)
Provides: perl(File::Basename)
Provides: perl(File::Find)
Provides: perl(Getopt::Std)
Provides: perl(IO::Pipe)
Provides: perl(IO::Socket)
Provides: perl(IPC::Open2)
Provides: perl(IPC::Open3)
Provides: perl(POSIX)
Provides: perl(Term::ReadLine)
Provides: perl(FileHandle)
Provides: perl(File::Copy)
Provides: perl(File::stat)
Provides: perl(Time::localtime)
Provides: perl(sort)

Provides: /bin/csh
Provides: /bin/tcsh
Provides: /bin/env

%prep
%build
%install
echo 'This package provides fake Provides for a small set of things which
are technically required to satisfy dependencies of CMSSW. All of these things are needed only by (for example) single shell or perl scripts, used only for standalone work, and thus we do not want to add them to the full required system seeds list.'> %{i}/README 
