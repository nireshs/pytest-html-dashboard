# Dashboard Screenshots

## How to Add a Screenshot

1. Open the sample report in your browser:
   - Navigate to: `reports/complete_dashboard_report.html`
   - Or use the live link: https://htmlpreview.github.io/?https://github.com/nireshs/pytest-html-dashboard/blob/main/reports/complete_dashboard_report.html

2. Take a screenshot:
   - **Windows**: Press `Win + Shift + S` (Snipping Tool)
   - **Mac**: Press `Cmd + Shift + 4`
   - Capture the full dashboard including header, charts, and table

3. Save the screenshot as:
   - `dashboard-preview.png` (main preview)
   - Recommended size: 1200px wide minimum
   - Format: PNG for best quality

4. Place the file in this directory: `docs/images/`

5. Commit and push:
   ```bash
   git add docs/images/dashboard-preview.png
   git commit -m "docs: add dashboard preview screenshot"
   git push origin main
   ```

## Alternative: Use GitHub Actions to Auto-Generate

You can also set up automated screenshot generation using Playwright or Puppeteer in GitHub Actions.

## Recommended Screenshots

- `dashboard-preview.png` - Full dashboard view (required for README)
- `charts-detail.png` - Close-up of interactive charts
- `error-analysis.png` - Error classification section
- `filters-demo.gif` - Animated demo of filter functionality
