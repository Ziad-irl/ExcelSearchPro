#!/usr/bin/env python3
"""
Quick GitHub deployment setup script for ExcelSearchPro
Run this script to prepare your project for GitHub deployment
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🚀 ExcelSearchPro GitHub Deployment Setup")
    print("=" * 50)
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed or not in PATH")
        print("Please install Git first: https://git-scm.com/downloads")
        sys.exit(1)
    
    print("✅ Git is installed")
    
    # Get GitHub username
    github_username = input("\n📝 Enter your GitHub username: ").strip()
    if not github_username:
        print("❌ GitHub username is required")
        sys.exit(1)
    
    # Update README.md with actual username
    readme_path = "README.md"
    if os.path.exists(readme_path):
        print(f"🔄 Updating {readme_path} with your GitHub username...")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('yourusername', github_username)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {readme_path}")
    
    # Update pyproject.toml with actual username
    pyproject_path = "pyproject.toml"
    if os.path.exists(pyproject_path):
        print(f"🔄 Updating {pyproject_path} with your GitHub username...")
        with open(pyproject_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('yourusername', github_username)
        
        with open(pyproject_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {pyproject_path}")
    
    # Initialize git repository
    if not os.path.exists('.git'):
        if not run_command("git init", "Initializing Git repository"):
            sys.exit(1)
    else:
        print("✅ Git repository already initialized")
    
    # Add all files
    if not run_command("git add .", "Adding all files to Git"):
        sys.exit(1)
    
    # Create initial commit
    commit_msg = "Initial commit: ExcelSearchPro v1.0.0 with GitHub Actions"
    if not run_command(f'git commit -m "{commit_msg}"', "Creating initial commit"):
        # Check if there are changes to commit
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        if not result.stdout.strip():
            print("ℹ️  No changes to commit")
        else:
            sys.exit(1)
    
    # Add remote (user will need to create the repo first)
    repo_url = f"https://github.com/{github_username}/ExcelSearchPro.git"
    print(f"\n📋 Next steps:")
    print(f"1. Create a new repository on GitHub named 'ExcelSearchPro'")
    print(f"2. Don't initialize with README, .gitignore, or license")
    print(f"3. Run these commands:")
    print(f"   git remote add origin {repo_url}")
    print(f"   git branch -M main")
    print(f"   git push -u origin main")
    print(f"\n🏷️  To create your first release:")
    print(f"   git tag -a v1.0.0 -m 'ExcelSearchPro v1.0.0'")
    print(f"   git push origin v1.0.0")
    print(f"\n🎉 Setup complete! Check DEPLOYMENT.md for detailed instructions.")

if __name__ == "__main__":
    main()
