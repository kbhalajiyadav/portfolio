# Bhalaji Yadav - Portfolio Website

A professional portfolio website built with **Hugo Blox** and deployed on **GitHub Pages**.

## 🌐 Live Website

Visit the live portfolio at: **https://kbhalajiyadav.github.io/portfolio**

## 📸 Preview

![Portfolio Preview](assets/images/avatar.png)

## 🚀 Quick Start

To deploy this portfolio to your own GitHub Pages:

1. **Create a GitHub repository** named `portfolio`
2. **Upload all files** from this folder to your repository
3. **Enable GitHub Actions** in your repository settings
4. **Configure GitHub Pages** to use GitHub Actions as the source
5. **Wait 2-5 minutes** for automatic deployment

For detailed instructions, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

## 📋 What's Included

### Sections
- **Hero Banner** - Introduction with profile photo
- **About Me** - Professional summary and expertise
- **Experience** - Work history and research positions
- **Projects** - Research projects with detailed descriptions
- **Publications** - Academic papers and presentations
- **Skills** - Technical competencies
- **Achievements** - Awards and recognitions
- **Contact** - Contact information and location

### Projects Featured
1. **Thermochromic Textiles for Diabetic Monitoring** - $30K funded research
2. **Automated Adhesion Testing Protocol** - 80% time reduction automation
3. **FDA Compliance & Quality Systems** - Audit readiness initiative
4. **Supply Chain Data Automation** - Python/Docker automation pipeline

### Publications
- **Journal Article**: "Mechanical Properties of Dual-Layer Electrospun Fiber Mats" - Polymers 17(13), 1777 (2025)
- **Poster Presentations**: ACS Fall 2025, VCU Research Symposium

## 🛠️ Built With

- **[Hugo](https://gohugo.io/)** - Static site generator
- **[Hugo Blox](https://hugoblox.com/)** - Website builder for Hugo
- **[GitHub Pages](https://pages.github.com/)** - Free hosting
- **[GitHub Actions](https://github.com/features/actions)** - Automated deployment

## 📁 File Structure

```
bhalaji-portfolio/
├── .github/workflows/hugo.yaml    # Deployment workflow
├── assets/images/                 # Profile photo and images
├── config/_default/               # Hugo configuration
├── content/                       # Website content
│   ├── authors/admin/            # Profile information
│   ├── project/                  # Project pages
│   └── publication/              # Publication pages
├── static/uploads/               # Resume PDF
└── DEPLOYMENT_GUIDE.md           # Detailed deployment guide
```

## 🔄 Updating Your Portfolio

To make changes:

```bash
# Edit the files you want to change
# Then commit and push:
git add .
git commit -m "Update portfolio"
git push origin main
```

GitHub Actions will automatically rebuild and redeploy your site!

## 📝 Customization Guide

### Update Profile Information
Edit: `content/authors/admin/_index.md`

### Update Homepage
Edit: `content/_index.md`

### Add New Projects
Create: `content/project/PROJECT_NAME/index.md`

### Add Publications
Create: `content/publication/PUBLICATION_NAME/index.md`

### Update Photo
Replace: `assets/images/avatar.png`

### Update Resume
Replace: `static/uploads/resume.pdf`

## 📞 Contact

- **Email**: kbhalajiyadav22@gmail.com
- **LinkedIn**: [linkedin.com/in/kbhalajiyadav](https://linkedin.com/in/kbhalajiyadav)
- **Phone**: +1 (804) 310-4169

## 📄 License

This portfolio template is based on [Hugo Blox](https://hugoblox.com/) which is open source.

---

**Created with ❤️ for Bhalaji Yadav**
