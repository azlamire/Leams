#!/usr/bin/env bash
grep 'PROJ_DIR' $(ENVFILE) | sed -e 's/\//\\\//g'); \
	path_now=$$(pwd | sed -e 's/\//\\\//g'); \
	sed -i "s/$$path_in/PROJ_DIR=$$path_now/" $(ENVFILE)

