Name:           desktop-effects
Version:        0.8.4
Release:        7%{?dist}
Summary:        Switch GNOME window management and effects

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://git.fedoraproject.org/git/desktop-effects.git
Source0:        https://fedorahosted.org/released/desktop-effects/%{name}-%{version}.tar.bz2
Source1:        desktop-effects-icons.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  desktop-file-utils
BuildRequires:  GConf2-devel
BuildRequires:  gtk2-devel
BuildRequires:  intltool
BuildRequires:  libglade2-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  mesa-libGL-devel

# https://bugzilla.redhat.com/show_bug.cgi?id=589189
# Changes (or equivalent) are already committed upstream
Patch1: desktop-effects-0.8.4-translation.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=532618
# Cherry-picked from upstream
Patch2: Connect-to-signals-after-calling-update_sensitive.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=574500
Patch3: Explicit-set-background-and-border-colors.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=533807
Patch4: Fix-calling-glXDestroyContext-on-uninitialized.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=555697
Patch5: desktop-effects-0.8.4-ml-translation.patch


Requires:       gnome-session
Requires:       hicolor-icon-theme

%description
desktop-effects provides a preference dialog to allow switching the GNOME
desktop between three different window managers: Metacity (the standard
GNOME 2 window manager), Compiz (offering 3D acceleration and special
effects), and GNOME Shell, which offers a preview of the GNOME 3 user
experience.

%prep
%setup -q -a 1

%patch1 -p1 -b .translation
%patch2 -p1 -b .update-sensitive
%patch3 -p1 -b .border-color
%patch4 -p1 -b .unitialized-context
%patch5 -p2 -b .ml-translation

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT

# Replace the icons with newer versions
rm -rf $RPM_BUILD_ROOT%{_datadir}/icons/hicolor

for i in 16 22 24 32 48 96 ; do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps
    install desktop-effects-icons/desktop-effects$i.png \
            $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/desktop-effects.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/desktop-effects.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/desktop-effects
%{_datadir}/icons/hicolor/*/apps/desktop-effects.png
%{_datadir}/applications/desktop-effects.desktop
%{_datadir}/desktop-effects/

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ] ; then
  /usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ] ; then
  /usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi

%changelog
* Tue Aug 10 2010 Owen Taylor <otaylor@redhat.com> - 0.8.4-7
- Add translation update for ml
  Resolves: bug 555697

* Tue Jul 13 2010 Owen Taylor <otaylor@redhat.com> - 0.8.4-6
- Actually apply patch for 533807
  Resolves: bug 607280

* Tue May  4 2010 Owen Taylor <otaylor@redhat.com> - 0.8.4-5
- Add translation updates for fr,ko,it
  Resolves: bug 589189
- Add patch fixing problems initializing wobbly-windows state
  Resolves: bug 591541
- Add patches fixing crashes in OpenGL detection
  Resolves: bug 607280

* Tue May  4 2010 Owen Taylor <otaylor@redhat.com> - 0.8.4-3
- Add new icons by Lapo Calamandrei
  Resolves: bug 588824

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.4-2.1
- Rebuilt for RHEL 6

* Fri Sep 18 2009 Owen Taylor <otaylor@redhat.com> - 0.8.4-1
- Update to 0.8.4 (fixes #524102)

* Mon Sep 14 2009 Owen Taylor <otaylor@redhat.com> - 0.8.3-1
- Update to 0.8.3 (translations)

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 0.8.2-2
- Add missing BuildRequires on mesa-libGL-devel

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Mon Aug 24 2009 Owen Taylor <otaylor@redhat.com> - 0.8.1-1
- Update to 0.8.1 (fixes leftover debugging hack)

* Mon Aug 24 2009 Owen Taylor <otaylor@redhat.com> - 0.8.0-2
- Add dist to release
- BuildRequire intltool and desktop-file-utils
- Point Source: at https://fedorahosted.org/released

* Sun Aug 23 2009 Owen Taylor <otaylor@redhat.com> - 0.8.0-1
- Initial version

