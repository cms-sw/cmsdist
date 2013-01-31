### RPM external xregexp 1.5.0
## NOCOMPILER

Source0: http://xregexp.com/xregexp.js
Source1: http://xregexp.com/plugins/xregexp-unicode-base.js
Source2: http://xregexp.com/plugins/xregexp-unicode-categories.js
Source3: http://xregexp.com/plugins/xregexp-unicode-scripts.js
Source4: http://xregexp.com/plugins/xregexp-unicode-blocks.js
Source5: http://xregexp.com/plugins/xregexp-matchrecursive.js
Requires: yuicompressor
BuildRequires: java-jdk

%prep

%build
rm -f *.js
cp %_sourcedir/*.js .
chmod 644 *.js
java -jar $YUICOMPRESSOR --type js -o .js:-min.js *.js

%install
mkdir -p %i/data/xregexp
cp *.js %i/data/xregexp
