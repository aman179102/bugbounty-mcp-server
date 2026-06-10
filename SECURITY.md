# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of BugBounty MCP Server seriously. If you believe you have
found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to **apgokul008@gmail.com**.

You should receive a response within 48 hours. If you do not, please follow up
via email to ensure we received your original message.

### What to Include

- Type of vulnerability
- Full path of source file(s) related to the vulnerability
- Location of affected source code (tag/branch/commit)
- Any special configuration required
- Step-by-step instructions to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability

### What to Expect

- We will acknowledge receipt of your report within 48 hours
- We will provide a more detailed response within 72 hours
- We will keep you informed of the fix progress
- We will notify you when the vulnerability is fixed

## Disclosure Policy

- We will coordinate disclosure with you
- We will acknowledge your contribution in public disclosures
- We will aim to release fixes within 30 days

## Security Best Practices

When using BugBounty MCP Server:

1. **Always use safe mode** when testing targets
2. **Configure allowed targets** to restrict scanning scope
3. **Never store API keys** in version control
4. **Use environment variables** for sensitive configuration
5. **Run in isolated environments** (Docker containers) when possible
6. **Keep dependencies updated** (`pip install --upgrade -r requirements.txt`)
7. **Review network access controls** before scanning external targets

## Safe Mode

BugBounty MCP Server includes a safe mode that:
- Restricts targets to a configured allowed list
- Prevents destructive operations
- Enables rate limiting by default
- Logs all operations for audit

Enable safe mode by setting `safe_mode: true` in your configuration.

## API Key Security

Never commit API keys to version control. Use the `.env` file:

```bash
SHODAN_API_KEY=your_key_here
CENSYS_API_ID=your_id_here
GITHUB_TOKEN=your_token_here
```

The `.env` file should be added to `.gitignore`.
