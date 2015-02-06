%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define develname %mklibname -d %name

Summary: Development environment
Name: openldev
Version: 1.0
Release: 9
License: GPLv2+
Group: Development/Other
URL: http://www.openldev.org/
Source0: %{name}-%{version}.tar.bz2
Patch0: openldev-1.0-gcc43.patch
Patch1: openldev-1.0-gcc44.patch
BuildRequires: pkgconfig(gtksourceview-1.0)
BuildRequires: libglade2.0-devel
BuildRequires: vte-devel
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libgnomeprint-2.2)
BuildRequires: pkgconfig(libgnomeprintui-2.2)
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(libgnomeuimm-2.6)
BuildRequires: pkgconfig
BuildRequires: imagemagick
BuildRequires: chrpath
BuildRequires: desktop-file-utils

%description
OpenLDev is a development environment that provides a graphical
front-end to Linux compilers such as gcc. It includes the basic
essentials needed by a Linux programmer. It is a graphical
interface to the collection of command line programming tools
available for Linux and Unix systems.

%package -n %{lib_name}
Summary:        Openldev library
Group:          Development/Other
Obsoletes:	%{_lib}openldev1.0

%description -n %{lib_name}
This is a library used by Openldev.

%package -n %{develname}
Summary:        Development files for GCompris
Group:          Development/Other
Requires:       %{lib_name} = %{version}
Provides:       lib%{name}-devel = %{EVRD}
Provides:       %{name}-devel = %{EVRD}
Obsoletes:	%{_lib}openldev1.0-devel

%description -n  %{develname}
Development file for Openldev.

%prep
%setup -q -n %{name}
%patch0 -p0
%patch1 -p0

%build
%configure2_5x
%make

%install
%makeinstall_std
# to remove binary-or-shlib-defines-rpath rpmlint error
chrpath -d $RPM_BUILD_ROOT/%{_bindir}/%{name}
# to remove script-without-shellbang rpmlint error
chmod ugo-x $RPM_BUILD_ROOT/%{_libdir}/*.la
chmod ugo-x $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.la

# menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Development-DevelopmentEnvironments" \
  --add-category="Development" \
  --add-category="IDE" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# icons
mkdir -p %{buildroot}%{_liconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
convert -geometry 48x48 pixmaps/%{name}96.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}96.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}96.png %{buildroot}%{_miconsdir}/%{name}.png

# remove unneeded files
rm -rf $RPM_BUILD_ROOT/%{_defaultdocdir}

# fix warnings
perl -pi -e "s/\r\n/\n/" NEWS README

# change mode for script (add executable mode)
chmod +x %{buildroot}%{_datadir}/%{name}/templates/*.pl

%files 
%defattr(644,root,root,755)
%doc README COPYING AUTHORS NEWS TODO ChangeLog INSTALL
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_datadir}/applications/openldev.desktop
%{_mandir}/*/*
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_libdir}/%{name}/makefileeditor.plugin
%{_libdir}/%{name}/insertinfo.plugin

%files -n %{lib_name}
%{_libdir}/*.so.%{lib_major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/%{name}/*.so


%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-6mdv2011.0
+ Revision: 613538
- rebuild

* Tue Apr 20 2010 Funda Wang <fwang@mandriva.org> 1.0-5mdv2010.1
+ Revision: 536918
- fix build with gcc 4.4

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Nov 11 2008 Funda Wang <fwang@mandriva.org> 1.0-4mdv2009.1
+ Revision: 302032
- add gcc 4.3 patch
- new devel package policy
- fix libname

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.0-2mdv2008.1
+ Revision: 171009
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jun 29 2007 trem <trem@mandriva.org> 1.0-1mdv2008.0
+ Revision: 45886
- new release 1.0


* Thu Aug 31 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.1-5mdv2007.0
- fix typo in menu

* Mon Aug 28 2006 Emmanuel Andry <eandry@mandriva.org> 0.6.1-4mdv2007.0
- fix xdg mimetypes

* Mon Aug 14 2006 Emmanuel Andry <eandry@mandriva.org> 0.6.1-3mdv2007.0
- xdg menu

* Sun Jul 30 2006 Emmanuel Andry <eandry@mandriva.org> 0.6.1-2mdv2007.0
- rebuild

* Tue May 30 2006 Emmanuel Andry <eandry@mandriva.org> 0.6.1-1mdk
- 0.6.1

* Thu Apr 27 2006 trem <trem@mandriva.org> 0.6.0-1mdk
- 0.6.0

* Tue Apr 04 2006 Jerome Soyer <saispo@mandriva.org> 0.5.6-1mdk
- New release 0.5.6

* Mon Mar 13 2006 trem <trem@mandriva.org> 0.5.5-1mdk
- 0.5.5

* Wed Feb 22 2006 Nicolas L�ureuil <neoclust@mandriva.org> 0.5.4-2mdk
- Add BuildRequires

* Sun Feb 19 2006 trem <trem@mandriva.org> 0.5.4-1mdk
- 0.5.4

* Mon Feb 06 2006 trem <trem@mandriva.org> 0.5.3-1mdk
- 0.5.3

* Sun Jan 15 2006 trem <trem@mandriva.org> 0.5.2-1mdk
- 0.5.2
- add lib package

* Sat Dec 10 2005 Couriousous <couriousous@mandriva.org> 0.5.1-1mdk
- Reenable parallel build
- From Trem <trem@zarb.org> :
	- 0.5.1
	- Fix BuildRequires

* Mon Nov 21 2005 Couriousous <couriousous@mandriva.org> 0.5.0-1mdk
- Disable parallel build as NFS sux
- From Trem <trem@zarb.org> :
	- Initial build

