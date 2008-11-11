%define name openldev
%define version 1.0
%define release %mkrel 4

%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define develname %mklibname -d %name

Summary: Development environment
Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2+
Group: Development/Other
URL: http://www.openldev.org/
Source0: %{name}-%{version}.tar.bz2
Patch0: openldev-1.0-gcc43.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libgtksourceview-1.0-devel
BuildRequires: libglade2.0-devel
BuildRequires: vte-devel
BuildRequires: libxml2-devel
BuildRequires: libgnomeprint-devel
BuildRequires: libgnomeprintui-devel
BuildRequires: libGConf2-devel
BuildRequires: libgnomeuimm-devel
BuildRequires: pkgconfig
BuildRequires: ImageMagick
BuildRequires: chrpath
BuildRequires: desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

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
Provides:       lib%{name}-devel = %{version}-%{release} 
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}openldev1.0-devel

%description -n  %{develname}
Development file for Openldev.

%prep
%setup -q -n %{name}
%patch0 -p0

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
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

%if %mdkversion < 200900
%post 
%{update_menus}
%{update_desktop_database}
%endif

%if %mdkversion < 200900
%postun 
%{clean_menus}
%{clean_desktop_database}
%endif

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_libdir}/*.la
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.la
