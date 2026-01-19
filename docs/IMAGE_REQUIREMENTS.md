# Image Requirements for MEnvAgent GitHub Pages

This document outlines all the images and visual assets needed for the GitHub Pages website.

## Required Images

### 1. Main Architecture Diagram
- **Location**: Architecture Overview section
- **Filename**: `MEnvAgent-main.png` or similar
- **Recommended Dimensions**: 1200x600px
- **Description**: Diagram showing:
  - Top: Environment Reuse Mechanism (retrieves and adapts historical environments)
  - Bottom: Planning-Execution-Verification loop with autonomous agents
- **Format**: PNG or SVG (SVG preferred for scalability)
- **Path**: Place in `docs/assets/images/`

### 2. Results Comparison Table/Chart
- **Location**: Benchmark section
- **Filename**: `results-comparison.png` or `results-table.png`
- **Recommended Dimensions**: 1000x400px
- **Description**: Performance comparison table or chart showing:
  - F2P Rate (%)
  - Time (min)
  - Cost (USD)
  - Comparison with baseline models
- **Format**: PNG or interactive chart data (JSON)
- **Path**: Place in `docs/assets/images/`

### 3. Language Distribution Chart
- **Location**: Benchmark section
- **Filename**: `language-distribution.png` or `language-performance.png`
- **Recommended Dimensions**: 800x600px
- **Description**: Chart showing performance across different programming languages
- **Suggested Types**: Bar chart, radar chart, or pie chart
- **Format**: PNG or SVG
- **Path**: Place in `docs/assets/images/`

### 4. Dataset Structure Visualization
- **Location**: Dataset section
- **Filename**: `dataset-structure.png`
- **Recommended Dimensions**: 800x600px
- **Description**: Diagram showing:
  - Dataset structure
  - Fields in each instance
  - Data flow
- **Format**: PNG or SVG
- **Path**: Place in `docs/assets/images/`

### 5. Optional: Hero Background Image (Optional)
- **Location**: Hero section background
- **Filename**: `hero-bg.jpg` or `hero-bg.png`
- **Recommended Dimensions**: 1920x1080px
- **Description**: Abstract tech background or pattern
- **Format**: JPG or PNG
- **Path**: Place in `docs/assets/images/`

### 6. Optional: Favicon
- **Filename**: `favicon.ico` or `favicon.png`
- **Dimensions**: 32x32px or 64x64px
- **Description**: Small robot icon or "M" logo
- **Format**: ICO or PNG
- **Path**: Place in `docs/`

## How to Add Images

Once you have the images ready:

1. **Save images** to the `docs/assets/images/` directory
2. **Update the HTML** by replacing the placeholder `<div>` elements with `<img>` tags:

### Example: Replacing Architecture Diagram Placeholder

Replace this:
```html
<div class="image-placeholder architecture-diagram">
    <div class="placeholder-content">
        <i class="fas fa-image"></i>
        <p>Main Architecture Diagram</p>
        <span class="placeholder-note">Please provide: MEnvAgent-main.png or similar</span>
        <span class="placeholder-note">Dimensions: 1200x600px recommended</span>
    </div>
</div>
```

With this:
```html
<div class="architecture-diagram-container">
    <img src="assets/images/MEnvAgent-main.png"
         alt="MEnvAgent Architecture Overview"
         class="architecture-diagram-img">
    <p class="image-caption">
        Overview of MEnvAgent: (Top) Environment Reuse Mechanism retrieves and adapts historical environments.
        (Bottom) Planning-Execution-Verification loop with autonomous agents.
    </p>
</div>
```

3. **Add corresponding CSS** (already included, but can be customized):

```css
.architecture-diagram-img {
    width: 100%;
    height: auto;
    border-radius: 1rem;
    box-shadow: var(--shadow-lg);
    margin: 2rem 0;
}

.image-caption {
    text-align: center;
    color: var(--text-secondary);
    font-style: italic;
    margin-top: 1rem;
}
```

## Image Optimization Tips

1. **Compress images** to reduce load times:
   - Use tools like TinyPNG, ImageOptim, or Squoosh
   - Target file size: < 500KB per image

2. **Use appropriate formats**:
   - PNG for diagrams with text
   - SVG for scalable graphics
   - JPG for photos/screenshots

3. **Add alt text** for accessibility:
   - Describe what the image shows
   - Keep it concise but informative

4. **Consider dark mode** (optional):
   - If diagrams have white backgrounds, add a slight border or shadow
   - Or create dark mode versions

## Tables as Images vs. HTML

For the results comparison table, you have two options:

### Option 1: Table as Image
- Pros: Easy to create, consistent appearance
- Cons: Not responsive, harder to update

### Option 2: HTML Table (Recommended)
Replace the placeholder with:

```html
<div class="results-table-container">
    <table class="results-table">
        <thead>
            <tr>
                <th>Model</th>
                <th>F2P Rate (%)</th>
                <th>Time (min)</th>
                <th>Cost (USD)</th>
            </tr>
        </thead>
        <tbody>
            <tr class="highlight">
                <td><strong>MEnvAgent</strong></td>
                <td><strong>XX.X</strong></td>
                <td><strong>XX.X</strong></td>
                <td><strong>$X.XX</strong></td>
            </tr>
            <tr>
                <td>Baseline-1</td>
                <td>XX.X</td>
                <td>XX.X</td>
                <td>$X.XX</td>
            </tr>
            <tr>
                <td>Baseline-2</td>
                <td>XX.X</td>
                <td>XX.X</td>
                <td>$X.XX</td>
            </tr>
        </tbody>
    </table>
</div>
```

## Current Placeholder Locations

All placeholders are marked with the CSS class `image-placeholder` and can be easily found in `index.html`:

1. Line ~300: Architecture diagram
2. Line ~450: Results table
3. Line ~500: Language distribution chart
4. Line ~600: Dataset structure visualization

## Questions?

If you have any questions about image requirements or need help implementing them, please refer to the main README or open an issue on GitHub.
