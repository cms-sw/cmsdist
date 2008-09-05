### RPM external test 1.39-CMS19
## NOCOMPILER

# THIS IS A TEST SPEC FILE.
# IT SERVES THE SOLE PURPOSE OF UNIT/INTEGRATION TESTING THE BUILDING PROCEDURES.
# DO NOT USE, COPY OR MODIFY IT WITHOUT KNOWING WHAT YOU ARE DOING.

Source: http://switch.dl.sourceforge.net/sourceforge/e2fsprogs/e2fsprogs-%realversion.tar.gz

%prep
%setup -n e2fsprogs-%realversion
%build
mkdir -p %i
echo "This is a test" > %i/test.txt

%install

%pre
echo "A simple pre install script."
%post
echo "A simple post install script."
