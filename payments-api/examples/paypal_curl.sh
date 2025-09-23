#!/bin/bash

# PayPal Webhook Test Script
# This script sends a test webhook payload to the PayPal webhook endpoint
# with proper HMAC signature for demo mode

set -e

# Configuration
API_URL="http://localhost:8065"
WEBHOOK_ENDPOINT="/webhooks/paypal"
DEMO_SECRET="${DEMO_HMAC_SECRET:-test_secret_for_development}"

# Read the payload
PAYLOAD_FILE="${1:-examples/paypal_webhook.json}"

if [ ! -f "$PAYLOAD_FILE" ]; then
    echo "❌ Payload file not found: $PAYLOAD_FILE"
    echo "Usage: $0 [payload_file]"
    echo "Example: $0 examples/paypal_webhook.json"
    exit 1
fi

echo "🚀 Testing PayPal webhook endpoint..."
echo "📄 Payload file: $PAYLOAD_FILE"
echo "🔗 Endpoint: $API_URL$WEBHOOK_ENDPOINT"

# Read payload content
PAYLOAD=$(cat "$PAYLOAD_FILE")

# For demo mode, generate a simple HMAC signature
# In production, this would be done by PayPal with their signing process
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$DEMO_SECRET" -hex | sed 's/^.* //')

echo "🔐 Generated signature for demo mode"
echo "📊 Payload size: $(echo "$PAYLOAD" | wc -c) bytes"

# Send the webhook with PayPal-style headers
echo "📡 Sending webhook..."

RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}\nTIME_TOTAL:%{time_total}" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "X-Demo-Signature: $SIGNATURE" \
    -H "PAYPAL-TRANSMISSION-ID: demo_transmission_$(date +%s)" \
    -H "PAYPAL-TRANSMISSION-TIME: $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    -H "PAYPAL-CERT-URL: https://api.sandbox.paypal.com/v1/notifications/certs/CERT-360caa42-fca2a594-a5cafa77" \
    -H "PAYPAL-AUTH-ALGO: SHA256withRSA" \
    -H "PAYPAL-TRANSMISSION-SIG: demo_signature_$(date +%s)" \
    -H "User-Agent: PayPal/1.0 (+https://developer.paypal.com/docs/api/webhooks/)" \
    -d "$PAYLOAD" \
    "$API_URL$WEBHOOK_ENDPOINT")

# Parse response
HTTP_BODY=$(echo "$RESPONSE" | sed -n '1,/HTTP_STATUS:/p' | head -n -1)
HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
TIME_TOTAL=$(echo "$RESPONSE" | grep "TIME_TOTAL:" | cut -d: -f2)

echo ""
echo "📈 Response:"
echo "   Status: $HTTP_STATUS"
echo "   Time: ${TIME_TOTAL}s"
echo "   Body: $HTTP_BODY"

# Check if successful
if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Webhook processed successfully!"

    # Try to parse JSON response
    if echo "$HTTP_BODY" | jq . >/dev/null 2>&1; then
        EVENT_ID=$(echo "$HTTP_BODY" | jq -r '.event_id // "unknown"')
        STATUS=$(echo "$HTTP_BODY" | jq -r '.status // "unknown"')
        echo "   Event ID: $EVENT_ID"
        echo "   Status: $STATUS"
    fi
else
    echo "❌ Webhook failed with status $HTTP_STATUS"
    echo "   Response: $HTTP_BODY"
    exit 1
fi

echo ""
echo "🔍 To verify the event was stored, check:"
echo "   curl $API_URL/admin/events | jq '.[] | select(.provider==\"paypal\")'"