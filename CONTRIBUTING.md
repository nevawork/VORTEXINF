# Contributing to VORTEX|INF

Thank you for your interest in contributing to VORTEX|INF! We appreciate your help in making this bot better.

**Owner:** NEVA 3pa8  
**Discord:** https://discord.gg/98qaRWnKuH

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)

---

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing. We expect all contributors to follow these guidelines.

---

## How to Contribute

There are several ways you can contribute to VORTEX|INF:

1. **Report Bugs** - Found an issue? Let us know!
2. **Suggest Features** - Have an idea? Share it!
3. **Improve Documentation** - Help make docs clearer
4. **Submit Code** - Fix bugs or add features (requires approval)
5. **Community Support** - Help other users in the Discord

---

## Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported
2. Update to the latest version
3. Try to reproduce the bug consistently

### How to Report

1. Open a GitHub Issue
2. Use a clear, descriptive title
3. Provide a detailed description of the bug
4. Include steps to reproduce
5. Provide the error message or log output
6. Include your bot configuration (without sensitive data)
7. Specify your Python version and OS

### Bug Report Template

```
**Title:** [Brief description]

**Description:**
[Detailed explanation]

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Message:**
[Include full error or logs]

**Environment:**
- Python Version: X.X.X
- Discord.py Version: X.X.X
- OS: Windows/Linux/Mac
- Bot Version: [commit hash or date]
```

---

## Suggesting Features

### Before Suggesting

1. Check if the feature already exists
2. Check if a similar feature is planned
3. Make sure it aligns with the bot's purpose

### How to Suggest

1. Open a GitHub Issue with the "enhancement" label
2. Use a clear, descriptive title
3. Explain the feature and why it would be useful
4. Provide examples or mockups if applicable
5. List any related features

### Feature Request Template

```
**Title:** [Feature description]

**Problem Statement:**
[Explain why this feature is needed]

**Proposed Solution:**
[Describe the feature in detail]

**Alternative Solutions:**
[Any other approaches?]

**Example Usage:**
/command_name [parameters]

**Additional Context:**
[Screenshots, references, etc.]
```

---

## Pull Request Guidelines

### Before Starting

1. **Get Approval:** Discuss your change in an issue first
2. **Fork the Repository:** Create your own copy
3. **Create a Branch:** `git checkout -b feature/your-feature-name`
4. **Keep It Small:** Focus on a single issue or feature
5. **Test Your Code:** Ensure it works correctly

### Submitting a Pull Request

1. **Push to Your Fork:** `git push origin feature/your-feature-name`
2. **Open a PR:** Click "New Pull Request" on GitHub
3. **Fill Out Template:** Provide all required information
4. **Link the Issue:** Reference the related issue
5. **Wait for Review:** We'll review and provide feedback
6. **Address Feedback:** Make requested changes
7. **Done!:** We'll merge when approved

### PR Template

```
**Description:**
[Brief summary of changes]

**Related Issue:**
Closes #[issue number]

**Type of Change:**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

**Changes Made:**
- Change 1
- Change 2
- Change 3

**Testing:**
- [ ] Tested locally
- [ ] No breaking changes
- [ ] Error handling added

**Checklist:**
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests passing
``` 

---

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Virtual Environment (recommended)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/VORTEXINF.git
cd VORTEXINF

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your test bot token to .env
```

### Running Tests

```bash
# Run the bot locally
python vortex.py

# Check for syntax errors
python -m py_compile vortex.py

# Check code style
pip install pylint
pylint *.py
```

---

## Coding Standards

### Python Style

- Follow **PEP 8** standards
- Use **4 spaces** for indentation
- Use **descriptive variable names**
- Add **docstrings** to all functions
- Keep **lines under 100 characters** (where possible)

### Example Function

```python
def calculate_user_level(experience: int) -> int:
    """
    Calculate user level based on experience points.
    
    Args:
        experience (int): Total experience points
        
    Returns:
        int: User level (1-100)
    """
    if not isinstance(experience, int) or experience < 0:
        raise ValueError("Experience must be a positive integer")
    
    return min(experience // 1000 + 1, 100)
```

### Naming Conventions

- **Functions/Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private Methods:** `_leading_underscore`

### Comments

- Add comments for complex logic
- Explain the "why", not the "what"
- Use `#` for inline comments
- Use `"""` for docstrings

### Error Handling

```python
try:
    result = await database.query(user_id)
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

---

## Important Notes

⚠️ **This is a proprietary project owned by NEVA 3pa8**

- Commercial use is **NOT allowed** without explicit permission
- You cannot redistribute this code
- You cannot modify and publish under a different name
- Contributing implies agreement to these terms

---

## Questions?

Join our Discord community: https://discord.gg/98qaRWnKuH

**Thank you for contributing to VORTEX|INF!** ❤️