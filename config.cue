// WARN: For some distros >1024 is privileged and can't be used for example NixOS

// 1. ОПРЕДЕЛЯЕМ СХЕМУ (ШАБЛОН) ДЛЯ АККАУНТОВ
// Это гарантирует, что мы не опечатаемся в ключах, и задает значения по умолчанию.
#Account: {
	email?:    string
	password?: string // WARN: This field will be deleted after success
	set?:      bool | *false // Значение по умолчанию — false
}

project: {
	dir: "/root/Leams"
	
	accounts: {
		// WARN: Mail is required until make captcha bypassing way to sign in a new mail
		mail: #Account & {
			email: "testtingdd@gmail.com"
			// If password field in comment it's like None and that means that new account will be created
			password: "MYPASSWORD"
		}
		
		vps: #Account & {
			// If email is empty than it will be replaced with mail_acc's
			email:    "testtingdd@gmail.com"
			password: "MYPASSWORD"
			set:      false
		}
		
		domain: #Account & {
			email:    "testtingdd@gmail.com"
			password: "MYPASSWORD"
			set:      false
		}
		
		cloudflare: #Account & {
			email:    "testtingdd@gmail.com"
			password: "MYPASSWORD"
			set:      false
		}
	}
	
	settings: {
		domain:     "leams.tech"
		cloudflare: true
		ip_vps:     "144.31.19.248"
	}
	
	configured: true
}

server: {
	http:  80
	https: 443
}

services: {
	reverse_proxy: {
		name: "reverse_proxy"
		port_http: 80
		port_https: 443
		conf_path: "\(project.dir)/infra/nginx/deploy/nginx.conf.template"
		letsencrypt_certs_path: "\(project.dir)/infra/nginx/deploy/data/certbot/letsencrypt"
		letsencrypt_www_path: "\(project.dir)/infra/nginx/deploy/data/certbot/www"
		cert_path: "/etc/letsencrypt/live/\(project.settings.domain)/fullchain.pem"
		ssl_key_path: "/etc/letsencrypt/live/\(project.settings.domain)/privkey.pem"
	}
	
	frontend: {
		name: "frontend"
		port: 3000
	}
	
	backend: {
		name: "backend"
		port: 8000
		sub:  "api"
	}
	
	database: {
		name: "database"
		port: 5432
		settings: [
			{user: "postgres"},
			{pass: "secret"},
			{host: "database"},
			{db:   "leams"},
		]
	}
	
	redis: {
		name: "redis"
		port: 6379
	}
	
	docs: {
		name: "docs"
		port: 8000
		sub:  "docs"
	}
	
	mobile: {
		name: "mobile"
		port: 3000
	}
	
	stream: {
		name: "stream"
		port: 1935
		sub:  "stream"
	}
}

