#!/usr/bin/env bash
# Provisions the intentionally-vulnerable lab services.
# Every weakness here is deliberate and documented in exercises/07-file-uploads.md.
set -euo pipefail

apt-get update -qq
apt-get install -y -qq nginx python3-pip sqlite3 cron >/dev/null

# --- 1. a "company portal" with a directory-listing upload folder ----------
mkdir -p /var/www/html/uploads
cat > /var/www/html/index.html <<'HTML'
<h1>ACME internal portal</h1>
<p>training lab — see exercises/05-web-basics.md</p>
<a href="/uploads/">uploads</a>
HTML
chown -R www-data:www-data /var/www/html/uploads
chmod 777 /var/www/html/uploads        # deliberate: world-writable upload dir

# --- 2. an over-permissive sudo rule (privesc exercise 10) -----------------
echo "student ALL=(ALL) NOPASSWD: /usr/bin/find" >> /etc/sudoers.d/lab
echo "student ALL=(ALL) NOPASSWD: /usr/bin/vim" >> /etc/sudoers.d/lab

# --- 3. a weak "service" a student can analyse (exercise 09) ---------------
useradd -m -s /bin/bash svc-backup || true
echo "svc-backup:Summer2023!" | chpasswd     # deliberate: weak password

# --- 4. a log file that the parsing capstone reads -------------------------
cat > /var/log/lab-access.log <<'LOG'
10.0.2.15 - - [24/Nov/2026:10:01:11 +0000] "GET /login HTTP/1.1" 200 512
10.0.2.99 - - [24/Nov/2026:10:01:12 +0000] "POST /login HTTP/1.1" 401 96
10.0.2.99 - - [24/Nov/2026:10:01:13 +0000] "POST /login HTTP/1.1" 401 96
10.0.2.99 - - [24/Nov/2026:10:01:14 +0000] "POST /login HTTP/1.1" 200 512
LOG

systemctl enable --now nginx
echo "lab ready — read exercises/01-recon.md to begin"
