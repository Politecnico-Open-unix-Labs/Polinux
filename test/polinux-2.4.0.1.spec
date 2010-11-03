# vim: set fileencoding=ascii :
#
# polinux-2.4.0.1
# 
# polinux is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# polinux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

Name:		polinux
Version:	2.4.0.1
Release:	1%{?dist}
Summary:	unofficial Linux distribution for students at Politecnico di Milano    

Group:		User Interface/Desktops
License:	GPL
URL:		http://www.poul.org/
BuildArch:	noarch	    
#Requires:	polinux-gnome-wifi | polinux-kde-wifi
Requires:	polinux-geo polinux-programming polinux-chemicals polinux-network
Requires:	polinux-electronics polinux-math polinux-artwork polinux-architectural 
Requires:	polinux-extra
Requires:	gnupg seahorse seahorse-plugins
Requires:	openoffice.org-gnome
Requires:	language-pack-it language-pack-gnome-it language-support-it

%description
This is a RPM port of Polinux, "a GNU/Linux distribution made by POuL, 
Politecnico Open unix Labs, as a way for giving Politecnico di Milano students
the possibility of trying Linux without necessarily install it or become less
productive. It can be used as a replacement for many Microsoft Windows based
programs used in many university courses."

%files

%package architectural
Summary:	Architectural dependencies for Polinux.
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	blender qcad

%description architectural
This metapackage includes:
	*blender
	*qcad

%files architectural

%package chemicals
Summary:	Chemicals dependencies for Polinux.
Group:		Applications/Scientific
Requires:	%{name} = %{version}-%{release}
Requires:	kalzium gromacs avogadro

%description chemicals
This metapackage includes:
	*kalzium
	*gromacs
	*avogadro

%files chemicals

%package courses
Summary:	Software required for POlinux courses 2009 by POuL.
Group:		Applications/Courses
Requires:	%{name} = %{version}-%{release}
Requires:	thunderbird enigmail thunderbird-locale-it thunderbird-gnome-support
Requires:	timidity rosegarden amarok tuxguitar audacity mplayer mencoder
Requires:	hydrogen ardour jackd
Requires:	rsync testdisk mondo ddrescue chntpw
Requires:	gnupg seahorse seahorse-plugins
Requires:	virtualbox-ose wine

%description courses
This metapackage includes various pieces of software needed for Polinux courses:
	*thunderbird with italian localization
	*enigmail
	*timidity
	*rosegarden
	*amarok
	*tuxguitar
	*audacity
	*mplayer
	*mencoder
	*gnupg
	*seahorse and plugins
	*virtualbox-ose
	*wine

%files courses

%package electronics
Summary:	Electronics dependencies for Polinux.
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	geda geda-doc geda-examples oregano

%description electronics
This metapackage includes:
	*geda with docs and examples
	*oregano

%files electronics

%package extras
Summary:	Extra packages for Polinux.
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	texlive-full lyx
Requires:	virtualbox-ose virtualbox-ose-guest-utils
Requires:	wine freemind

%description extras
This metapackage includes extra stuff that is not included in main distribution:
	*texlive-full and lyx
	*virtualbox-ose and utils
	*wine
	*freemind

%files extras

%package geo
Summary:	Geo dependencies for Polinux.
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	celestia grass stellarium

%description geo
This metapackage includes:
	*celestia
	*grass
	*stellarium

%files geo

%package math
Summary:	Math dependencies for Polinux.
Group:		Applications/Scientific
Requires:	%{name} = %{version}-%{release}
Requires:	octave3.0 octave3.0-doc
Requires:	octave-audio octave-bioinfo octave-communications octave-financial
Requires:	octave-ga octave-image octave-linear-algebra octave-odebvp
Requires:	octave-odepkg octave-signal octave-statistics
Requires:	gnuplot scilab scilab-doc
Requires:	maxima wxmaxima r-recommended python-scipy python-matplotlib
Requires:	freefem freemat speedcrunch labplot elmer

%description math
This metapackage includes:
	*octave with lots of modules
	*gnuplot
	*scilab
	*wxmaxima
	*scipy
	*freefm
	*speedcrunch
	*labplot
	*elmer

%files math

%package network
Summary:	Network dependencies for Polinux.
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
Requires:	wireshark filezilla
#Requires:	firebug firefox-webdeveloper

%description network
This metapackage includes:
	*wireshark
	*filezilla

%files network

%package programming
Summary:	Programming dependencies for Polinux.
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	default-jdk eclipse anjuta
Requires:	mysql-client mysql-server
Requires:	rapidsvn subversion
Requires:	flex flex-doc bison bison-do
#Requires:	manpages-dev

%description programming
This metapackage includes:
	*eclipse
	*anjuta
	*mysql
	*subversion
	*flex, bison and related docs

%files programming

%changelog
* Fri Jan 22 2010 Stefano Sanfilippo  2.4.0.1
- Initial, untested RPM release
