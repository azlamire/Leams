// config.cue
package config

import "os"
import "strings"

settings: {
  github_id: os.Getenv("GITHUB_ID")
  github_secret: os.Getenv("GITHUB_SECRET")
  
  main_page: "https://\(os.Getenv("DOMAIN_NAME")):\(os.Getenv("NGINX_REVERSE_PORT_HTTPS"))"
  
  broker: "redis://\(os.Getenv("REDIS_NAME")):\(os.Getenv("REDIS_PORT"))/0"
  
  database_url: "postgresql:psycopg://\(os.Getenv("POSTGRES_USER")):\(os.Getenv("POSTGRES_PASSWORD"))@\(os.Getenv("DATABASE_HOST"))/\(os.Getenv("POSTGRES_DB"))"
  
  s3: {
    access_key: os.Getenv("S3_ACCESS_KEY")
    secret_key: os.Getenv("S3_SECRET_KEY")
    endpoint: os.Getenv("S3_ENDPOINT")
    bucket_name: os.Getenv("S3_BUCKET_NAME")
  }
}

_settings: settings & {
  github_id: !=""
  github_secret: !=""
  broker: =~ ^redis://
  database_url: =~ ^postgresql:
}
