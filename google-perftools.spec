### RPM external google-perftools 0.98
Source: http://google-perftools.googlecode.com/files/%n-%{realversion}.tar.gz

%prep
%setup -n %n-%realversion

%build
%if (("%cmsplatf" == "slc4_ia32_gcc412")||("%cmsplatf" == "slc4_ia32_gcc422")||("%cmsplatf" == "slc4_ia32_gcc345"))
./configure --prefix=%i
make %makeprocesses
%endif
%if ("%cmsplatf" == "slc4_amd64_gcc345")
# Make a fake library for now to keep everything happy. Actually building
# for 64bit requires building libunwind, which we are not yet doing at
# the moment.
cat << \EOF_TMPFILE > tmpgp.cc
namespace gptmp {
  void foo(void*) {
  }
}
EOF_TMPFILE
g++ -c -o tmp.o -fPIC tmpgp.cc
g++ -shared -o libgptmp.so tmp.o
%endif

%install
%if (("%cmsplatf" == "slc4_ia32_gcc412")||("%cmsplatf" == "slc4_ia32_gcc422")||("%cmsplatf" == "slc4_ia32_gcc345"))
make install
%endif
%if ("%cmsplatf" == "slc4_amd64_gcc345")
# Just copy over the dummy library
mkdir -p %i/lib
cp libgptmp.so %i/lib/libtcmalloc.so
cp libgptmp.so %i/lib/libtcmalloc_minimal.so
%endif

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=tcmalloc_minimal version=%v>
<lib name=tcmalloc_minimal>
<client>
 <Environment name=GOOGLE-PERFTOOLS_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$GOOGLE-PERFTOOLS_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=tcmalloc version=%v>
<lib name=tcmalloc>
<client>
 <Environment name=GOOGLE-PERFTOOLS_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$GOOGLE-PERFTOOLS_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE


%post
%{relocateConfig}etc/scram.d/%n
