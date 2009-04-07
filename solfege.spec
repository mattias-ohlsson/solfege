Name:		solfege
Version:	3.14.1       
Release:	2%{?dist}
Summary:	Music education software

Group:		Applications/Multimedia
License:	GPLv3
URL:		http://www.solfege.org/
Source0:	http://dl.sourceforge.net/solfege/%{name}-%{version}.tar.gz
Source1:	solfege.sh.in
#don't require X to build from Tom Cato Amundsen, to be merged upstream
Patch0:         solfege-%{version}-no-x.patch
#make sure desktop file is sane, don't use extension without path in Icon=
Patch1:         solfege-%{version}-desktop.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	texinfo, swig, gettext, docbook-style-xsl 
BuildRequires:	pygtk2-devel >= 2.12, libxslt
BuildRequires:  lilypond, swig
BuildRequires:	desktop-file-utils, gettext

Requires:	timidity++, lilypond
Requires:       gnome-python2-gtkhtml2, esound
Requires:	pygtk2 >= 2.12

%description
Solfege is free music education software. Use it to train your rhythm, 
interval, scale and chord skills. Solfege - Smarten your ears!

%prep
%setup -q
%patch0 -p0
%patch1 -p0

#preserve timestamps
%{__sed} -i.stamp -e 's|shutil\.copy|shutil.copy2|' tools/pcopy.py

#fix permissios for debuginfo package
chmod 0755 $RPM_BUILD_DIR/%{name}-%{version}/src/_version.py

%build
export INSTALL="%{__install} -c -p"
#override hardocded path
%configure --enable-docbook-stylesheet=`ls %{_datadir}/sgml/docbook/xsl-stylesheets-1.*/html/chunk.xsl`
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%{__mkdir} $RPM_BUILD_ROOT%{_libexecdir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/solfege $RPM_BUILD_ROOT%{_libexecdir}/solfege-bin
#permissions
%{__chmod} 755 $RPM_BUILD_ROOT%{_libdir}/solfege/*.so

#Change encoding to UTF-8
for f in AUTHORS README ; do
        iconv -f ISO-8859-15 -t UTF-8 $f > ${f}.tmp && \
                %{__mv} -f ${f}.tmp ${f} || \
                %{__rm} -f ${f}.tmp
done

#Setup wrapper script
%{__install} -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/solfege

%find_lang %{name}

desktop-file-install --vendor fedora --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/solfege
%{_datadir}/solfege/
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_mandir}/man?/*


%changelog
* Wed Apr 7 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.14.1-2
- Update launcher script to use esdcompat and not esd

* Wed Apr 7 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.14.1-1
- New upstream release
- Add patch to not require X to build
- Add patch to fix desktop file, don't use extensions without path in Icon=
- Add lilypond dependency
- Make sure permissions in debuginfo are sane

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.10.4-2
- Rebuild for Python 2.6

* Tue Mar 18 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.10.4-1
- New bugfix release

* Tue Mar 18 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.10.3-1
- New release

* Sun Mar 16 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.10.2-5
- Clean up docbook path override

* Sun Mar 16 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.10.2-1
- New major release
- Update license to GPLv3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.0-2
- Autorebuild for GCC 4.3

* Mon Jun 04 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.8.0-1
- New major release
* Sun Mar 11 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.5-1
- Update to 3.6.5
* Sun Dec 31 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-8
- Rebuild for new pygtk2-devel

* Wed Dec 20 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-6
- Fix charset conversion
- Remove Application category from desktop file
- Fix changelog

* Tue Dec 19 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-5
- Move original binary to %%{_libexecdir}
- Remove X-Fedora Category from meny entry
- Add pygtk2 Requires
- Replace libxlst-devel BuildRequires with libxlst
- Keep timestamps for image files 
- Convert AUTHORS and README from iso8859 to UTF-8 

* Fri Dec 15 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-4
- Fix permissions issue in wrapper script
- Fix debuginfo package
- Fix indentation

* Fri Dec 15 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-3
- Change permissions

* Thu Dec 14 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-2
- Use install to install wrapper script
- Improvements to wrapper script

* Thu Dec 14 2006 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 3.6.4-1
- Initial build
