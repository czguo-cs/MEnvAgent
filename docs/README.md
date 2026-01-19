# MEnvAgent GitHub Pages

This directory contains the source code for the MEnvAgent project website hosted on GitHub Pages.

## 🌐 Website URL

Once published, the website will be available at:
- `https://your-username.github.io/MEnvAgent/` (if using project pages)
- `https://your-domain.com` (if using custom domain)

## 📁 Directory Structure

```
docs/
├── index.html              # Main HTML file
├── assets/
│   ├── css/
│   │   └── style.css       # Stylesheet
│   ├── js/
│   │   └── script.js       # JavaScript functionality
│   └── images/             # Image assets (to be added)
├── IMAGE_REQUIREMENTS.md   # Guide for required images
└── README.md              # This file
```

## 🚀 Setup GitHub Pages

### Method 1: Using GitHub Settings (Recommended)

1. **Push the `docs/` directory** to your GitHub repository:
   ```bash
   git add docs/
   git commit -m "Add GitHub Pages website"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Source", select:
     - Branch: `main`
     - Folder: `/docs`
   - Click **Save**

3. **Wait for deployment**:
   - GitHub will automatically build and deploy your site
   - This usually takes 1-2 minutes
   - You'll see a green checkmark and the URL when it's ready

### Method 2: Using gh-pages Branch

Alternatively, you can use a dedicated `gh-pages` branch:

```bash
# Create and switch to gh-pages branch
git checkout -b gh-pages

# Copy docs content to root
cp -r docs/* .

# Commit and push
git add .
git commit -m "Deploy GitHub Pages"
git push origin gh-pages

# Switch back to main
git checkout main
```

Then in GitHub Settings → Pages, select `gh-pages` branch and `/ (root)`.

## 🎨 Adding Images

Before publishing, you should add the required images. See [`IMAGE_REQUIREMENTS.md`](IMAGE_REQUIREMENTS.md) for:
- List of required images
- Recommended dimensions
- Where to place them
- How to replace placeholders

### Quick Steps:

1. Create your images according to specifications
2. Place them in `docs/assets/images/`
3. Update `index.html` to replace placeholder divs with `<img>` tags
4. Test locally (see Testing section below)
5. Commit and push

## 🧪 Testing Locally

To preview the website locally before publishing:

### Option 1: Using Python's HTTP Server

```bash
cd docs
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

### Option 2: Using Node.js http-server

```bash
npm install -g http-server
cd docs
http-server
```

### Option 3: Using VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

## ✏️ Customization

### Update Repository Links

Replace placeholder URLs throughout `index.html`:

```html
<!-- Change from: -->
<a href="https://github.com/your-org/MEnvAgent">

<!-- To: -->
<a href="https://github.com/actual-username/MEnvAgent">
```

### Update arXiv and Dataset Links

When paper and dataset are published:

```html
<!-- Update arXiv link -->
<a href="https://arxiv.org/abs/XXXX.XXXXX">
<!-- To actual arXiv ID -->

<!-- Update HuggingFace dataset link -->
<a href="https://huggingface.co/datasets/TODO/MEnvData-SWE-2K">
<!-- To actual dataset path -->
```

### Modify Colors

Edit `assets/css/style.css` to change the color scheme:

```css
:root {
    --primary-color: #6366f1;  /* Change to your preferred color */
    --secondary-color: #10b981;
    /* ... */
}
```

### Add Custom Domain (Optional)

1. Create a file named `CNAME` in the `docs/` directory:
   ```bash
   echo "your-domain.com" > docs/CNAME
   ```

2. Configure DNS settings at your domain registrar:
   - Add CNAME record pointing to `your-username.github.io`

3. In GitHub Settings → Pages, enter your custom domain

## 📝 Content Updates

### Updating News

Edit the news section in `index.html`:

```html
<div class="news-item">
    <div class="news-date">Month Year</div>
    <div class="news-content">
        <h4>News Title</h4>
        <p>News description...</p>
    </div>
</div>
```

### Updating Results

Replace "TBD" values in the results section with actual data:

```html
<div class="improvement-value">+8.6%</div>
```

### Adding Authors

Update the citation section with actual author names:

```html
<code>@article{menvagent2026,
  title={MEnvAgent: ...},
  author={FirstAuthor, SecondAuthor, ThirdAuthor},  <!-- Update this -->
  journal={...},
  year={2026}
}</code>
```

## 🔧 Troubleshooting

### Site Not Displaying

1. Check that GitHub Pages is enabled in Settings
2. Verify the correct branch and folder are selected
3. Ensure all files are pushed to the repository
4. Wait 1-2 minutes for GitHub to rebuild
5. Try clearing browser cache or using incognito mode

### Images Not Loading

1. Verify image paths are correct (relative to `index.html`)
2. Check image files are in `docs/assets/images/`
3. Ensure image filenames match exactly (case-sensitive)

### CSS/JS Not Loading

1. Check that paths in `index.html` are correct:
   ```html
   <link rel="stylesheet" href="assets/css/style.css">
   <script src="assets/js/script.js"></script>
   ```
2. Verify files exist in the correct locations
3. Check browser console for 404 errors

### Layout Issues on Mobile

1. Test on multiple devices/screen sizes
2. Use browser developer tools to simulate mobile
3. Check responsive CSS media queries in `style.css`

## 📊 Analytics (Optional)

To track website visitors, add Google Analytics:

1. Get your Google Analytics tracking ID
2. Add before `</head>` in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 🎯 SEO Optimization

The site includes basic SEO meta tags. To enhance:

1. **Add Open Graph tags** for social media sharing:
```html
<meta property="og:title" content="MEnvAgent">
<meta property="og:description" content="...">
<meta property="og:image" content="assets/images/og-image.png">
```

2. **Add Twitter Card tags**:
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="MEnvAgent">
```

3. **Create sitemap.xml** (optional for better indexing)

## 📚 Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [HTML5 Boilerplate](https://html5boilerplate.com/)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [Google Fonts](https://fonts.google.com/)

## 🤝 Contributing

To suggest improvements to the website:

1. Fork the repository
2. Make changes in the `docs/` directory
3. Test locally
4. Submit a pull request

## 📧 Support

For issues with the website, please:
- Open an issue on GitHub
- Tag with "website" label
- Include screenshots if applicable

---

**Note**: Remember to update placeholder content and add images before the official launch!
