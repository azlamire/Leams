#!/usr/bin/env bash
set -e
source /etc/os-release
echo -n "Do you want to use Docker (1) or Podman (2): "
read user_input
case "$user_input" in
    1) container_cmd="docker" ;;
    2) container_cmd="podman" ;;
    *)
      echo "Invalid choice. Please enter 1 for Docker or 2 for Podman."
      exit 1
      ;;
esac
if [[ $OSTYPE == "linux-gnu" ]]; then
  if ! command -v "$container_cmd" >/dev/null 2>&1; then 
    echo "$container_cmd is not installed. Installing..."
    case $ID in
      nixos)
        echo -n "$container_cmd can be installed imperatively or declaratively"
        echo -n "If you want that it would be installed declaratively make sure that a user has access to /etc/nixos"
        echo -n "Declaratively (1) or imperatively (2)? "
        read nixos_choice
        case $nixos_choice in 
          1)
            sed -i '/systemPackages/a $container_cmd' /etc/nixos/configuration.nix
            ;;
          2)
            nix run nixpkgs\#$container_cmd compose up 
            ;;
          *)
            echo "Unfortunately we don't have a third option in NixOS :("
            exit 1
          ;;
        esac
        ;;
      arch | manjaro | garuda | endevouros)
        sudo pacman -S $container_cmd
        ;;
      ubuntu | debian | mint | popos | elementaryos | zorinos | kali | pclinux | parrot | mxlinux | bodhi | deepin | peppermint | tuxedo | voyager | antix)
        sudo apt install $container_cmd
        ;;
      alpine)
        apk add $container_cmd
        ;;
      solus )
        sudo eopkgs install -y $container_cmd
        ;;
      slackware)
        sudo slackpkg install $container_cmd
        ;;
      gentoo)
        "I will add when will be on gentoo" 
        ;;
      fedora | almalinux | rocky )
        sudo dnf install -y $container_cmd
        ;;
      centos)
        sudo yum install -y $container_cmd
        ;;
      opensuse)
        sudo zypper install -y $container_cmd
        ;;
      void)
        sudo xbps install -y $container_cmd
        ;;
      *)
        echo "Please install $container_cmd manually or create an issue for support in https://github.com/azlamire/Leams/issues"
        exit 1
        ;;
    esac
    echo "$container_cmd installed successfully!"
  else
    echo "$container_cmd found in the system"
  fi
elif [[ $OSTYPE == "macos" ]]; then
  brew install $container_cmd
fi
$container_cmd compose up
