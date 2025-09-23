module.exports = {
  apps: [{
    name: 'payments-api',
    script: 'uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port ${APP_PORT:-8065}',
    interpreter: 'python',
    instances: 1,
    exec_mode: 'fork',

    // Environment variables
    env: {
      NODE_ENV: 'production',
      APP_ENV: 'prod',
      APP_PORT: process.env.APP_PORT || 8065,
      DATABASE_URL: process.env.DATABASE_URL || 'sqlite+aiosqlite:///./payments.db',
      STRIPE_SIGNING_SECRET: process.env.STRIPE_SIGNING_SECRET || '',
      PAYPAL_MODE: process.env.PAYPAL_MODE || 'sandbox',
      PAYPAL_WEBHOOK_ID: process.env.PAYPAL_WEBHOOK_ID || '',
      PAYPAL_CLIENT_ID: process.env.PAYPAL_CLIENT_ID || '',
      PAYPAL_CLIENT_SECRET: process.env.PAYPAL_CLIENT_SECRET || '',
      DEMO_HMAC_SECRET: process.env.DEMO_HMAC_SECRET || '',
      DLQ_BACKEND: process.env.DLQ_BACKEND || 'db',
      REDIS_URL: process.env.REDIS_URL || 'redis://localhost:6379/0'
    },

    // Development environment
    env_development: {
      NODE_ENV: 'development',
      APP_ENV: 'dev',
      DATABASE_URL: 'sqlite+aiosqlite:///./payments-dev.db'
    },

    // Logging
    log_file: './logs/payments-api.log',
    out_file: './logs/payments-api-out.log',
    error_file: './logs/payments-api-error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',

    // Process management
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',

    // Advanced options
    restart_delay: 1000,
    max_restarts: 10,
    min_uptime: '10s',

    // Graceful shutdown
    kill_timeout: 3000,
    wait_ready: true,
    listen_timeout: 3000,

    // Health monitoring
    health_check_grace_period: 3000,
    health_check_fatal_error_exit: true
  }]
};