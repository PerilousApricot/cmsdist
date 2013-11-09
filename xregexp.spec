### RPM external xregexp 1.5.0
## NOCOMPILER

Source0: http://xregexp.com/xregexp.js
Source1: http://xregexp.com/addons/unicode/unicode-base.js
Source2: http://xregexp.com/addons/unicode/unicode-categories.js
Source3: http://xregexp.com/addons/unicode/unicode-scripts.js
Source4: http://xregexp.com/addons/unicode/unicode-blocks.js
Source5: http://xregexp.com/addons/matchrecursive.js
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
