# Deployment Guide - Research Agent

## Option 1: Streamlit Community Cloud (Recommended - FREE)

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Steps

1. **Prepare Your Repository**
   ```bash
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Initial commit"
   
   # Create a new repo on GitHub and push
   git remote add origin https://github.com/YOUR_USERNAME/research-agent.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/research-agent`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In your Streamlit Cloud dashboard, click on your app
   - Go to "Settings" → "Secrets"
   - Add your secrets (use your actual API keys from `.env`):
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   GOOGLE_API_KEY = "your-google-api-key-here"
   SEARCH_PROVIDER = "duckduckgo"
   ```

4. **Access Your App**
   - Your app will be live at: `https://YOUR_USERNAME-research-agent-XXXXX.streamlit.app`
   - Share this URL with anyone!

---

## Option 2: Railway (Alternative - FREE Tier Available)

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add Environment Variables**
   ```bash
   railway variables set GROQ_API_KEY="your-key-here"
   railway variables set GOOGLE_API_KEY="your-key-here"
   railway variables set SEARCH_PROVIDER="duckduckgo"
   ```

---

## Option 3: Render (Alternative - FREE Tier Available)

1. **Create `render.yaml`** (already in your project)

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Create a new "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect and deploy

3. **Add Environment Variables**
   - In Render dashboard, go to "Environment"
   - Add: `GROQ_API_KEY`, `GOOGLE_API_KEY`, `SEARCH_PROVIDER`

---

## Testing Your Deployment

After deployment, test with:
- Simple draft: "Elon Musk bought Twitter."
- Complex draft: "The Python programming language was created by Guido van Rossum and was released in 1991."

---

## Troubleshooting

### App crashes on startup
- Check logs in your deployment platform
- Verify all dependencies are in `requirements.txt`
- Ensure secrets are properly set

### No results from research
- Verify GROQ_API_KEY is valid
- Check DuckDuckGo search is not rate-limited

### Slow performance
- Free tiers have resource limits
- Consider upgrading to paid tier for faster processing

---

## Cost Comparison

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Streamlit Cloud | ✅ 1 app | $20/month (3 apps) |
| Railway | ✅ $5 credit | Pay-as-you-go |
| Render | ✅ 750 hrs/month | $7/month+ |

**Recommendation**: Start with Streamlit Community Cloud for the easiest setup!
