### RPM external libxml2 2.9.2
%define downloadv %(echo %{realversion} | cut -d"_" -f1)
Source: ftp://xmlsoft.org/%{n}/%{n}-%{downloadv}.tar.gz
%define online %(case "%{cmsplatf}" in (*onl_*_*) echo true;; (*) echo false;; esac)
%define strip_files %{i}/lib/lib* %{i}/bin/{xmlcatalog,xmllint}
%define drop_files %{i}/share/{man,doc,gtk-doc}

%if "%{online}" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif

%prep
%setup -n %{n}-%{downloadv}

%build
./configure --disable-static --prefix=%{i} --build="%{_build}" \
            --host="%{_host}" --with-zlib="${ZLIB_ROOT}" --without-python
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
rm -rf %{i}/lib/*.{l,}a

%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/xml2Conf.sh
