# Carousel Images Folder

## 📸 Place Your Carousel Images Here

This folder contains images for the landing page carousel/slideshow.

---

## ✅ Quick Setup

### 1. Prepare Images
- **Size:** 1200x400px (recommended)
- **Format:** JPEG or PNG
- **File Size:** Under 200KB each
- **Quality:** High quality but compressed

### 2. Name Your Files
```
workshop.jpg      - Hands-on workshops image
seminar.jpg       - Industry seminars image
networking.jpg    - Professional networking image
```

### 3. Compress Images
Use these free tools:
- **TinyPNG:** https://tinypng.com/
- **Squoosh:** https://squoosh.app/
- **Compressor.io:** https://compressor.io/

### 4. Update Template
Edit `templates/landing.html` and replace:

```html
<!-- Replace this -->
<img src="{% static 'images.jpeg' %}" ...>

<!-- With this -->
<img src="{% static 'highlights/workshop.jpg' %}" ...>
```

---

## 📋 Current Placeholder

Currently using: `static/images.jpeg` (placeholder)

**Replace with real event photos for best results!**

---

## 🎯 Image Tips

### Good Images:
✅ Clear, well-lit photos  
✅ Show people and activities  
✅ Professional appearance  
✅ Horizontal orientation (landscape)  
✅ Space at bottom for text overlay

### Avoid:
❌ Blurry or dark photos  
❌ Vertical orientation (portrait)  
❌ Too much text in image  
❌ Large file sizes (>300KB)  
❌ Low resolution

---

## 📱 Mobile Optimization

Images automatically resize for mobile devices:
- **Desktop:** 400px height
- **Mobile:** 300px height
- **Aspect Ratio:** Maintained
- **Loading:** Optimized

---

## ✅ Ready to Go!

1. Add your images to this folder
2. Update the template paths
3. Refresh the landing page
4. Enjoy your beautiful carousel! 🎠

---

**Need help? Check `CAROUSEL_SETUP.md` for detailed instructions.**

