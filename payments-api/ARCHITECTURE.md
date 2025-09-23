# Architecture Documentation

## Overview

The Payments Reliability API is designed as a production-grade microservice for processing webhook events from payment providers (Stripe and PayPal) with emphasis on reliability, security, and observability.

## Design Principles

- **Reliability First**: Idempotency, DLQ, retry mechanisms
- **Security by Design**: Signature verification, constant-time comparisons, PII protection
- **Observability**: Structured logging, metrics, health checks
- **Simplicity**: Minimal dependencies, clear separation of concerns
- **Production Ready**: PM2 process management, Nginx integration

## System Architecture

```
                                 Internet
                                    │
                            ┌───────▼────────┐
                            │     Nginx      │
                            │  (Rate Limit,  │
                            │   SSL, etc.)   │
                            └───────┬────────┘
                                    │
                            ┌───────▼────────┐
                            │   FastAPI      │
                            │  Application   │
                            │                │
                            │ ┌────────────┐ │
                            │ │  Webhook   │ │
                            │ │ Handlers   │ │
                            │ └────────────┘ │
                            │                │
                            │ ┌────────────┐ │
                            │ │   Auth &   │ │
                            │ │ Validation │ │
                            │ └────────────┘ │
                            │                │
                            │ ┌────────────┐ │
                            │ │Idempotency │ │
                            │ │  Manager   │ │
                            │ └────────────┘ │
                            └───────┬────────┘
                                    │
                        ┌───────────┼───────────┐
                        │           │           │
                ┌───────▼───┐  ┌────▼────┐ ┌───▼────┐
                │ Database  │  │   DLQ   │ │  Jobs  │
                │(SQLite/PG)│  │ Worker  │ │ Worker │
                │           │  │         │ │        │
                │┌─────────┐│  │┌───────┐│ │┌──────┐│
                ││Events   ││  ││Retry  ││ ││Recon ││
                ││Idem.Keys││  ││Logic  ││ ││Job   ││
                ││DLQ Msgs ││  ││       ││ ││      ││
                │└─────────┘│  │└───────┘│ │└──────┘│
                └───────────┘  └─────────┘ └────────┘
```

## Component Details

### 1. HTTP Layer (Nginx)

**Purpose**: Reverse proxy, SSL termination, rate limiting, security headers

**Key Features**:
- Rate limiting by endpoint type
- SSL/TLS termination
- Security headers injection
- Request/response logging
- Health check proxying

**Configuration**:
- Webhook endpoints: Higher rate limits for legitimate traffic
- Admin endpoints: Restricted access, moderate limits
- Health endpoints: No rate limiting
- Metrics: IP-restricted access

### 2. Application Layer (FastAPI)

**Purpose**: Business logic, API routing, request/response handling

**Key Components**:

#### Webhook Handlers (`app/webhooks/`)
- **Stripe Handler**: Official signature verification, event parsing
- **PayPal Handler**: Real + demo verification modes, OAuth token management

#### Configuration Management (`app/config.py`)
- Environment-based configuration
- Secret masking for logs
- Validation and defaults

#### Database Layer (`app/db.py`)
- Async SQLAlchemy with connection pooling
- Transaction management
- Health check capabilities

#### Utilities (`app/utils/`)
- **Crypto**: Constant-time signature verification
- **Idempotency**: Duplicate detection and handling
- **Ports**: Automatic port selection

### 3. Data Layer

**Purpose**: Persistent storage for events, idempotency keys, DLQ messages

**Schema Design**:

```sql
-- Idempotency tracking
CREATE TABLE idempotency_keys (
    id INTEGER PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_key (key)
);

-- Event storage
CREATE TABLE payment_events (
    id INTEGER PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    event_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload_json TEXT NOT NULL,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, event_id),
    INDEX idx_provider_event (provider, event_id),
    INDEX idx_received_at (received_at)
);

-- Dead Letter Queue
CREATE TABLE dlq_messages (
    id INTEGER PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    event_id VARCHAR(255) NOT NULL,
    payload_json TEXT NOT NULL,
    error_kind VARCHAR(100) NOT NULL,
    attempts INTEGER DEFAULT 0,
    next_retry_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_next_retry (next_retry_at)
);

-- Reconciliation tracking
CREATE TABLE reconciliation_log (
    id INTEGER PRIMARY KEY,
    provider VARCHAR(50),
    event_id VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    details_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
);
```

### 4. Background Workers

#### DLQ Retry Worker (`app/jobs/retry_worker.py`)

**Purpose**: Process failed webhook events with exponential backoff

**Algorithm**:
1. Poll database for messages due for retry
2. Respect concurrency limits (semaphore)
3. Exponential backoff: 2^attempts minutes (max 60 min)
4. Jitter: ±25% randomization
5. Max attempts: 5 retries

**Flow**:
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Failed    │───▶│     DLQ     │───▶│   Retry     │
│  Webhook    │    │   Storage   │    │   Worker    │
│ Processing  │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       │            ┌──────▼──────┐           │
       │            │ Exponential │           │
       │            │  Backoff    │           │
       └────────────┤ Calculator  │◀──────────┘
                    └─────────────┘
```

#### Reconciliation Job (`app/jobs/reconciliation.py`)

**Purpose**: Generate reports on event processing for monitoring

**Features**:
- Event counts by provider and type
- Anomaly detection (duplicates, high frequency)
- Time-window analysis
- Report persistence

### 5. Security Architecture

#### Signature Verification

**Stripe**:
- HMAC-SHA256 with timestamp tolerance
- Constant-time signature comparison
- Replay attack prevention

**PayPal**:
- Production: OAuth + verification API
- Development: Demo HMAC for offline testing
- Header validation and transmission verification

#### Data Protection

- PII masking in logs
- Secret scrubbing in error messages
- Constant-time string comparisons
- Input validation and sanitization

### 6. Monitoring & Observability

#### Logging Strategy

```json
{
  "timestamp": "2024-01-01T10:00:00Z",
  "level": "INFO",
  "message": "Webhook processed successfully",
  "extra": {
    "request_id": "req_123",
    "provider": "stripe",
    "event_id": "evt_456",
    "event_type": "payment_intent.succeeded",
    "duration_ms": 150,
    "outcome": "processed"
  }
}
```

#### Metrics Collection

- Request counters by endpoint and outcome
- Processing latency histograms
- DLQ depth and retry counts
- Error rates by type and provider

#### Health Checks

- **Liveness** (`/health`): Basic service availability
- **Readiness** (`/ready`): Dependency health (database, external APIs)

## Deployment Architecture

### Development

```
Developer → localhost:8065 → SQLite
```

### Production

```
Internet → Nginx:443 → FastAPI:8065 → PostgreSQL
                                   └── Redis (optional)
```

### Process Management

- **PM2**: Process monitoring, auto-restart, log management
- **Systemd**: Service management and auto-start
- **Docker**: Containerization (optional)

## Scalability Considerations

### Horizontal Scaling

- Stateless application design
- Database connection pooling
- Shared DLQ storage (Redis)
- Load balancer support

### Vertical Scaling

- Async I/O for database operations
- Connection pooling
- Memory-efficient data structures
- Configurable worker concurrency

### Performance Optimizations

- Database indexes on frequently queried columns
- Efficient JSON serialization
- Minimal dependencies
- Request/response streaming for large payloads

## Data Flow Diagrams

### Successful Webhook Processing

```
┌─────────┐   ┌──────────┐   ┌─────────────┐   ┌──────────┐   ┌──────────┐
│ Webhook │──▶│  Nginx   │──▶│   FastAPI   │──▶│   Auth   │──▶│   Idem   │
│Provider │   │          │   │             │   │  Check   │   │  Check   │
└─────────┘   └──────────┘   └─────────────┘   └──────────┘   └──────────┘
                                   │                               │
                                   ▼                               ▼
                            ┌─────────────┐                ┌──────────┐
                            │   Store     │◀───────────────│   New    │
                            │   Event     │                │  Event?  │
                            └─────────────┘                └──────────┘
                                   │                               │
                                   ▼                               ▼
                            ┌─────────────┐                ┌──────────┐
                            │   Return    │                │  Return  │
                            │  Success    │                │Duplicate │
                            └─────────────┘                └──────────┘
```

### Failed Webhook Processing

```
┌─────────┐   ┌──────────┐   ┌─────────────┐   ┌──────────┐
│ Webhook │──▶│  Nginx   │──▶│   FastAPI   │──▶│Processing│
│Provider │   │          │   │             │   │  Error   │
└─────────┘   └──────────┘   └─────────────┘   └──────────┘
                                   │                 │
                                   ▼                 ▼
                            ┌─────────────┐   ┌──────────┐
                            │  Add to DLQ │◀──│   Log    │
                            │             │   │  Error   │
                            └─────────────┘   └──────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │Retry Worker │
                            │  Processes  │
                            └─────────────┘
```

## Technology Choices

### Framework: FastAPI

**Rationale**:
- High performance async framework
- Automatic OpenAPI documentation
- Type hints and validation
- Dependency injection system
- Mature ecosystem

### Database: SQLAlchemy + SQLite/PostgreSQL

**Rationale**:
- Async support for high concurrency
- ORM abstraction with raw SQL flexibility
- Migration management with Alembic
- Connection pooling and health checks
- Multi-database support (dev/prod)

### Testing: PyTest

**Rationale**:
- Excellent async support
- Fixture system for test data
- Parametrized testing
- Coverage integration
- Mock and patching capabilities

### Process Management: PM2

**Rationale**:
- Zero-downtime deployments
- Log management and rotation
- Process monitoring and restart
- Load balancing across instances
- Development and production modes

## Future Enhancements

### Short Term

- Redis integration for DLQ backend
- More sophisticated rate limiting
- Additional payment provider support
- Enhanced metrics and alerting

### Medium Term

- Multi-region deployment support
- Advanced anomaly detection
- Performance optimization
- Container deployment options

### Long Term

- Event sourcing architecture
- Real-time analytics dashboard
- Machine learning for fraud detection
- GraphQL API support