# Payments Reliability API

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/Matheuszaid/payments-api/actions)
[![Coverage](https://img.shields.io/badge/Coverage-92%25-brightgreen)](https://github.com/Matheuszaid/payments-api)
[![Security](https://img.shields.io/badge/Security-Bandit%20%7C%20Safety-green)](https://github.com/Matheuszaid/payments-api/security)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009485)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-blue)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**A production-grade webhook processing service for Stripe and PayPal payments with robust signature verification, idempotency, DLQ retry mechanisms, and comprehensive monitoring.**

**Why it matters in payments:**
- **Replay Protection**: Constant-time signature verification prevents replay attacks
- **Idempotency**: Duplicate detection prevents double-processing critical payment events
- **Observability**: Real-time metrics and reconciliation detect payment flow anomalies
- **Graceful Failure**: DLQ retry with exponential backoff ensures no webhook is lost

## Features

- ✅ **Webhook Processing**: Stripe & PayPal webhook handlers with signature verification
- ✅ **Security**: Constant-time signature verification, PII masking, input validation
- ✅ **Idempotency**: Duplicate event detection and handling
- ✅ **Reliability**: Dead Letter Queue (DLQ) with exponential backoff retry
- ✅ **Monitoring**: Health checks, metrics, reconciliation reports
- ✅ **Production Ready**: PM2 process management, Nginx configuration
- ✅ **Testing**: Comprehensive unit, integration, and E2E test suite
- ✅ **Documentation**: Complete API documentation and runbooks

## Quick Start

### Prerequisites

- Python 3.11+
- pip or poetry
- SQLite (default) or PostgreSQL
- Optional: Redis for DLQ backend

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd payments-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make deps
# or: pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### Configuration

Set the following environment variables in `.env`:

```env
# Application
APP_ENV=dev
APP_PORT=8065  # Optional: auto-selects from 8065-8099 if not set

# Database
DATABASE_URL=sqlite+aiosqlite:///./payments.db

# Stripe
STRIPE_SIGNING_SECRET=whsec_your_stripe_signing_secret

# PayPal
PAYPAL_MODE=sandbox  # live, sandbox, or demo_hmac
PAYPAL_WEBHOOK_ID=your_webhook_id
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
DEMO_HMAC_SECRET=demo_secret_for_testing

# DLQ (optional)
DLQ_BACKEND=db  # or redis
REDIS_URL=redis://localhost:6379/0
```

### Development

```bash
# Start development server (auto-selects free port)
make dev

# Run tests
make test

# Run with coverage
make cov

# Lint code
make lint

# Run E2E tests
make e2e
```

### Production Deployment

#### Option 1: PM2 (Bare Metal/VPS)

For bare metal servers or VPS environments:

```bash
# Install PM2 globally
npm install -g pm2

# Start with PM2
make pm2-start

# Check status
pm2 status

# View logs
pm2 logs payments-api

# Stop service
make pm2-stop
```

#### Option 2: Docker (Containerized)

For containerized deployments:

```bash
# Simple deployment
docker-compose up -d

# With Redis DLQ backend
docker-compose --profile redis up -d

# With PostgreSQL database
docker-compose --profile postgres up -d

# Full stack (PostgreSQL + Redis)
docker-compose --profile redis --profile postgres up -d
```

**When to use which:**
- **PM2**: Direct server deployment, easier debugging, systemd integration
- **Docker**: Container orchestration, easier scaling, isolated environments

## Port Selection

The application automatically selects a free port from the range 8065-8099, avoiding common development ports (3000, 5173, 8000, 8080, 9000). You can override this by setting `APP_PORT` in the environment.

```bash
# Auto-select port
make dev

# Use specific port
APP_PORT=8888 make dev
```

## Usage Examples

The `examples/` directory contains ready-to-use scripts and payloads:

```bash
# Test Stripe webhook
./examples/stripe_curl.sh examples/stripe_webhook.json

# Test PayPal webhook
./examples/paypal_curl.sh examples/paypal_webhook.json

# Import Postman collection
# File: examples/postman_collection.json
```

### Prerequisites for Examples
Ensure your `.env` file has:
```env
DEMO_HMAC_SECRET=test_secret_for_development
PAYPAL_MODE=demo_hmac
```

## API Endpoints

### Webhooks

```bash
# Stripe webhook
curl -X POST http://localhost:8065/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: t=1234567890,v1=signature_here" \
  -d '{"id":"evt_123","type":"payment_intent.succeeded","data":{}}'

# PayPal webhook (demo HMAC mode)
curl -X POST http://localhost:8065/webhooks/paypal \
  -H "Content-Type: application/json" \
  -H "X-Demo-Signature: hmac_signature_here" \
  -d '{"id":"WH-123","event_type":"PAYMENT.CAPTURE.COMPLETED","resource":{}}'
```

### Health & Monitoring

```bash
# Health check
curl http://localhost:8065/health

# Readiness check
curl http://localhost:8065/ready

# Metrics
curl http://localhost:8065/metrics

# Reconciliation summary
curl http://localhost:8065/reconciliation/summary?hours_back=24
```

### Admin

```bash
# List recent events
curl http://localhost:8065/admin/events?limit=10

# Filter by provider
curl http://localhost:8065/admin/events?provider=stripe
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Stripe/PayPal │───▶│   Payments API  │───▶│    Database     │
│    Webhooks     │    │                 │    │   (SQLite/PG)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │                 │    │                 │
                       │   DLQ Worker    │    │  Reconciliation │
                       │  (Retry Logic)  │    │      Job        │
                       │                 │    │                 │
                       └─────────────────┘    └─────────────────┘
```

## Observability & Monitoring

### Prometheus Metrics
The API exposes comprehensive metrics at `/metrics`:

**Key Metrics Available:**
- `payments_api_build_info{environment,name,version}` - Application build information
- `http_requests_total{endpoint,method,status_code}` - Total HTTP requests processed
- `http_request_duration_seconds{endpoint,method}` - Request duration histogram
- `webhook_events_total{provider,event_type,status}` - Total webhook events processed
- `webhook_processing_duration_seconds{provider,event_type}` - Webhook processing time
- `webhook_signature_validations_total{provider,result}` - Signature validation metrics
- `database_operations_total{operation,table,status}` - Database operation metrics
- `application_info{environment,version}` - Application status information

**Sample Metrics Output:**
```
payments_api_build_info{environment="production",name="payments-api",version="0.2.0-rc"} 1.0
http_requests_total{endpoint="/health",method="GET",status_code="200"} 306.0
```

### Grafana Dashboard
Pre-configured dashboard with:
- P50/P95/P99 latency panels
- Error rate monitoring
- Request throughput tracking
- DLQ backlog visualization
- Health status indicators

```bash
# Check observability configuration
make observability
```

**Grafana Dashboard Import:**
1. Open Grafana UI
2. Go to "+" → "Import"
3. Upload the file: `grafana/dashboard.json`
4. Configure data source (Prometheus)
5. Click "Import"

The dashboard includes comprehensive monitoring for:
- Request latency (P50/P95/P99)
- Error rates by endpoint
- Webhook processing metrics
- Database operation performance

### Distributed Tracing
- Request ID generation (`x-request-id`)
- Trace ID propagation (`x-trace-id`, `traceparent`)
- Structured logging with trace context
- Custom log formatter with trace/request IDs

### Performance Benchmarks
Latest k6 performance test results (working endpoints):
- **P95 Latency**: 397.95ms ✅ (meets <500ms threshold)
- **P50 Latency**: 95.33ms
- **P90 Latency**: 322.08ms
- **Throughput**: 2.67 req/s (successful requests)
- **Success Rate**: 100% (health/metrics/docs endpoints)
- **Test Duration**: 30s smoke test with 5 VUs

## Testing

### Test Coverage: 92%
The test suite includes:

- **Unit Tests**: Core logic, crypto functions, utilities
- **Integration Tests**: Database operations, webhook processing
- **E2E Tests**: Full API flows, real HTTP requests
- **Performance Tests**: k6 load testing with thresholds

```bash
# Run all tests
make test

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# With coverage report
make cov

# Performance testing
make perf

# Complete verification suite (returns non-zero on failure)
make verify

# Expected output format:
# ✅ VERIFICATION SUMMARY: ALL CHECKS PASSED
#    Tests: PASSED (92%) | Security: 0 CVEs | Docker: PASSED
```

## Nginx Setup

Copy the Nginx configuration and modify as needed:

```bash
# Copy configuration
sudo cp nginx/payments-api.conf.example /etc/nginx/sites-available/payments-api

# Update domain and SSL certificates in the file
sudo nano /etc/nginx/sites-available/payments-api

# Enable site
sudo ln -s /etc/nginx/sites-available/payments-api /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Security Considerations

- All webhook signatures are verified using constant-time comparison
- PII data is masked in logs
- Input validation on all endpoints
- Rate limiting configured in Nginx
- HTTPS enforced in production
- Secrets never logged or exposed

## Monitoring & Observability

- Structured JSON logging
- Health and readiness endpoints
- Metrics collection
- Error tracking
- Performance monitoring
- Reconciliation reports

## Development Commands

```bash
make venv          # Create virtual environment
make deps          # Install dependencies
make dev           # Run development server
make test          # Run all tests
make lint          # Lint code
make cov           # Run tests with coverage
make e2e           # Run E2E tests
make pm2-start     # Start with PM2
make pm2-stop      # Stop PM2 process
make docs          # Generate static API documentation
make db-upgrade    # Run database migrations
```

## Database Migrations

The project uses Alembic for database migrations:

```bash
# Run migrations to latest version
make db-upgrade

# Create new migration (after model changes)
alembic revision --autogenerate -m "Add new table"

# Database URLs supported:
# SQLite: sqlite+aiosqlite:///./payments.db (default)
# PostgreSQL: postgresql+asyncpg://user:pass@localhost/dbname
```

## Live API Docs (Static)

Access the API documentation:

- **OpenAPI Spec**: [`openapi.json`](openapi.json) - Complete OpenAPI 3.0 specification
- **Interactive Docs**: [`site/index.html`](site/index.html) - Static HTML documentation
- **Generate Docs**: Run `make docs` to regenerate static documentation from the OpenAPI spec

## Troubleshooting

### Port Already in Use

The application will automatically find a free port in the range 8065-8099. If all ports are busy, you'll see an error. Set a specific port with `APP_PORT=<port>`.

### Database Connection Issues

Check your `DATABASE_URL` setting. For SQLite, ensure the directory is writable. For PostgreSQL, verify connection parameters.

### Webhook Signature Verification

- Stripe: Ensure `STRIPE_SIGNING_SECRET` matches your webhook endpoint secret
- PayPal: For production, use real verification. For development, use `PAYPAL_MODE=demo_hmac`

### PM2 Process Issues

```bash
# Check process status
pm2 status

# View logs
pm2 logs payments-api

# Restart process
pm2 restart payments-api

# Delete and recreate
pm2 delete payments-api
make pm2-start
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [SECURITY.md](SECURITY.md) - Security implementation details
- [RUNBOOK.md](RUNBOOK.md) - Operations and incident response
- [TESTPLAN.md](TESTPLAN.md) - Testing strategy and coverage
- [ADRs/](ADRs/) - Architecture Decision Records

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `make lint test`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.