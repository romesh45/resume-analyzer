# Deployment Guide

## Platform: Render.com (Recommended)

Render is the best choice for this project because it:
- Offers a **free tier** for lightweight apps
- Integrates seamlessly with **GitHub**
- Auto-deploys on every git push
- Supports Python/Flask perfectly
- Handles file uploads (PDF processing)

---

## Step-by-Step Deployment to Render

### 1. **Push to GitHub**
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### 2. **Create Render Account**
- Go to https://render.com
- Sign up with GitHub
- Grant repository access

### 3. **Create New Web Service**
- Click **New +** → **Web Service**
- Connect your GitHub repository: `resume-analyzer`
- Select the repo branch (usually `main`)

### 4. **Configure Service**
Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `resume-analyzer` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:10000 'src.app:app'` |

### 5. **Environment Variables**
Add in the **Environment** section:
```
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

### 6. **Disk (for file uploads)**
- Add a persistent disk:
  - **Name**: `uploads`
  - **Mount path**: `/var/data/uploads`
  - **Size**: 1 GB

### 7. **Deploy**
- Click **Create Web Service**
- Render automatically builds and deploys
- Your app will be live at: `https://resume-analyzer.onrender.com`

---

## Alternative Deployment Options

### **Railway** (Also Excellent)
- Free tier available
- GitHub auto-deployment
- **Deploy**: Connect repo at https://railway.app, select `resume-analyzer`

### **PythonAnywhere**
- Python-specific hosting
- Beginner-friendly dashboard
- **Deploy**: https://www.pythonanywhere.com (manual upload or GitHub)

### **DigitalOcean**
- Most affordable paid option ($12/month)
- Full control, more scalable
- **Deploy**: Create Droplet → Install Python → Clone repo → Run with Gunicorn

---

## Testing Your Deployment

After deployment, test with:

```bash
# Test web interface
curl https://your-app-url.com

# Test API endpoint
curl -X POST https://your-app-url.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python, Flask, API Development",
    "job_description": "We need Python developer with Flask experience"
  }'
```

---

## Monitoring & Logs

**On Render:**
- Dashboard → Your service → **Logs**
- View real-time deployment logs
- Monitor for errors and crashes

---

## Cost Estimation

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Render** | ✅ Available | $7-15/month |
| **Railway** | ✅ Available | $5/month |
| **DigitalOcean** | ❌ No | $12/month |
| **PythonAnywhere** | ✅ Limited | $5/month |

---

## Next Steps

1. Commit the deployment files: `render.yaml`, `.env.example`
2. Push to GitHub
3. Sign up on Render
4. Connect your repository
5. Your app will deploy automatically! 🚀

