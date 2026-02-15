#!/usr/bin/env bash
source /etc/os-release

if ! command -v docker >/dev/null 2>&1 || command -v podman > /dev/null 2>&1; then
  echo "Docker not found"
  case $ID in
    nixos)
      ;;
    arch | manjaro | garuda)
      sudo pacman -S docker
      ;;
    ubuntu | debian | mint | popos | elementaryos | zorinos | kali | pclinux | parrot | mxlinux | bodhi | deepin | peppermint | tuxedo | voyager | antix)
      sudo apt install docker
      ;;
    solus )
      sudo eopkgs install -y docker
      ;;
    slackware)
      sudo slackpkg install docker
      ;;
    gentoo)
      portage
      ;;
    fedora | almalinux | rocky )
      sudo dnf install -y docker
      ;;
    centos)
      sudo yum install -y docker
      ;;
    opensuse)
      sudo zypper install -y docker
      ;;
    void)
      sudo xbps install -y docker
      ;;
    *)
      echo "I'm sorry please create issues for other distro"
  esac
else
  command docker compose up
fi
