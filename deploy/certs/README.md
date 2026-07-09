# SSL certificates — HOST level (not Docker)

This app runs on **port 8888** inside Docker, bound to `127.0.0.1` only.

Your **host nginx** (shared with other apps) handles HTTPS on ports 80/443
and proxies to this app at `http://127.0.0.1:8888`.

Use `deploy/host-nginx-snippet.conf` on the server.

Certbot on host:
```bash
sudo certbot certonly --nginx -d winningblueprints.com -d www.winningblueprints.com
sudo nginx -t && sudo systemctl reload nginx
```

Do NOT place certs in this folder for Docker — they are not used anymore.
