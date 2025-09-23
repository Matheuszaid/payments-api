import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
export const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '1m', target: 10 },   // Stay at 10 users
    { duration: '30s', target: 50 },  // Ramp up to 50 users
    { duration: '2m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.05'],   // Error rate must be below 5%
    errors: ['rate<0.05'],
  },
};

const BASE_URL = 'http://localhost:8065';

// Generate HMAC signature for demo mode
function generateDemoSignature(payload, secret) {
  // This would normally use crypto, but for k6 we'll use a simple hash
  // In real scenario, this would be proper HMAC-SHA256
  return 'demo_signature_' + Math.random().toString(36).substring(7);
}

export default function () {
  // Test 1: Health check
  let healthResponse = http.get(`${BASE_URL}/health`);
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
    'health response contains status': (r) => r.json('status') !== undefined,
  }) || errorRate.add(1);

  sleep(0.1);

  // Test 2: Stripe webhook simulation
  const stripePayload = {
    id: `evt_test_${Math.random().toString(36).substring(7)}`,
    object: 'event',
    api_version: '2020-08-27',
    created: Math.floor(Date.now() / 1000),
    data: {
      object: {
        id: `ch_test_${Math.random().toString(36).substring(7)}`,
        object: 'charge',
        amount: 2000,
        currency: 'usd',
        status: 'succeeded',
      },
    },
    type: 'charge.succeeded',
    livemode: false,
    pending_webhooks: 1,
    request: {
      id: `req_test_${Math.random().toString(36).substring(7)}`,
      idempotency_key: null,
    },
  };

  const stripeHeaders = {
    'Content-Type': 'application/json',
    'X-Demo-Signature': generateDemoSignature(JSON.stringify(stripePayload), 'test_secret'),
  };

  let stripeResponse = http.post(
    `${BASE_URL}/webhooks/stripe`,
    JSON.stringify(stripePayload),
    { headers: stripeHeaders }
  );

  check(stripeResponse, {
    'stripe webhook status is 200': (r) => r.status === 200,
    'stripe webhook processed': (r) => r.json('status') === 'ok',
  }) || errorRate.add(1);

  sleep(0.1);

  // Test 3: PayPal webhook simulation
  const paypalPayload = {
    id: `WH-test-${Math.random().toString(36).substring(7)}`,
    event_type: 'PAYMENT.CAPTURE.COMPLETED',
    create_time: new Date().toISOString(),
    resource: {
      id: `payment_${Math.random().toString(36).substring(7)}`,
      amount: {
        currency_code: 'USD',
        value: '20.00',
      },
      status: 'COMPLETED',
    },
  };

  const paypalHeaders = {
    'Content-Type': 'application/json',
    'X-Demo-Signature': generateDemoSignature(JSON.stringify(paypalPayload), 'test_secret'),
  };

  let paypalResponse = http.post(
    `${BASE_URL}/webhooks/paypal`,
    JSON.stringify(paypalPayload),
    { headers: paypalHeaders }
  );

  check(paypalResponse, {
    'paypal webhook status is 200': (r) => r.status === 200,
    'paypal webhook processed': (r) => r.json('status') === 'ok',
  }) || errorRate.add(1);

  sleep(0.1);

  // Test 4: Metrics endpoint
  let metricsResponse = http.get(`${BASE_URL}/metrics`);
  check(metricsResponse, {
    'metrics endpoint accessible': (r) => r.status === 200,
    'metrics contains prometheus format': (r) => r.body.includes('# HELP'),
  }) || errorRate.add(1);

  sleep(0.2);

  // Test 5: Documentation endpoint
  let docsResponse = http.get(`${BASE_URL}/docs`);
  check(docsResponse, {
    'docs endpoint accessible': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.1);

  // Test 6: Duplicate webhook (should be handled gracefully)
  let duplicateResponse = http.post(
    `${BASE_URL}/webhooks/stripe`,
    JSON.stringify(stripePayload),
    { headers: stripeHeaders }
  );

  check(duplicateResponse, {
    'duplicate webhook handled': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(0.3);
}

export function teardown(data) {
  console.log('Performance test completed');
  console.log('Check the reports/ directory for detailed results');
}