%define	name	rocksndiamonds
%define version 3.2.6.1
%define rel	5
%define release %mkrel %rel
%define	Summary	A boulderdash like game

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
Source0:	http://www.artsoft.org/RELEASES/unix/rocksndiamonds/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
URL:		http://www.artsoft.org/rocksndiamonds/
License:	GPL
Group:		Games/Arcade
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	libsmpeg-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a nice little game with color graphics and sound for your
Unix system.

If you know the game "Boulderdash" (Commodore C64) or "Emerald Mine"
(Amiga) or "Supaplex" (PC), you know what "ROCKS'N'DIAMONDS" is about.

%prep
%setup -q
perl -pi -e 's!.*RO_GAME_DIR\s*=.*!RO_GAME_DIR = %{_gamesdatadir}/%{name}!; s!.*RW_GAME_DIR\s*=.*!RW_GAME_DIR = /var/games/%{name}!' Makefile

%build
make sdl OPTIONS="%optflags" CC="gcc %ldflags"

%install
rm -rf %{buildroot}

# Install stuff
mkdir -p %{buildroot}%{_gamesbindir} %{buildroot}%{_gamesdatadir}/%{name} %{buildroot}%{_mandir}/man1
cp -a %{name} %{buildroot}%{_gamesbindir}/%{name}
cp -a graphics levels sounds music %{buildroot}%{_gamesdatadir}/%{name}
cp -a *.1 %{buildroot}%{_mandir}/man1

# Install scores
mkdir -p %{buildroot}/var/games/%{name}
install -d %{buildroot}/var/games/%{name}/scores


# Menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Rocks n Diamonds
Comment=%Summary
Exec=%_gamesbindir/%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF


# Icon
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%pre
if [ -d %{_gamesdatadir}/%{name}/scores ]; then
	mkdir -p /var/games/%{name}/
	mv %{_gamesdatadir}/%{name}/scores /var/games/%{name}/
fi

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COPYING
%attr(0755,root,root) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%_datadir/applications/mandriva*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man?/*
/var/games/%{name}
