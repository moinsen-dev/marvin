# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of Marvin seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:
- Open a public GitHub issue
- Post about it publicly on social media
- Exploit the vulnerability

### Please DO:
1. **Email us directly** at: security@moinsen.dev
2. **Include the following information:**
   - Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
   - Full paths of source file(s) related to the issue
   - Location of affected source code (tag/branch/commit or direct URL)
   - Any special configuration required to reproduce the issue
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue, including how an attacker might exploit it

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Initial Assessment**: Within 5 business days, we will provide an initial assessment
- **Resolution Timeline**: We aim to resolve critical issues within 30 days
- **Communication**: We will keep you informed about the progress of resolving the issue
- **Credit**: We will credit you for the discovery when we announce the vulnerability (unless you prefer to remain anonymous)

## Security Best Practices for Users

### API Keys and Secrets
- Never commit API keys or secrets to your repository
- Use environment variables for sensitive configuration
- Rotate API keys regularly

### Dependencies
- Keep Marvin and its dependencies up to date
- Run `uv pip audit` regularly to check for known vulnerabilities
- Review security advisories on our GitHub repository

### Configuration
- Use HTTPS for API endpoints when available
- Limit API access with proper authentication
- Follow the principle of least privilege

## Security Features

Marvin includes several security features:

1. **Input Validation**: All user inputs are validated before processing
2. **Dependency Scanning**: Regular automated scans for vulnerable dependencies
3. **Safe File Handling**: Secure file operations with path traversal protection
4. **API Security**: Rate limiting and authentication for API endpoints

## Disclosure Policy

When we receive a security vulnerability report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release new security fix versions
5. Publish a security advisory on GitHub

## Comments on this Policy

If you have suggestions on how this process could be improved, please submit a pull request or open an issue to discuss.