# 🚀 GitHub Deployment Guide for ExcelSearchPro

This guide will help you deploy ExcelSearchPro to GitHub with automated releases.

## Prerequisites

1. **GitHub Account**: Make sure you have a GitHub account
2. **Git**: Install Git on your system
3. **Python 3.8+**: Ensure Python is installed and working

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and click "New repository"
2. Name it `ExcelSearchPro` (or your preferred name)
3. Make it public or private (your choice)
4. **Don't** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Initialize and Push to GitHub

Open PowerShell in your project directory and run:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: ExcelSearchPro v1.0.0"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ExcelSearchPro.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Set Up PyPI Publishing (Optional)

If you want to publish to PyPI:

1. Create account at [PyPI](https://pypi.org/)
2. Go to Account Settings → API tokens
3. Create a new token with "Entire account" scope
4. In your GitHub repository:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token (starts with `pypi-`)

## Step 4: Create Your First Release

### Method 1: GitHub Web Interface

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `ExcelSearchPro v1.0.0`
5. Describe the release features
6. Click "Publish release"

### Method 2: Git Tags (Command Line)

```powershell
# Create and push a tag
git tag -a v1.0.0 -m "ExcelSearchPro v1.0.0"
git push origin v1.0.0
```

## Step 5: Automated Builds

Once you create a release, GitHub Actions will automatically:

1. **Run Tests** on multiple Python versions and operating systems
2. **Build Executables** for Windows, macOS, and Linux
3. **Create Release Packages** with executables and documentation
4. **Publish to PyPI** (if configured)
5. **Upload Release Assets** to GitHub Releases

## Step 6: Update Repository Links

After creating your repository, update these files:

### README.md
Replace `yourusername` in badges with your actual GitHub username:
```markdown
[![CI/CD](https://github.com/YOURUSERNAME/ExcelSearchPro/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOURUSERNAME/ExcelSearchPro/actions)
```

### pyproject.toml
Update the homepage and repository URLs:
```toml
[project.urls]
"Homepage" = "https://github.com/YOURUSERNAME/ExcelSearchPro"
"Repository" = "https://github.com/YOURUSERNAME/ExcelSearchPro"
"Bug Tracker" = "https://github.com/YOURUSERNAME/ExcelSearchPro/issues"
```

## Release Process for Future Versions

1. **Update Version**: Edit `pyproject.toml` version number
2. **Update Changelog**: Document new features/fixes
3. **Commit Changes**: `git commit -am "Bump version to vX.Y.Z"`
4. **Create Tag**: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
5. **Push**: `git push origin main && git push origin vX.Y.Z`

## Monitoring Builds

- Check **Actions** tab for build status
- View **Releases** page for download links
- Monitor **Issues** for user feedback

## Troubleshooting

### Build Failures
- Check the Actions tab for error logs
- Ensure all dependencies are in `requirements.txt`
- Test builds locally before pushing

### Missing Executables
- Verify PyInstaller builds work locally
- Check that `build_exe.py` runs without errors
- Ensure all imported modules are available

### PyPI Upload Issues
- Verify your PyPI token is correct
- Check that version number is unique
- Ensure package metadata is valid

## Security Best Practices

1. **Never commit secrets** (API keys, passwords)
2. **Use repository secrets** for sensitive data
3. **Enable branch protection** for main branch
4. **Require PR reviews** for important changes
5. **Keep dependencies updated** with security patches

---

🎉 **Congratulations!** Your ExcelSearchPro project is now properly set up for GitHub deployment with automated releases!
