# This script will push your project to GitHub
# Run from PowerShell with: ./push_to_github.ps1

# Change these variables
$GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"
$REPO_NAME = "conversational-browser-agent"
$COMMIT_MESSAGE = "Initial commit: Conversational Browser Control Agent"

# Check if git is installed
Write-Host "Checking for git installation..." -ForegroundColor Cyan
try {
    git --version | Out-Null
} catch {
    Write-Host "Git is not installed or not in PATH. Please install git and try again." -ForegroundColor Red
    exit
}

# Initialize git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Cyan
    git init
}

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Cyan
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Cyan
git commit -m $COMMIT_MESSAGE

# Create GitHub repository if it doesn't exist (requires GitHub CLI)
Write-Host "NOTE: To create the repository automatically, install GitHub CLI (gh) first." -ForegroundColor Yellow
Write-Host "Otherwise, create the repository manually on GitHub and run the commands below." -ForegroundColor Yellow
Write-Host ""
Write-Host "GitHub Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Green

# Add GitHub remote and push
Write-Host "To add GitHub remote and push:" -ForegroundColor Cyan
Write-Host "Run these commands after creating your GitHub repository:" -ForegroundColor Cyan
Write-Host ""
Write-Host "git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" -ForegroundColor White
Write-Host "git branch -M main" -ForegroundColor White
Write-Host "git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "For authentication issues, see: https://docs.github.com/en/authentication" -ForegroundColor Yellow
