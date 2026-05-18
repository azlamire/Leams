CONFIG ?= ./config.cue
SEC_CONFIG ?= ./config.dev.env
SERVICE_ENVS = $(shell find . -type f -name "*.tmpl*" ! -path "*node_modules*" ! -path "*.venv*" ! -path "*local*" ! -path "*nginx.conf*" ! -path "*nginx.ssl*")

define check_bin
  $(foreach dep,$(1),command -v $(dep) >/dev/null || { echo '$(dep) not found. Please download it.' >&2; exit 1; };)
endef
define loadenv
	set -a && . $(CONFIG) && set +a
endef

proj_path:
	@path_in=$$(grep 'PROJ_DIR' $(CONFIG) | sed -e 's/\//\\\//g'); \
	path_now=$$(pwd | sed -e 's/\//\\\//g'); \
	sed -i "s/$$path_in/PROJ_DIR=$$path_now/" $(CONFIG); \
	echo 'export SOME_ENV=someTest'

nginx_cl:
	@first=$$(grep "set_real_ip_from" $$PROJ_DIR/./infra/nginx/deploy/nginx.conf.template | \
		sed -e 's/^[[:space:]]*//' \
		-e "s/set_real_ip_from //" \
		-e 's/\//\\\//g'); \
	second=$$(curl -s https://www.cloudflare.com/ips-v6 https://www.cloudflare.com/ips-v4 | \
		sed -e 's/\//\\\//g' | \
		tr '\n' ' '); \
	sed -i "s/$$first/$$second;/" ./infra/nginx/deploy/nginx.conf.template

# This creates selfsigned key and certificate for https but unsecure so only for dev
openssl: proj_path
	$(call check_bin,openssl)
	$(loadenv) && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $$PROJ_DIR/infra/nginx/local/nginx-selfsigned.key -out $$PROJ_DIR/infra/nginx/local/nginx-selfsigned.crt

# Replace *.temp file to their substituted versions
replace: proj_path
	@$(call check_bin, gomplate cue)
	@for file in $(SERVICE_ENVS); do \
		dest=$$(echo $$file | sed 's/\.tmpl//'); \
		cue export $(CONFIG) --out yaml | gomplate -d "config=stdin:///?type=application/yaml" -f $$file -o $$dest; \
	done

# Like openssl but creates official letsencrypt key and certficate. This for production
encrypt: replace
	@$(call check_bin,docker)
	docker compose -f compose.letsencrypt.yaml \
		--env-file $(CONFIG) \
		up --force-recreate --build --abort-on-container-exit 

pre_ansible: replace
	cue export config.cue --out yaml > ./infra/ansible/config.yaml
	docker compose up pre_ansible --force-recreate

launch: replace 
	@$(call check_bin,docker)
	docker compose --env-file $(CONFIG) up --force-recreate --build

back_check:
	# NOTE: Every new line new shell --> new env
	@$(call check_bin,docker)
	$(loadenv) && docker compose run --build $$COMPOSE_BACKEND_NAME uv run ruff check .

front_check: proj_path
	@$(call check_bin,docker)
	$(loadenv) && docker run --rm \
		-v $$PROJ_DIR/frontend:/app \
		-w /app \
		oven/bun:alpine \
		sh -c "bun install && bunx --bun @biomejs/biome check ./src/"

deploy: nginx_cl encrypt launch

all_check: back_check front_check

.PHONY: replace openssl encrypt compose-up back_check deploy back_check front_check all_check nginx_cl proj_path
