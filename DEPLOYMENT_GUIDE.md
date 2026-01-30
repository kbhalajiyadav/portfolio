# 🚀 Hugo Blox Portfolio - Deployment Guide

This guide will walk you through deploying your Hugo Blox portfolio website to **GitHub Pages**.

---

## 📋 Prerequisites

Before you begin, make sure you have:

1. **GitHub Account** - [Sign up here](https://github.com/signup) if you don't have one
2. **Git installed** on your computer - [Download Git](https://git-scm.com/downloads)
3. **Hugo Extended** installed (optional for local testing) - [Install Hugo](https://gohugo.io/installation/)

---

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and log in to your account
2. Click the **+** icon in the top right corner → **New repository**
3. Name your repository: `portfolio` (or any name you prefer)
4. Make it **Public** (required for GitHub Pages)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Step 2: Upload Your Portfolio Files

#### Option A: Using Git Command Line (Recommended)

Open your terminal/command prompt and run:

```bash
# Navigate to your portfolio folder
cd /path/to/bhalaji-portfolio

# Initialize Git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial portfolio setup"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

#### Option B: Using GitHub Web Interface

1. On your repository page, click **uploading an existing file** link
2. Drag and drop all files from your `bhalaji-portfolio` folder
3. Click **Commit changes**

### Step 3: Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab (top of the page)
3. In the left sidebar, click **Pages**
4. Under **Source**, select **GitHub Actions**
5. The workflow file (`.github/workflows/hugo.yaml`) is already included in your repository

### Step 4: Enable GitHub Actions

1. In your repository, click the **Actions** tab
2. You may see a message: "Workflows aren't being run on this forked repository"
3. Click **I understand my workflows, go ahead and enable them**
4. The workflow will automatically run and deploy your site

### Step 5: Wait for Deployment

1. Go to the **Actions** tab to see the deployment progress
2. Wait for the workflow to complete (usually 2-5 minutes)
3. Once complete, your site will be live at:
   ```
   https://YOUR_USERNAME.github.io/portfolio
   ```

---

## 🔄 Making Updates

Whenever you want to update your portfolio:

```bash
# Navigate to your portfolio folder
cd /path/to/bhalaji-portfolio

# Make your changes to the files

# Add, commit, and push changes
git add .
git commit -m "Update portfolio - [describe your changes]"
git push origin main
```

GitHub Actions will automatically rebuild and redeploy your site!

---

## 🎨 Customizing Your Portfolio

### Update Personal Information

Edit `content/authors/admin/_index.md` to update:
- Your bio
- Social media links
- Contact information

### Update Homepage Content

Edit `content/_index.md` to modify:
- Hero section (main banner)
- Experience timeline
- Projects showcase
- Skills section

### Add New Projects

1. Create a new folder in `content/project/PROJECT_NAME/`
2. Add an `index.md` file with your project details
3. Push to GitHub

### Add Publications

1. Create a new folder in `content/publication/PUBLICATION_NAME/`
2. Add an `index.md` file with publication details
3. Push to GitHub

### Update Profile Photo

Replace `assets/images/avatar.png` with your own photo (keep the same filename).

### Update Resume

Replace `static/uploads/resume.pdf` with your latest resume.

---

## 📁 File Structure

```
bhalaji-portfolio/
├── .github/
│   └── workflows/
│       └── hugo.yaml          # GitHub Actions deployment
├── assets/
│   └── images/
│       └── avatar.png         # Your profile photo
├── config/
│   └── _default/
│       ├── config.yaml        # Hugo configuration
│       ├── languages.yaml     # Site navigation
│       ├── module.yaml        # Module settings
│       └── params.yaml        # Site parameters
├── content/
│   ├── _index.md              # Homepage content
│   ├── authors/
│   │   └── admin/
│   │       └── _index.md      # Your profile/bio
│   ├── project/               # Your projects
│   │   ├── thermochromic-textiles/
│   │   ├── adhesion-analysis/
│   │   ├── fda-compliance/
│   │   └── supply-chain-automation/
│   └── publication/           # Your publications
│       ├── electrospun-fiber-mats/
│       └── adhesives-wearable/
├── static/
│   └── uploads/
│       └── resume.pdf         # Your resume
├── .gitignore
├── DEPLOYMENT_GUIDE.md        # This guide
└── go.mod                     # Hugo module file
```

---

## 🐛 Troubleshooting

### Issue: Site not deploying

**Solution:**
1. Check the **Actions** tab for error messages
2. Ensure your repository is **Public**
3. Verify GitHub Pages is set to use **GitHub Actions**

### Issue: Images not showing

**Solution:**
- Make sure images are in the `assets/images/` folder
- Reference them correctly in your markdown files

### Issue: Changes not appearing

**Solution:**
1. Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)
2. Check the Actions tab to ensure deployment completed
3. Wait a few minutes for GitHub Pages to update

### Issue: "Workflow not found"

**Solution:**
- Ensure the `.github/workflows/hugo.yaml` file exists
- Check that the file is in the correct location
- Verify the YAML syntax is correct

---

## 📚 Additional Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Blox Documentation](https://docs.hugoblox.com/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 💡 Tips

1. **Test locally first** (optional): If you have Hugo installed, run `hugo server -D` to preview changes locally
2. **Use meaningful commit messages** to track your changes
3. **Update regularly** to keep your portfolio current
4. **Check your site on mobile** to ensure responsive design

---

## ✅ Quick Checklist

- [ ] Created GitHub repository
- [ ] Uploaded all portfolio files
- [ ] Enabled GitHub Actions
- [ ] Configured GitHub Pages source to "GitHub Actions"
- [ ] Workflow completed successfully
- [ ] Site is live at `https://YOUR_USERNAME.github.io/portfolio`

---

## 📞 Need Help?

If you encounter issues:
1. Check the [Hugo Blox documentation](https://docs.hugoblox.com/)
2. Review [GitHub Pages troubleshooting](https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites)
3. Check the Actions logs for specific error messages

---

**Your portfolio will be live at:** `https://kbhalajiyadav.github.io/portfolio` 🎉
