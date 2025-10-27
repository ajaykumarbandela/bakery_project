# AWS Free Tier Deployment - Cost-Conscious Guide

## ⚠️ WARNING: AWS Can Charge You Even on Free Tier

While AWS offers a free tier, you CAN get charged if you're not careful. This guide helps you stay within free limits.

---

## 🆓 Free Tier Limits (First 12 Months)

- **EC2**: 750 hours/month of t2.micro or t3.micro (one instance 24/7)
- **EBS**: 30 GB of storage
- **Data Transfer**: 15 GB outbound per month
- **Elastic IP**: Free ONLY when attached to a running instance

---

## 💰 What Will Cost You Money

### Immediate Charges:
- ❌ Elastic Load Balancer ($16-20/month) - **Don't use**
- ❌ RDS Database ($15+/month after free tier) - **Use SQLite instead**
- ❌ NAT Gateway ($32+/month) - **Don't use**
- ❌ Multiple EC2 instances
- ❌ Elastic IP not attached to instance ($3.60/month)

### After 12 Months:
- EC2 t2.micro: ~$8-10/month
- EBS 20GB: ~$2/month
- Data transfer: $0.09/GB after 15GB

---

## 🛡️ How to Avoid Charges

### 1. Set Up Billing Alerts (CRITICAL!)

Before doing ANYTHING else:

1. Go to AWS Console → **Billing Dashboard**
2. Click **Budgets** → **Create budget**
3. Choose **Cost budget**
4. Set amount: **$1** (yes, one dollar!)
5. Set email alerts at:
   - 50% of budget ($0.50)
   - 85% of budget ($0.85)
   - 100% of budget ($1.00)

### 2. Enable Free Tier Usage Alerts

1. AWS Console → **Billing Preferences**
2. Check **"Receive Free Tier Usage Alerts"**
3. Enter your email

### 3. Use Cost Explorer

1. AWS Console → **Cost Explorer**
2. Enable it (might take 24 hours)
3. Check weekly for any unexpected charges

---

## 📝 Deployment Steps (Free Tier Safe)

### Step 1: Launch EC2 Instance

1. AWS Console → EC2 → **Launch Instance**
2. Choose **Ubuntu 22.04 LTS** (Free tier eligible)
3. Instance type: **t2.micro** ✅ (1 vCPU, 1GB RAM)
4. Key pair: Create new or use existing
5. Security group: 
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
6. Storage: **8 GB** (free tier includes 30GB)
7. **Launch instance**

### Step 2: Connect to Instance

```bash
# Download your .pem key file
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-instance-public-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and essentials
sudo apt install python3-pip python3-venv nginx git -y

# Install PostgreSQL (optional, or use SQLite)
# sudo apt install postgresql postgresql-contrib -y
```

### Step 4: Clone and Setup Project

```bash
# Clone your repo
cd /home/ubuntu
git clone https://github.com/ajaykumarbandela/bakery_project.git
cd bakery_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install gunicorn

# Run migrations
cd bakery_project
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
```

### Step 5: Configure Gunicorn

```bash
# Create systemd service
sudo nano /etc/systemd/system/bakery.service
```

Add this content:
```ini
[Unit]
Description=Bakery Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/bakery_project/bakery_project
Environment="PATH=/home/ubuntu/bakery_project/venv/bin"
ExecStart=/home/ubuntu/bakery_project/venv/bin/gunicorn \
          --workers 2 \
          --bind unix:/home/ubuntu/bakery_project/bakery.sock \
          bakery_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl start bakery
sudo systemctl enable bakery
sudo systemctl status bakery
```

### Step 6: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/bakery
```

Add:
```nginx
server {
    listen 80;
    server_name your-instance-public-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/bakery_project/bakery_project;
    }

    location /media/ {
        root /home/ubuntu/bakery_project/bakery_project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/bakery_project/bakery.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/bakery /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Update Django Settings

Add your EC2 public IP to `ALLOWED_HOSTS` in settings.py:
```python
ALLOWED_HOSTS = ['your-ec2-public-ip', 'localhost']
```

Restart:
```bash
sudo systemctl restart bakery
```

---

## 📊 Monitor Your Costs

### Daily Checks (First Week):
1. AWS Console → Billing Dashboard
2. Check "Month-to-Date Spend"
3. Verify it shows $0.00

### Weekly Checks:
1. Review Cost Explorer
2. Check for any unexpected services
3. Verify only t2.micro EC2 is running

### Monthly Checks:
1. Review detailed billing
2. Check free tier usage
3. Delete unused snapshots/volumes

---

## 🚨 If You See Charges

1. **Immediately stop all services**
2. Check what's charging you:
   - AWS Console → Billing → Bills
3. Common culprits:
   - Elastic Load Balancer
   - Multiple EC2 instances
   - RDS database
   - Unattached Elastic IP
4. **Terminate/delete the expensive service**

---

## 🎯 Better Alternative: Use Render (FREE)

Honestly, for a free tier beginner, **Render is much simpler**:

```bash
# No charges, no surprises, no credit card needed
1. Go to render.com
2. Connect GitHub repo
3. Click deploy
4. Done! ✅
```

**AWS is great but:**
- Complex to set up
- Easy to accidentally get charged
- Free tier expires after 12 months
- Requires constant monitoring

**Render/Railway/PythonAnywhere:**
- Truly free (with limits)
- No surprise charges
- Simple deployment
- Perfect for learning/small projects

---

## 🔧 Cleanup (To Avoid Charges)

When you're done testing:

```bash
# Stop EC2 instance (still charges for storage)
AWS Console → EC2 → Select instance → Stop

# OR Terminate (completely free)
AWS Console → EC2 → Select instance → Terminate

# Release Elastic IP (if you created one)
AWS Console → EC2 → Elastic IPs → Release

# Delete snapshots
AWS Console → EC2 → Snapshots → Delete
```

---

## 💡 Final Recommendation

**For your bakery project:**

| Platform | Free? | Best For |
|----------|-------|----------|
| **Render** ⭐ | Yes | Production-ready hobby projects |
| **PythonAnywhere** | Yes | Learning, simple projects |
| **Railway** | $5/month credit | Modern apps, good DX |
| **AWS** | 12 months* | Learning AWS, future scaling |

*But requires careful monitoring and expires

**My advice:** Start with **Render**, learn the ropes, then move to AWS when you understand cloud costs better.

---

## 📚 Resources

- [AWS Free Tier FAQs](https://aws.amazon.com/free/free-tier-faqs/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [Render Documentation](https://render.com/docs)
