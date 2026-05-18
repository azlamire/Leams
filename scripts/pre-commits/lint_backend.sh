#!/usr/bin/env bash
set -e
source /etc/os-release
cd $PROJ_DIR/backend
case $ID in
	nixos)
		nix develop . --command uv run ruff check . --fix
		;;
	ubuntu | debian | mint | popos | elementaryos | zorinos | kali | pclinux | parrot | mxlinux | bodhi | deepin | peppermint | tuxedo | voyager | antix)
		uv run ruff check . --fix
		;;
	*)
		docker run -it --rm -v ".":/app -w /app astral/uv:bookworm-slim uv sync && uv uv run ruff check .
		;;
	esac
	;;

