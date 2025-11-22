# Update GitHub Information Script
param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    [Parameter(Mandatory=$true)]
    [string]$AuthorName,
    [Parameter(Mandatory=$true)]
    [string]$AuthorEmail
)

Write-Host 'Updating GitHub information...' -ForegroundColor Cyan
Write-Host '  GitHub Username: ' -NoNewline; Write-Host $GitHubUsername -ForegroundColor Yellow
Write-Host '  Author Name: ' -NoNewline; Write-Host $AuthorName -ForegroundColor Yellow
Write-Host '  Author Email: ' -NoNewline; Write-Host $AuthorEmail -ForegroundColor Yellow
Write-Host ''

$files = @('setup.py', 'pyproject.toml', 'README.md', 'CHANGELOG.md')

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host 'Updating ' -NoNewline; Write-Host $file -ForegroundColor Green
        $content = Get-Content $file -Raw
        $content = $content -replace 'yourusername', $GitHubUsername
        $content = $content -replace 'Your Name', $AuthorName
        $content = $content -replace 'your\.email@example\.com', $AuthorEmail
        Set-Content $file -Value $content -NoNewline
        Write-Host '  Updated successfully' -ForegroundColor Green
    }
}

Write-Host ''
Write-Host 'All files updated!' -ForegroundColor Green
Write-Host 'Next: git add . && git commit -m \"Update GitHub info\" && git push' -ForegroundColor Cyan
