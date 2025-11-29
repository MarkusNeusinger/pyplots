# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

1. **Do NOT create a public GitHub Issue** for security vulnerabilities
2. Email the maintainer directly or use GitHub's private vulnerability reporting:
   - Go to the **Security** tab → **Report a vulnerability**
3. Include as much detail as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Resolution Timeline**: Depends on severity
  - Critical: 24-72 hours
  - High: 1-2 weeks
  - Medium/Low: Next release cycle

### Scope

Security issues we're interested in:

- Authentication/authorization bypasses
- SQL injection, XSS, CSRF vulnerabilities
- Exposed secrets or credentials
- Insecure dependencies with known CVEs
- Code execution vulnerabilities in plot generation

### Out of Scope

- Issues in dependencies without a clear exploit path
- Theoretical vulnerabilities without proof of concept
- Social engineering attacks
- Issues requiring physical access

## Security Best Practices for Contributors

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive configuration
- Keep dependencies updated (Dependabot is enabled)
- Follow secure coding practices (OWASP guidelines)
- All AI-generated code is reviewed before merge
