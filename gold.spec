### RPM external gold 2.19.1
## BUILDIF case `uname`:`uname -p` in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
# This builds a gold-enabled binutils. 
Source0: http://ftp.gnu.org/gnu/binutils/binutils-%realversion.tar.bz2
Patch0: binutils-2.19.1-fix-gold

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define gcc_major %(echo %realversion | cut -f1 -d.)
%prep
%setup -n binutils-%realversion
%patch0 -p1
case %cmsos in 
  slc*_amd64 )
    # This patches the default linker script to align stuff at 4096 kB boundaries rather 
    # than the default 2MB (MAXPAGESIZE value for x86_64 architecture).
    perl -p -i -e 's|\$[{]MAXPAGESIZE[}]|4096|g;s|\$[{]SEGMENT_SIZE[}]|4096|g' ld/scripttempl/elf.sc
  ;;
esac
%build
./configure --prefix=%i --enable-gold
make %makeprocesses

%install
make install
find %i/lib %i/lib64 -name '*.la' -exec rm -f {} \; || true

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gold
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=gold version=@GOLD_VERSION@>
<client>
 <Environment name=GOLD_BASE default="@GOLD_ROOT@"></Environment>
 <Environment name=GOLDBINDIR default="$GOLD_BASE/bin"></Environment>
</client>
<Runtime name=LD_LIBRARY_PATH value="$GOLD_BASE/lib" type=path>
<Runtime name=PATH value="$GOLD_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
