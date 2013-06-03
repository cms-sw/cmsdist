### RPM external libjio 0.22

## INITENV +PATH LD_LIBRARY_PATH %{i}/lib

#   package information
Summary:      Journalled IO Library
URL:          http://users.auriga.wearlab.de/~alb/libjio/
Vendor:       Alberto Bertogli <albertogli@telpin.com.ar>
Packager:     Conrad Steenberg <conrad@hep.caltech.edu>

#   list of sources
Source: http://users.auriga.wearlab.de/~alb/libjio/files/%{v}/%{n}-%{v}.tar.bz2

#   build information
Requires: gcc

%description
Libjio is a userspace library to do journaled, transaction-oriented I/O.

It provides a very simple API to commit and rollback transactions, and on
top of that a UNIX-alike set of functions to perform most regular operations
(ie. open(), read(), write()) in a non-intrusive threadsafe and atomic way,
with safe and fast crash recovery. This allows the library to guarantee file
integrity even after unexpected crashes, never leaving your files in an
inconsistent state. On the disk, the file you work on is exactly like a
regular one, but a special directory is created to store in-flight
transactions.

%prep
%setup -n %n-%v

%build
make

%install
#    rm -rf %i

    mkdir -p -m 755 \
        %i/lib

    mkdir -p -m 755 \
        %i/bin

    mkdir -p -m 755 \
        %i/include

    mkdir -p -m 755 \
        %i/doc/libjio-%{v}

#ansi.c    check.o     common.h  jiofsck    libjio.h   README   unix.c
#ansi.o    checksum.c  common.o  jiofsck.c  libjio.so  samples  unix.o
#bindings  checksum.o  doc       jiofsck.o  Make.conf  trans.c  UPGRADING
#check.c   common.c    INSTALL   libjio.a   Makefile   trans.o  utils

       install -m 755 \
        jiofsck \
        %i/bin


       install -m 644 \
        libjio.h \
        %i/include


       install -m 644 \
        libjio.so libjio.a \
        %i/lib

       install -m 644 \
        INSTALL README UPGRADING \
        %i/doc/libjio-%{v}

    strip %i/bin/* >/dev/null 2>&1 || true

