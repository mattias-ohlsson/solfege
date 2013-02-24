Name:		solfege
Version:	3.20.7
Release:	3%{?dist}
Summary:	Music education software

Group:		Applications/Multimedia
License:	GPLv3
URL:		http://www.solfege.org/
Source0:	http://downloads.sourceforge.net/solfege/%{name}-%{version}.tar.gz
# Fix startup issue on F17+ (BZ 832764):
# Correctly determine the PREFIX even if solfege is executed as /bin/solfege
Patch0:		solfege-3.20.6-prefix.patch

BuildRequires:	python2-devel
BuildRequires:	texinfo, swig, gettext, docbook-style-xsl 
BuildRequires:	pygtk2-devel >= 2.12, libxslt
BuildRequires:	swig, txt2man
BuildRequires:	desktop-file-utils, gettext

Requires:	timidity++
Requires:	pygtk2 >= 2.12

%description
Solfege is free music education software. Use it to train your rhythm, 
interval, scale and chord skills. Solfege - Smarten your ears!

%prep
%setup -q
%patch0 -p1 -b .prefix

#preserve timestamps
%{__sed} -i.stamp -e 's|shutil\.copy|shutil.copy2|' tools/pcopy.py

%build
export INSTALL="%{__install} -c -p"
#override hardocded path
%configure --enable-docbook-stylesheet=`ls %{_datadir}/sgml/docbook/xsl-stylesheets-1.*/html/chunk.xsl`
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

#permissions
%{__chmod} 755 $RPM_BUILD_ROOT%{_libdir}/solfege/*.so
%{__chmod} 755 $RPM_BUILD_ROOT%{_datadir}/solfege/solfege/_version.py

#Change encoding to UTF-8
for f in AUTHORS README ; do
	iconv -f ISO-8859-15 -t UTF-8 $f > ${f}.tmp && \
		%{__mv} -f ${f}.tmp ${f} || \
		%{__rm} -f ${f}.tmp
done

%find_lang %{name}

desktop-file-install --delete-original \
%if 0%{?fedora} && 0%{?fedora} < 19
	--vendor fedora \
%endif
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--remove-category Application \
	$RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%files -f %{name}.lang
%doc README AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/solfege/
%{_datadir}/solfege/
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_mandir}/man?/*

%changelog
* Sun Feb 24 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.20.7-3
- Remove --vendor from desktop-file-install. https://fedorahosted.org/fesco/ticket/1077

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 07 2012 Christian Krause <chkr@fedoraproject.org> - 3.20.7-1
- Update to new upstream release (BZ 880539)

* Sun Sep 02 2012 Christian Krause <chkr@fedoraproject.org> - 3.20.6-2
- Add patch to fix startup issue on F17+ (BZ 832764)

* Sat Jul 21 2012 Christian Krause <chkr@fedoraproject.org> - 3.20.6-1
- Update to new upstream release (BZ 834200)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Christian Krause <chkr@fedoraproject.org> - 3.20.3-1
- Update to new upstream release (BZ 748133)

* Tue Oct 11 2011 Christian Krause <chkr@fedoraproject.org> - 3.20.3-1
- Update to new upstream release (BZ 741233)

* Mon Sep 12 2011 Christian Krause <chkr@fedoraproject.org> - 3.20.2-1
- Update to new upstream release (BZ 737498)

* Sat Sep 10 2011 Christian Krause <chkr@fedoraproject.org> - 3.20.1-2
- Remove superfluous Requires: gnome-python2-gtkhtml2

* Sun Jul 24 2011 Christian Krause <chkr@fedoraproject.org> - 3.20.1-1
- Update to new upstream release (BZ 720301)

* Sat Jun 18 2011 Christian Krause <chkr@fedoraproject.org> - 3.20.0-1
- Update to new upstream release (BZ 713414)
- Remove upstreamed patches
- Minor spec file cleanup

* Mon May 30 2011 Christian Krause <chkr@fedoraproject.org> - 3.18.8-1
- Update to new upstream release (BZ 707534)
- Minor spec file cleanup

* Sun Mar 06 2011 Christian Krause <chkr@fedoraproject.org> - 3.18.7-3
- Remove superfluous dependency to esound (BZ 678361)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Christian Krause <chkr@plauener.de> - 3.18.7-1
- Update to new upstream release (BZ 648180)

* Wed Oct 27 2010 Christian Krause <chkr@fedoraproject.org> - 3.18.6-1
- Update to new upstream release (BZ 643606)
- Remove upstreamed patch

* Sun Oct 10 2010 Christian Krause <chkr@fedoraproject.org> - 3.18.3-1
- Update to new upstream release (BZ 636475)
- Update patch to fix the build problem with swig 2.0

* Sat Jul 24 2010 Christian Krause <chkr@fedoraproject.org> - 3.16.4-1
- Update to new upstream release (BZ 617836)
- Add patch to fix a build problem

* Wed May 19 2010 Christian Krause <chkr@fedoraproject.org> - 3.16.3-1
- Update to new upstream release

* Sun Apr 18 2010 Christian Krause <chkr@fedoraproject.org> - 3.16.1-1
- Update to new upstream release

* Fri Apr 02 2010 Christian Krause <chkr@fedoraproject.org> - 3.16.0-1
- Update to new upstream release
- Remove patch to fix python's search path, solfege uses absolute
  imports now

* Sun Mar 07 2010 Christian Krause <chkr@fedoraproject.org> - 3.14.11-1
- Update to new upstream release
- Remove upstreamed patch
- Use timitidy as default
- Add patch to remove /usr/bin from python's search path to avoid crash
  on startup if package mpich2 is installed

* Sun Feb 07 2010 Christian Krause <chkr@fedoraproject.org> - 3.14.10-1
- Update to new upstream release
- Some spec file cleanup
- Add minor patch to fix a problem with the default config (programs and
  their parameters are now stored in separate config entries)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.14.2-1
- New upstream release
- No-X patch merged upstream, remove it.

* Sat Apr 11 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 3.14.1-2
- Don't depend on lilypond

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
