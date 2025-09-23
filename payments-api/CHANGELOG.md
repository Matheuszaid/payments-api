# Changelog

All notable changes to the Payments Reliability API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0-rc] - 2025-09-23

### Added
- **Production-Ready Docker Support**: Multi-stage Dockerfile with non-root user and HEALTHCHECK
- **Database Migrations**: Complete Alembic integration with `make db-upgrade` command
- **Comprehensive Documentation**: OpenAPI spec, static docs, and Grafana dashboard
- **Docker Compose Setup**: Multi-profile deployment with optional Redis and PostgreSQL
- **Dependency Management**: Renovate configuration for automated dependency updates
- **Usage Examples**: Ready-to-use curl scripts and Postman collection
- **Live API Documentation**: Static HTML docs linked from README

### Enhanced
- **Performance Testing**: Updated k6 tests with realistic thresholds (P95 < 500ms achieved)
- **Security Scanning**: Explicit CVE counts in reports (0 high/critical vulnerabilities)
- **Make Verify**: Compact summary output with non-zero exit codes on failure
- **Prometheus Metrics**: Documented exact metric names with sample output
- **README Structure**: Added Usage Examples section and clarified PM2 vs Docker deployment

### Fixed
- **Dead Code Removal**: Cleaned up unused variables in metrics.py
- **Badge Links**: Updated to real repository URLs (Matheuszaid/payments-api)
- **Performance Numbers**: Corrected latency metrics to reflect working endpoints

### Security
- **Container Hardening**: Non-root Docker container with security best practices
- **Vulnerability Scanning**: Zero high/critical CVEs across all security tools
- **Dependency Updates**: Automated dependency management with Renovate

### Infrastructure
- **Deployment Options**: Clear guidance on PM2 vs Docker usage patterns
- **Health Monitoring**: Docker HEALTHCHECK and comprehensive observability
- **Database Support**: Both SQLite (default) and PostgreSQL configurations

## [0.1.0] - Previous Release

### Added
- Initial webhook processing for Stripe and PayPal
- Basic API endpoints and database models
- Test suite and CI/CD pipeline
- PM2 configuration for production deployment

---

**Migration Guide**: This release includes breaking changes to deployment patterns.
See README.md for updated deployment instructions using Docker Compose or PM2.

**Security**: All dependencies have been scanned and are free of high/critical vulnerabilities.

**Performance**: Achieves P95 latency < 500ms for core API endpoints under normal load.