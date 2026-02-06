# Railway Deployment Guide for Uglier

## Quick Fix for 502 Error

The "EOF when reading a line" error happens because `uglier.py` has an interactive REPL mode that tries to read input. Railway doesn't have a terminal, so it fails.

### Solution: Deploy These Files

Make sure you have these files in your Railway project:

1. ✅ `server.py` - Updated to use PORT environment variable
2. ✅ `uglier.py` - The interpreter (without running REPL automatically)
3. ✅ `index.html` - The web interface
4. ✅ `requirements.txt` - Python dependencies
5. ✅ `Procfile` - Tells Railway how to start the app
6. ✅ `nixpacks.toml` - Railway build configuration
7. ✅ `runtime.txt` - Specifies Python version

## Step-by-Step Deployment

### Option 1: Update Your Existing Deployment

1. **Download all the new files** from this conversation
2. **Replace all files** in your Railway GitHub repo
3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix Railway deployment - remove REPL mode"
   git push
   ```
4. Railway will automatically redeploy

### Option 2: Fresh Deploy

1. **Create a new folder** with these files:
   - server.py
   - uglier.py
   - index.html
   - requirements.txt
   - Procfile
   - nixpacks.toml
   - runtime.txt

2. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Uglier interpreter"
   git push origin main
   ```

3. **Deploy on Railway**:
   - Go to Railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect and deploy

### Option 3: Deploy from ZIP

1. **Download all files** to a folder
2. Go to Railway dashboard
3. Click "New Project" → "Deploy from GitHub"
4. Or use Railway CLI:
   ```bash
   railway login
   railway init
   railway up
   ```

## Environment Variables

Railway automatically sets:
- `PORT` - The port your app should listen on (handled in server.py)

No additional environment variables needed!

## Checking Your Deployment

### 1. Check Build Logs
- Go to your Railway project
- Click "Deployments"
- Click on the latest deployment
- Check "Build Logs" - should show:
  ```
  Installing dependencies from requirements.txt
  Building...
  Build succeeded
  ```

### 2. Check Deploy Logs
- Click "Deploy Logs" - should show:
  ```
  Starting Uglier web server on port XXXX...
  Server will be available at http://0.0.0.0:XXXX
  ```

### 3. Check Your Domain
- Visit: `your-app-name.up.railway.app`
- You should see the Uglier web interface
- Try running some code!

## Common Issues & Fixes

### Issue 1: Still Getting EOF Error
**Problem**: The REPL mode in uglier.py is still running

**Fix**: Make sure `uglier.py` does NOT have this at the bottom:
```python
# DON'T HAVE THIS IN PRODUCTION:
if __name__ == "__main__":
    while True:
        inp = input(">>> ")  # This causes EOF error!
```

The version I provided has this section, but it only runs when you run `python uglier.py` directly, NOT when imported by server.py.

### Issue 2: 502 Bad Gateway
**Causes**:
- App isn't binding to the correct PORT
- App crashed during startup
- Dependencies failed to install

**Fix**:
1. Check Deploy Logs for errors
2. Make sure `server.py` uses: `port = int(os.environ.get("PORT", 5000))`
3. Make sure all dependencies in `requirements.txt` install successfully

### Issue 3: App Starts But Shows Blank Page
**Cause**: `index.html` not being served

**Fix**: Make sure `server.py` has:
```python
app = Flask(__name__, static_folder='.')

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')
```

### Issue 4: Can't Import uglier Module
**Cause**: `uglier.py` is trying to run REPL mode when imported

**Fix**: Make sure the REPL code in `uglier.py` is inside:
```python
if __name__ == "__main__":
    # REPL code here
```

This ensures it only runs when you execute `python uglier.py` directly, not when `server.py` imports it.

## Verifying Your Files

### Check server.py
Must include:
```python
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

### Check Procfile
Must contain exactly:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 server:app
```

### Check requirements.txt
Must include:
```
Flask==2.3.3
Werkzeug==2.3.7
gunicorn==21.2.0
```

## Test Locally Before Deploying

Test that everything works locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set PORT manually
export PORT=5000

# Run server
python server.py
```

Visit `http://localhost:5000` - should work!

If it works locally, it will work on Railway.

## Railway CLI Commands

Useful Railway CLI commands:

```bash
# Login
railway login

# Link to existing project
railway link

# Check logs
railway logs

# Open in browser
railway open

# Redeploy
railway up
```

## Success Checklist

✅ All files uploaded to GitHub  
✅ `Procfile` exists and uses gunicorn  
✅ `requirements.txt` has all dependencies  
✅ `server.py` uses `PORT` environment variable  
✅ `uglier.py` doesn't run REPL when imported  
✅ Build logs show successful build  
✅ Deploy logs show server starting  
✅ Can access domain without 502 error  
✅ Web interface loads  
✅ Can run code successfully  

## Still Having Issues?

If you're still getting errors:

1. **Share the exact error** from Deploy Logs
2. **Check which files** you have in Railway
3. **Verify the content** of server.py and uglier.py
4. **Try the health check endpoint**: `your-app.up.railway.app/health`

The most common issue is that `uglier.py` is trying to run the REPL (interactive mode) when imported by Flask, causing the EOF error. The fix is ensuring the REPL code is inside `if __name__ == "__main__":` block.

## Your Domain

Once deployed successfully, your app will be at:
```
https://your-app-name.up.railway.app
```

Share this link with anyone to let them code Python in their browser! 🚀
