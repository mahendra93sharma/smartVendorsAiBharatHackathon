# Contributing to Smart Vendors

Thank you for your interest in contributing to Smart Vendors! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/smart-vendors.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit and push to your fork
7. Open a Pull Request

## Development Setup

### Prerequisites

- AWS Account (for testing infrastructure)
- Python 3.11+
- Node.js 18+
- Terraform 1.0+
- AWS CLI configured

### Local Development

```bash
# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install frontend dependencies
cd frontend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your AWS credentials and configuration
```

## Code Style Guidelines

### Python

- **Formatter**: Black (line length: 88)
- **Linter**: Flake8
- **Type Checker**: mypy
- **Import Sorting**: isort

```bash
# Format code
black backend/

# Check types
mypy backend/

# Sort imports
isort backend/
```

**Style Rules:**
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use descriptive variable names (no single letters except loop counters)

### TypeScript/JavaScript

- **Formatter**: Prettier
- **Linter**: ESLint
- **Style**: Airbnb TypeScript

```bash
# Format code
npm run format

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix
```

**Style Rules:**
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use explicit types (avoid `any`)
- Keep components under 200 lines
- Extract complex logic into custom hooks

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(voice): add Hindi language support for transcription

Implemented AWS Transcribe integration with hi-IN language code.
Added fallback to English if Hindi transcription fails.

Closes #123
```

```
fix(marketplace): correct buyer notification logic

Fixed bug where buyers were notified multiple times for the same listing.
Added deduplication check before sending SNS notifications.
```

## Testing Guidelines

### Unit Tests

- Write unit tests for all new functions
- Aim for 80%+ code coverage
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`

```python
def test_extract_transaction_valid_hindi_text_returns_transaction():
    """Test that valid Hindi text extracts transaction correctly."""
    text = "Do kilo tamatar, pachas rupaye"
    result = extract_transaction(text, vendor_id="test-123")
    
    assert result.item_name == "tamatar"
    assert result.quantity == 2.0
    assert result.price == 50.0
```

### Property-Based Tests

- Use Hypothesis (Python) or fast-check (TypeScript)
- Test universal properties across many inputs
- Include requirement validation comments

```python
from hypothesis import given, strategies as st

# Feature: hackathon-deliverables, Property 3: Voice transcription
@given(
    audio=audio_file_strategy(),
    language=st.sampled_from(['hi-IN', 'en-IN'])
)
def test_transcription_returns_valid_result(audio, language):
    """Property: Transcription always returns text with confidence score."""
    result = transcribe_audio(audio, language)
    
    assert result.text is not None
    assert 0.0 <= result.confidence <= 1.0
    assert result.language in ['hi-IN', 'en-IN']
```

### Integration Tests

- Test end-to-end flows
- Use mocked AWS services (moto library)
- Clean up resources after tests

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_voice_api.py

# Run property tests with more iterations
pytest tests/property/ --hypothesis-iterations=1000
```

## Pull Request Process

1. **Update Documentation**: Ensure README and docs are updated for new features
2. **Add Tests**: All new code must have tests
3. **Run Linters**: Ensure code passes all linting checks
4. **Update Changelog**: Add entry to CHANGELOG.md (if exists)
5. **Request Review**: Tag relevant maintainers for review

### PR Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts
- [ ] PR description explains changes clearly

## Architecture Decisions

For significant architectural changes:

1. Open an issue first to discuss the approach
2. Get consensus from maintainers
3. Document the decision in `docs/architecture.md`
4. Update architecture diagrams if needed

## AWS Infrastructure Changes

When modifying Terraform configuration:

1. Test changes in a separate AWS account/environment
2. Document new resources in `infrastructure/README.md`
3. Update cost estimates if applicable
4. Ensure backward compatibility or provide migration guide

## Documentation

- Keep documentation up-to-date with code changes
- Use clear, concise language
- Include code examples where helpful
- Add diagrams for complex concepts

### Documentation Structure

```
docs/
├── architecture.md      # System architecture
├── API.md              # API documentation
├── DEPLOYMENT.md       # Deployment guide
└── screenshots/        # UI screenshots
```

## Questions or Issues?

- **Bug Reports**: Open an issue with detailed reproduction steps
- **Feature Requests**: Open an issue describing the feature and use case
- **Questions**: Open a discussion or reach out to maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Smart Vendors! 🙏
