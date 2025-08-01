# GitHub Setup and Maintenance Guide

## 🚀 Setting Up GitHub Repository

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in to your account
2. **Click the "+" icon** in the top right corner
3. **Select "New repository"**
4. **Fill in the details:**
   - Repository name: `rag-api-document-qa`
   - Description: `A smart Retrieval-Augmented Generation (RAG) API for document question answering`
   - Make it **Public** (for portfolio visibility)
   - **Don't** initialize with README (we already have one)
   - **Don't** add .gitignore (we already have one)
   - **Don't** add license (we'll add it later if needed)

### Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Run these in your terminal:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/rag-api-document-qa.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Setup

Visit your GitHub repository URL to confirm everything is uploaded correctly.

## 📝 Best Practices for GitHub Maintenance

### 1. Commit Message Convention

Use clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "feat: Add PDF document processing functionality"
git commit -m "fix: Resolve OCR image processing bug"
git commit -m "docs: Update README with API usage examples"
git commit -m "refactor: Improve vector search performance"

# Commit message format: type: description
# Types: feat, fix, docs, style, refactor, test, chore
```

### 2. Branch Strategy

```bash
# Main branch - always stable
git checkout main

# Feature branches for new development
git checkout -b feature/document-processing
git checkout -b feature/ocr-integration
git checkout -b feature/vector-storage

# Bug fix branches
git checkout -b fix/upload-endpoint-error
```

### 3. Pull Request Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

3. **Push to GitHub**
   ```bash
   git push origin feature/new-feature
   ```

4. **Create Pull Request** on GitHub
   - Go to your repository on GitHub
   - Click "Compare & pull request"
   - Add description of changes
   - Request review if working with others

5. **Merge after review**
   - Delete feature branch after merging

### 4. Regular Maintenance

#### Daily Tasks
```bash
# Pull latest changes
git pull origin main

# Check status
git status

# View recent commits
git log --oneline -10
```

#### Weekly Tasks
```bash
# Update dependencies
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: Update dependencies"

# Clean up old branches
git branch -d feature/old-feature
git push origin --delete feature/old-feature
```

## 🔧 GitHub Features to Use

### 1. Issues
- Create issues for bugs, feature requests, and tasks
- Use labels to categorize issues
- Assign issues to team members
- Link issues to pull requests

### 2. Projects (Kanban Board)
- Create a project board for task management
- Organize issues by status (To Do, In Progress, Done)
- Track progress visually

### 3. Wiki
- Create project documentation
- Add setup guides
- Document API endpoints

### 4. Actions (CI/CD)
- Set up automated testing
- Deploy to staging/production
- Run code quality checks

## 📋 Repository Structure

Your repository should look like this:

```
rag-api-document-qa/
├── .github/                    # GitHub specific files
│   ├── workflows/             # GitHub Actions
│   └── ISSUE_TEMPLATE.md      # Issue templates
├── app/                       # Application code
├── data/                      # Data directories
├── docs/                      # Documentation
├── tests/                     # Test files
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── env.example               # Environment template
└── LICENSE                   # Project license
```

## 🛡️ Security Best Practices

### 1. Never Commit Sensitive Data
```bash
# ✅ Good - Use environment variables
OPENAI_API_KEY=your_key_here

# ❌ Bad - Never commit actual API keys
OPENAI_API_KEY=sk-1234567890abcdef
```

### 2. Use .env for Local Development
```bash
# Copy environment template
cp env.example .env

# Edit .env with your actual values
# .env is in .gitignore, so it won't be committed
```

### 3. Regular Security Updates
```bash
# Update dependencies regularly
pip install --upgrade package-name

# Check for security vulnerabilities
pip-audit
```

## 📊 Monitoring and Analytics

### 1. GitHub Insights
- View repository traffic
- Monitor code frequency
- Track contributor activity

### 2. Code Quality
- Use GitHub's code scanning
- Set up automated testing
- Monitor test coverage

## 🚀 Deployment Integration

### 1. Heroku
```bash
# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

### 2. Vercel/Netlify
- Connect GitHub repository
- Automatic deployments on push
- Preview deployments for pull requests

## 📞 Getting Help

- **GitHub Docs**: https://docs.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **GitHub Community**: https://github.com/orgs/community/discussions

## 🎯 Next Steps

1. Create the GitHub repository
2. Push your code
3. Set up branch protection rules
4. Create your first issue
5. Set up GitHub Actions for CI/CD
6. Add project description and topics
7. Create a development roadmap 