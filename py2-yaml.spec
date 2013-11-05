### RPM external py2-yaml 3.09
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source: http://pyyaml.org/download/pyyaml/PyYAML-%realversion.tar.gz
Requires: python libyaml py2-pyrex

%prep
%setup -n PyYAML-%realversion
cat >> setup.cfg <<-EOF
	[build_ext]
	include_dirs = $LIBYAML_ROOT/include
	library_dirs = $LIBYAML_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py --with-libyaml install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;


# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

