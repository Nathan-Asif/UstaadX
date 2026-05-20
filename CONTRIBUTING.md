# Contributing to UstaadX

Thank you for your interest in contributing to UstaadX!

## Development Workflow

### 1. Fork and Clone

```bash
git clone <your-fork-url>
cd ustaadx
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 3. Make Changes

- Follow code style guidelines
- Write tests for new features
- Update documentation
- Keep commits focused and atomic

### 4. Commit Changes

Use conventional commit messages:

```bash
git commit -m "feat: add provider matching algorithm"
git commit -m "fix: resolve booking creation bug"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify event handler logic"
git commit -m "test: add workflow engine tests"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Create a Pull Request with:
- Clear title and description
- Reference related issues
- List changes made
- Include screenshots (if UI changes)

## Code Style

### Python (Backend)

- Follow PEP 8
- Use Black for formatting
- Use Ruff for linting
- Type hints encouraged
- Max line length: 100

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type check
mypy app/
```

### Dart (Mobile)

- Follow Dart style guide
- Use `flutter format`
- Follow `analysis_options.yaml`
- Prefer const constructors
- Use trailing commas

```bash
# Format code
flutter format lib/

# Analyze code
flutter analyze
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_events.py
```

### Mobile Tests

```bash
# Run all tests
flutter test

# Run specific test
flutter test test/features/auth_test.dart

# Run with coverage
flutter test --coverage
```

## Documentation

- Update relevant docs for changes
- Add code comments for complex logic
- Update API documentation
- Include examples where helpful

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commits are clean and focused

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How was this tested?

## Screenshots (if applicable)

## Related Issues
Closes #123
```

## Code Review Process

1. Automated checks run (linting, tests)
2. Maintainer reviews code
3. Feedback addressed
4. Approved and merged

## Getting Help

- Check existing documentation
- Search existing issues
- Ask in discussions
- Create new issue if needed

## License

By contributing, you agree that your contributions will be licensed under the project license.
