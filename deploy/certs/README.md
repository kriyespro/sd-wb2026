# SSL certificates for nginx

Place your TLS certificates here before starting Docker:

- `fullchain.pem` — full certificate chain
- `privkey.pem` — private key

## Let's Encrypt (recommended)

On the server (with ports 80/443 open):

```bash
# Stop nginx container first if running
sudo apt install certbot
sudo certbot certonly --standalone -d winningblueprints.com -d www.winningblueprints.com

# Copy certs into this folder
sudo cp /etc/letsencrypt/live/winningblueprints.com/fullchain.pem deploy/certs/
sudo cp /etc/letsencrypt/live/winningblueprints.com/privkey.pem deploy/certs/
sudo chmod 644 deploy/certs/fullchain.pem
sudo chmod 600 deploy/certs/privkey.pem
```

Renewal: set up a cron job or use certbot renew, then restart nginx container.

## IP access (159.195.52.197)

The nginx config includes the server IP in `server_name`. Ensure your cert covers the domain; IP-only HTTPS may need a separate cert or SAN entry.
