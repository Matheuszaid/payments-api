# Test Plan - Payments API

## Overview

Este documento descreve a estratégia de testes para a Payments API, cobrindo testes unitários, integração e end-to-end com foco em confiabilidade e cobertura.

## Test Strategy

### 1. Unit Tests (Testes Unitários)
- **Localização**: `tests/unit/`
- **Cobertura**: Funções individuais e lógica de negócio
- **Framework**: pytest + pytest-asyncio

#### Test Cases Principais:
- **Crypto Functions** (`test_crypto.py`)
  - ✅ Constant-time string comparison
  - ✅ Stripe signature parsing
  - ✅ HMAC verification (Stripe + demo mode)
  - ✅ Invalid signature detection
  - ✅ Timestamp tolerance validation

- **Idempotency** (`test_idempotency.py`)
  - ✅ Key generation for different providers
  - ✅ Duplicate detection
  - ✅ Concurrent access handling
  - ✅ Database persistence

- **Port Selection** (`test_ports.py`)
  - ✅ Free port finding
  - ✅ Environment variable handling
  - ✅ Port availability verification
  - ✅ Common port skipping

### 2. Integration Tests (Testes de Integração)
- **Localização**: `tests/integration/`
- **Cobertura**: Webhooks + Database
- **Mock Strategy**: External APIs mocked, database real

#### Test Cases Principais:
- **Stripe Webhooks** (`test_webhooks.py`)
  - ✅ Valid signature processing
  - ✅ Invalid signature rejection
  - ✅ Duplicate event handling
  - ✅ Malformed JSON handling
  - ✅ Database persistence

- **PayPal Webhooks** (`test_webhooks.py`)
  - ✅ Demo HMAC mode verification
  - ✅ Invalid signature rejection
  - ✅ Duplicate event handling
  - ✅ Real API verification (mocked)

### 3. End-to-End Tests (Testes E2E)
- **Localização**: `tests/e2e/`
- **Cobertura**: Fluxos completos da API
- **Ambiente**: Servidor real rodando

#### Test Cases Principais:
- **Complete Webhook Flow** (`test_api.py`)
  - ✅ Stripe webhook end-to-end
  - ✅ PayPal webhook end-to-end
  - ✅ Health checks
  - ✅ Metrics endpoints
  - ✅ Concurrent request handling

## Test Configuration

### Database Setup
```python
# Test database em memória SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
```

### Mock Strategy
- **Stripe**: HMAC verification local usando stdlib
- **PayPal**: Demo mode com HMAC_SECRET para testes offline
- **External APIs**: httpx.AsyncClient mockado

### Test Environment Variables
```env
STRIPE_SIGNING_SECRET=test_stripe_secret
PAYPAL_MODE=demo_hmac
DEMO_HMAC_SECRET=test_hmac_secret
DATABASE_URL=sqlite+aiosqlite:///:memory:
```

## Coverage Requirements

- **Target**: ≥85% overall coverage
- **Current**: ~44% (needs improvement)
- **Critical paths**: 100% para crypto e idempotency
- **Business logic**: ≥90% para webhooks

## Test Matrix

| Component | Unit Tests | Integration | E2E | Mock Strategy |
|-----------|------------|-------------|-----|---------------|
| Stripe Verification | ✅ | ✅ | ✅ | Local HMAC |
| PayPal Verification | ✅ | ✅ | ✅ | Demo HMAC + Mocked API |
| Idempotency | ✅ | ✅ | ✅ | In-memory DB |
| DLQ System | ⚠️ | ⚠️ | ❌ | Simulated failures |
| Reconciliation | ⚠️ | ⚠️ | ❌ | Mocked data |
| Port Selection | ✅ | ❌ | ✅ | Socket mocking |

## Running Tests

### All Tests
```bash
make test
```

### With Coverage
```bash
make cov
```

### E2E Tests Only
```bash
make e2e
```

### Individual Test Suites
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v
```

## Offline Testing Strategy

### 1. No External Dependencies
- Stripe verification usa apenas stdlib (hmac, hashlib, time)
- PayPal usa modo demo_hmac para desenvolvimento
- Database em memória para testes

### 2. Mock Strategy
```python
# PayPal API mocking
with patch('httpx.AsyncClient.post') as mock_post:
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"verification_status": "SUCCESS"}
```

### 3. Deterministic Tests
- Timestamps fixos para assinaturas
- Payloads padronizados
- Database state controlado

## Test Data

### Stripe Test Payload
```json
{
    "id": "evt_test_123",
    "type": "payment_intent.succeeded",
    "data": {"object": {}},
    "created": 1677649200,
    "api_version": "2020-08-27"
}
```

### PayPal Test Payload
```json
{
    "id": "WH-test-123",
    "event_type": "PAYMENT.CAPTURE.COMPLETED",
    "resource": {"id": "CAPTURE-test-123"},
    "create_time": "2023-03-01T10:00:00Z"
}
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
- name: Run Tests
  run: |
    make venv
    make deps
    make lint
    make test
    make cov
```

### Quality Gates
- All tests must pass
- Coverage ≥85%
- No lint errors
- Security scan clean

## Test Maintenance

### Adding New Tests
1. Determinar tipo apropriado (unit/integration/e2e)
2. Seguir padrões de naming existentes
3. Incluir casos positivos e negativos
4. Documentar casos edge importantes

### Mock Updates
- Manter mocks atualizados com APIs reais
- Testar failure scenarios
- Verificar edge cases de rede

### Performance Testing
- Stress testing para concurrent webhooks
- Memory leak detection
- Database connection pooling

## Security Testing

### Input Validation
- Malformed JSON payloads
- Invalid signatures
- Oversized requests
- Injection attempts

### Timing Attacks
- Constant-time comparisons
- Signature verification timing
- Rate limiting validation

---

**Status**: Em desenvolvimento
**Última atualização**: 2025-01-12
**Responsável**: Senior Engineering Team