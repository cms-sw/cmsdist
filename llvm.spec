### RPM external llvm 2.8
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

Source0: http://llvm.org/releases/%realversion/llvm-%realversion.tgz
Source1: http://llvm.org/releases/%realversion/clang-%realversion.tgz 

%prep
%setup -T -b0 -n llvm-%realversion
%setup -T -D -a1 -c -n llvm-%realversion/tools
mv clang-%realversion clang
%setup -T -D -n llvm-%realversion

%build
mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized
make %makeprocesses

%install
cd objs
make install
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config

case %cmsos in 
  osx*)
    #Fix up install names for some of the libraries.
    for x in BugpointPasses.dylib profile_rt.dylib LLVMHello.dylib
    do
      install_name_tool -change $x lib$x -id lib$x %i/lib/lib$x
    done
  ;;
esac

