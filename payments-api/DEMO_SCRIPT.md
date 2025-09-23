# 🎬 DEMO SCRIPT - PAYMENTS API (5-7 minutes)

## Preparation (30 seconds)

```bash
# Terminal setup
cd payments-api
. .venv/bin/activate

# Ensure clean state
docker-compose down
rm -f payments.db*
```

## 1. Infrastructure Health Check (1 minute)

```bash
# Start the application with Docker
echo "🚀 Starting Payments API with Docker..."
docker-compose up -d

# Wait for startup
sleep 5

# Health check
echo "💓 Checking application health..."
curl -s http://localhost:8065/health | jq

# Readiness check with dependencies
echo "✅ Checking readiness..."
curl -s http://localhost:8065/ready | jq
```

**Expected Output:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-23T...",
  "version": "0.2.0-rc"
}
```

## 2. Metrics Baseline (1 minute)

```bash
# Check initial metrics
echo "📊 Baseline metrics..."
curl -s http://localhost:8065/metrics | grep -E "(http_requests_total|payments_api_build_info)"

# JSON metrics for debugging
echo "📈 JSON metrics view..."
curl -s http://localhost:8065/metrics/json | jq
```

**Highlight:**
- Zero HTTP requests initially
- Build info shows correct version
- Prometheus format ready for monitoring

## 3. Stripe Webhook Processing (2 minutes)

```bash
# Show webhook example
echo "📝 Stripe webhook payload:"
cat examples/stripe_webhook.json | jq

# Send Stripe webhook (will fail - no valid signature)
echo "🔒 Testing signature verification..."
curl -X POST http://localhost:8065/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: invalid" \
  -d @examples/stripe_webhook.json

# Send with demo signature (for demo purposes)
echo "✅ Sending valid demo webhook..."
./examples/stripe_curl.sh examples/stripe_webhook.json
```

**Expected Output:**
- First request: `{"status": "error", "message": "Invalid signature"}`
- Second request: `{"status": "processed", "event_id": "evt_..."}`

## 4. Idempotency Demonstration (1 minute)

```bash
# Send the same webhook again
echo "🔄 Testing idempotency - sending same webhook..."
./examples/stripe_curl.sh examples/stripe_webhook.json

# Show duplicate detection
echo "🎯 Second call should show 'duplicate ignored'..."
```

**Expected Output:**
```json
{
  "status": "duplicate",
  "message": "Event already processed",
  "event_id": "evt_1234567890"
}
```

## 5. Metrics After Processing (1 minute)

```bash
# Check updated metrics
echo "📊 Metrics after webhook processing..."
curl -s http://localhost:8065/metrics | grep -E "(http_requests_total|webhook_events_total)"

# Show event storage
echo "🗄️ Stored events..."
curl -s "http://localhost:8065/admin/events?limit=5" | jq
```

**Highlight:**
- HTTP request counters incremented
- Webhook processing metrics recorded
- Events persisted in database

## 6. PayPal Webhook Demo (1 minute)

```bash
# PayPal webhook example
echo "💙 PayPal webhook demo..."
./examples/paypal_curl.sh examples/paypal_webhook.json

# Show multi-provider support
echo "🌍 Multi-provider event list..."
curl -s "http://localhost:8065/admin/events?provider=paypal&limit=3" | jq
```

## 7. Operational Features (1 minute)

```bash
# Reconciliation summary
echo "📋 Reconciliation summary (last 24h)..."
curl -s "http://localhost:8065/reconciliation/summary?hours_back=24" | jq

# Container status and logs
echo "🐳 Container health..."
docker-compose ps
docker-compose logs --tail=5 payments-api
```

## 8. Cleanup & Architecture Overview (30 seconds)

```bash
# Stop demo environment
docker-compose down

echo "🏗️ Architecture highlights demonstrated:"
echo "  ✅ Signature verification with security"
echo "  ✅ Idempotency preventing duplicate processing"
echo "  ✅ Multi-provider support (Stripe + PayPal)"
echo "  ✅ Comprehensive observability"
echo "  ✅ Production-ready containerization"
```

## Key Demo Points to Emphasize

1. **Security First**: Signature verification prevents unauthorized webhooks
2. **Reliability**: Idempotency ensures no duplicate processing
3. **Observability**: Metrics and logging for production monitoring
4. **Multi-provider**: Supports both Stripe and PayPal with unified interface
5. **Production Ready**: Docker, health checks, proper error handling

## Troubleshooting Tips

**If containers fail to start:**
```bash
# Check port conflicts
docker-compose logs
# Try different port
APP_PORT=8070 docker-compose up -d
```

**If webhooks fail:**
```bash
# Check application logs
docker-compose logs payments-api
# Verify demo environment variables
grep DEMO_HMAC .env
```

**If metrics don't update:**
```bash
# Force refresh metrics endpoint
curl http://localhost:8065/metrics/json
# Check application startup logs
```

## Demo Flow Summary

1. **Infrastructure** → Health & readiness checks
2. **Security** → Signature verification demonstration
3. **Processing** → Successful webhook handling
4. **Reliability** → Idempotency in action
5. **Observability** → Metrics and event tracking
6. **Scalability** → Multi-provider support

**Total Time:** 5-7 minutes with natural explanations