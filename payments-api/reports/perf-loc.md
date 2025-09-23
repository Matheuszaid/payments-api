Starting application for performance tests...
. .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8065 &
Running k6 performance tests...
k6 run perf/stripe-smoke.k6.js

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: perf/stripe-smoke.k6.js
        output: -

     scenarios: (100.00%) 1 scenario, 50 max VUs, 5m0s max duration (incl. graceful stop):
              * default: Up to 50 looping VUs for 4m30s over 5 stages (gracefulRampDown: 30s, gracefulStop: 30s)


running (0m00.7s), 01/50 VUs, 104 complete and 0 interrupted iterations
default   [   0% ] 01/50 VUs  0m00.7s/4m30.0s

running (0m01.7s), 01/50 VUs, 173 complete and 0 interrupted iterations
default   [   1% ] 01/50 VUs  0m01.7s/4m30.0s

running (0m02.7s), 01/50 VUs, 248 complete and 0 interrupted iterations
default   [   1% ] 01/50 VUs  0m02.7s/4m30.0s

running (0m05.8s), 02/50 VUs, 249 complete and 0 interrupted iterations
default   [   2% ] 02/50 VUs  0m05.8s/4m30.0s
2025-09-23 20:21:03,194 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:21:03,194 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("idempotency_keys")
2025-09-23 20:21:03,194 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-09-23 20:21:03,197 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("payment_events")
2025-09-23 20:21:03,200 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-09-23 20:21:03,201 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("dlq_messages")
2025-09-23 20:21:03,201 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-09-23 20:21:03,202 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("reconciliation_log")
2025-09-23 20:21:03,202 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-09-23 20:21:03,587 INFO sqlalchemy.engine.Engine COMMIT

running (0m06.7s), 03/50 VUs, 375 complete and 0 interrupted iterations
default   [   2% ] 03/50 VUs  0m06.7s/4m30.0s
2025-09-23 20:21:04,073 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:21:04,544 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:21:04,547 INFO sqlalchemy.engine.Engine [generated in 0.00317s] ('2025-09-23 20:21:03.983701', 5, 10, 0)
2025-09-23 20:21:04,622 INFO sqlalchemy.engine.Engine ROLLBACK

running (0m07.7s), 03/50 VUs, 449 complete and 0 interrupted iterations
default   [   3% ] 03/50 VUs  0m07.7s/4m30.0s

running (0m09.7s), 03/50 VUs, 449 complete and 0 interrupted iterations
default   [   4% ] 03/50 VUs  0m09.7s/4m30.0s
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK

running (0m10.7s), 04/50 VUs, 480 complete and 0 interrupted iterations
default   [   4% ] 04/50 VUs  0m10.7s/4m30.0s
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m11.9s), 04/50 VUs, 480 complete and 0 interrupted iterations
default   [   4% ] 04/50 VUs  0m11.9s/4m30.0s

running (0m12.9s), 04/50 VUs, 480 complete and 0 interrupted iterations
default   [   5% ] 04/50 VUs  0m12.9s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m13.7s), 05/50 VUs, 480 complete and 0 interrupted iterations
default   [   5% ] 05/50 VUs  0m13.7s/4m30.0s
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m14.7s), 05/50 VUs, 480 complete and 0 interrupted iterations
default   [   5% ] 05/50 VUs  0m14.7s/4m30.0s
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK

running (0m15.8s), 05/50 VUs, 480 complete and 0 interrupted iterations
default   [   6% ] 05/50 VUs  0m15.8s/4m30.0s
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK

running (0m16.7s), 06/50 VUs, 485 complete and 0 interrupted iterations
default   [   6% ] 06/50 VUs  0m16.7s/4m30.0s
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m17.8s), 06/50 VUs, 485 complete and 0 interrupted iterations
default   [   7% ] 06/50 VUs  0m17.8s/4m30.0s

running (0m18.7s), 06/50 VUs, 485 complete and 0 interrupted iterations
default   [   7% ] 06/50 VUs  0m18.7s/4m30.0s

running (0m19.7s), 06/50 VUs, 485 complete and 0 interrupted iterations
default   [   7% ] 06/50 VUs  0m19.7s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m20.8s), 07/50 VUs, 485 complete and 0 interrupted iterations
default   [   8% ] 07/50 VUs  0m20.8s/4m30.0s
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m21.7s), 07/50 VUs, 485 complete and 0 interrupted iterations
default   [   8% ] 07/50 VUs  0m21.7s/4m30.0s
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK

running (0m22.7s), 07/50 VUs, 485 complete and 0 interrupted iterations
default   [   8% ] 07/50 VUs  0m22.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m23.7s), 08/50 VUs, 490 complete and 0 interrupted iterations
default   [   9% ] 08/50 VUs  0m23.7s/4m30.0s
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m24.9s), 08/50 VUs, 491 complete and 0 interrupted iterations
default   [   9% ] 08/50 VUs  0m24.9s/4m30.0s
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m25.7s), 08/50 VUs, 492 complete and 0 interrupted iterations
default   [  10% ] 08/50 VUs  0m25.7s/4m30.0s

running (0m26.7s), 08/50 VUs, 492 complete and 0 interrupted iterations
default   [  10% ] 08/50 VUs  0m26.7s/4m30.0s

running (0m27.7s), 09/50 VUs, 492 complete and 0 interrupted iterations
default   [  10% ] 09/50 VUs  0m27.7s/4m30.0s
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK

running (0m28.7s), 09/50 VUs, 492 complete and 0 interrupted iterations
default   [  11% ] 09/50 VUs  0m28.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK

running (0m29.7s), 09/50 VUs, 492 complete and 0 interrupted iterations
default   [  11% ] 09/50 VUs  0m29.7s/4m30.0s
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m30.8s), 10/50 VUs, 498 complete and 0 interrupted iterations
default   [  11% ] 10/50 VUs  0m30.8s/4m30.0s
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m31.7s), 10/50 VUs, 500 complete and 0 interrupted iterations
default   [  12% ] 10/50 VUs  0m31.7s/4m30.0s
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m32.7s), 10/50 VUs, 500 complete and 0 interrupted iterations
default   [  12% ] 10/50 VUs  0m32.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m33.7s), 10/50 VUs, 501 complete and 0 interrupted iterations
default   [  12% ] 10/50 VUs  0m33.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m34.7s), 10/50 VUs, 502 complete and 0 interrupted iterations
default   [  13% ] 10/50 VUs  0m34.7s/4m30.0s
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m35.7s), 10/50 VUs, 502 complete and 0 interrupted iterations
default   [  13% ] 10/50 VUs  0m35.7s/4m30.0s
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m36.7s), 10/50 VUs, 510 complete and 0 interrupted iterations
default   [  14% ] 10/50 VUs  0m36.7s/4m30.0s

running (0m37.7s), 10/50 VUs, 512 complete and 0 interrupted iterations
default   [  14% ] 10/50 VUs  0m37.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK

running (0m38.7s), 10/50 VUs, 512 complete and 0 interrupted iterations
default   [  14% ] 10/50 VUs  0m38.7s/4m30.0s

running (0m39.7s), 10/50 VUs, 512 complete and 0 interrupted iterations
default   [  15% ] 10/50 VUs  0m39.7s/4m30.0s
2025-09-23 20:21:36,941 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:21:36,942 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:21:36,942 INFO sqlalchemy.engine.Engine [cached since 32.4s ago] ('2025-09-23 20:21:36.940924', 5, 10, 0)
2025-09-23 20:21:36,968 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m40.7s), 10/50 VUs, 512 complete and 0 interrupted iterations
default   [  15% ] 10/50 VUs  0m40.7s/4m30.0s

running (0m41.7s), 10/50 VUs, 512 complete and 0 interrupted iterations
default   [  15% ] 10/50 VUs  0m41.7s/4m30.0s
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK

running (0m42.8s), 10/50 VUs, 512 complete and 0 interrupted iterations
default   [  16% ] 10/50 VUs  0m42.8s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m43.7s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  16% ] 10/50 VUs  0m43.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK

running (0m44.8s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  17% ] 10/50 VUs  0m44.8s/4m30.0s

running (0m45.7s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  17% ] 10/50 VUs  0m45.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m47.0s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  17% ] 10/50 VUs  0m47.0s/4m30.0s

running (0m47.8s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  18% ] 10/50 VUs  0m47.8s/4m30.0s
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (0m48.7s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  18% ] 10/50 VUs  0m48.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK

running (0m49.7s), 10/50 VUs, 522 complete and 0 interrupted iterations
default   [  18% ] 10/50 VUs  0m49.7s/4m30.0s
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK

running (0m50.9s), 10/50 VUs, 528 complete and 0 interrupted iterations
default   [  19% ] 10/50 VUs  0m50.9s/4m30.0s
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m51.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  19% ] 10/50 VUs  0m51.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK

running (0m52.8s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  20% ] 10/50 VUs  0m52.8s/4m30.0s

running (0m53.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  20% ] 10/50 VUs  0m53.7s/4m30.0s

running (0m54.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  20% ] 10/50 VUs  0m54.7s/4m30.0s

running (0m55.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  21% ] 10/50 VUs  0m55.7s/4m30.0s

running (0m56.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  21% ] 10/50 VUs  0m56.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m57.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  21% ] 10/50 VUs  0m57.7s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK

running (0m58.7s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  22% ] 10/50 VUs  0m58.7s/4m30.0s
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (0m59.8s), 10/50 VUs, 532 complete and 0 interrupted iterations
default   [  22% ] 10/50 VUs  0m59.8s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m00.8s), 10/50 VUs, 542 complete and 0 interrupted iterations
default   [  23% ] 10/50 VUs  1m00.8s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m01.9s), 10/50 VUs, 542 complete and 0 interrupted iterations
default   [  23% ] 10/50 VUs  1m01.9s/4m30.0s

running (1m02.7s), 10/50 VUs, 542 complete and 0 interrupted iterations
default   [  23% ] 10/50 VUs  1m02.7s/4m30.0s
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (1m03.8s), 10/50 VUs, 542 complete and 0 interrupted iterations
default   [  24% ] 10/50 VUs  1m03.8s/4m30.0s
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK

running (1m04.7s), 10/50 VUs, 542 complete and 0 interrupted iterations
default   [  24% ] 10/50 VUs  1m04.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m05.7s), 10/50 VUs, 542 complete and 0 interrupted iterations
default   [  24% ] 10/50 VUs  1m05.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m06.7s), 10/50 VUs, 550 complete and 0 interrupted iterations
default   [  25% ] 10/50 VUs  1m06.7s/4m30.0s
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK

running (1m07.7s), 10/50 VUs, 552 complete and 0 interrupted iterations
default   [  25% ] 10/50 VUs  1m07.7s/4m30.0s

running (1m08.9s), 10/50 VUs, 552 complete and 0 interrupted iterations
default   [  26% ] 10/50 VUs  1m08.9s/4m30.0s

running (1m09.8s), 10/50 VUs, 552 complete and 0 interrupted iterations
default   [  26% ] 10/50 VUs  1m09.8s/4m30.0s

running (1m10.7s), 10/50 VUs, 552 complete and 0 interrupted iterations
default   [  26% ] 10/50 VUs  1m10.7s/4m30.0s
2025-09-23 20:22:08,319 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:22:08,320 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:22:08,320 INFO sqlalchemy.engine.Engine [cached since 63.78s ago] ('2025-09-23 20:22:08.318927', 5, 10, 0)
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
2025-09-23 20:22:08,323 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK

running (1m11.7s), 10/50 VUs, 552 complete and 0 interrupted iterations
default   [  27% ] 10/50 VUs  1m11.7s/4m30.0s
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (1m12.7s), 10/50 VUs, 552 complete and 0 interrupted iterations
default   [  27% ] 10/50 VUs  1m12.7s/4m30.0s
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m14.1s), 10/50 VUs, 553 complete and 0 interrupted iterations
default   [  27% ] 10/50 VUs  1m14.1s/4m30.0s
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK

running (1m14.7s), 10/50 VUs, 553 complete and 0 interrupted iterations
default   [  28% ] 10/50 VUs  1m14.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK

running (1m15.7s), 10/50 VUs, 560 complete and 0 interrupted iterations
default   [  28% ] 10/50 VUs  1m15.7s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m16.8s), 10/50 VUs, 560 complete and 0 interrupted iterations
default   [  28% ] 10/50 VUs  1m16.8s/4m30.0s
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (1m17.7s), 10/50 VUs, 562 complete and 0 interrupted iterations
default   [  29% ] 10/50 VUs  1m17.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK

running (1m18.9s), 10/50 VUs, 562 complete and 0 interrupted iterations
default   [  29% ] 10/50 VUs  1m18.9s/4m30.0s

running (1m19.7s), 10/50 VUs, 562 complete and 0 interrupted iterations
default   [  30% ] 10/50 VUs  1m19.7s/4m30.0s
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK

running (1m20.7s), 10/50 VUs, 562 complete and 0 interrupted iterations
default   [  30% ] 10/50 VUs  1m20.7s/4m30.0s
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK

running (1m21.8s), 10/50 VUs, 563 complete and 0 interrupted iterations
default   [  30% ] 10/50 VUs  1m21.8s/4m30.0s

running (1m22.7s), 10/50 VUs, 563 complete and 0 interrupted iterations
default   [  31% ] 10/50 VUs  1m22.7s/4m30.0s

running (1m23.7s), 10/50 VUs, 563 complete and 0 interrupted iterations
default   [  31% ] 10/50 VUs  1m23.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK

running (1m24.8s), 10/50 VUs, 563 complete and 0 interrupted iterations
default   [  31% ] 10/50 VUs  1m24.8s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK

running (1m25.7s), 10/50 VUs, 563 complete and 0 interrupted iterations
default   [  32% ] 10/50 VUs  1m25.7s/4m30.0s
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m26.8s), 10/50 VUs, 571 complete and 0 interrupted iterations
default   [  32% ] 10/50 VUs  1m26.8s/4m30.0s
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK

running (1m27.8s), 10/50 VUs, 572 complete and 0 interrupted iterations
default   [  33% ] 10/50 VUs  1m27.8s/4m30.0s

running (1m28.9s), 10/50 VUs, 572 complete and 0 interrupted iterations
default   [  33% ] 10/50 VUs  1m28.9s/4m30.0s

running (1m29.7s), 10/50 VUs, 572 complete and 0 interrupted iterations
default   [  33% ] 10/50 VUs  1m29.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m30.7s), 10/50 VUs, 572 complete and 0 interrupted iterations
default   [  34% ] 10/50 VUs  1m30.7s/4m30.0s
INFO:     127.0.0.1:33400 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK

running (1m31.7s), 12/50 VUs, 573 complete and 0 interrupted iterations
default   [  34% ] 12/50 VUs  1m31.7s/4m30.0s
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (1m32.9s), 13/50 VUs, 573 complete and 0 interrupted iterations
default   [  34% ] 13/50 VUs  1m32.9s/4m30.0s

running (1m33.8s), 15/50 VUs, 573 complete and 0 interrupted iterations
default   [  35% ] 15/50 VUs  1m33.8s/4m30.0s
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /health HTTP/1.1" 200 OK

running (1m34.8s), 16/50 VUs, 573 complete and 0 interrupted iterations
default   [  35% ] 16/50 VUs  1m34.8s/4m30.0s

running (1m35.7s), 17/50 VUs, 573 complete and 0 interrupted iterations
default   [  35% ] 17/50 VUs  1m35.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m36.7s), 18/50 VUs, 573 complete and 0 interrupted iterations
default   [  36% ] 18/50 VUs  1m36.7s/4m30.0s
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (1m38.1s), 20/50 VUs, 580 complete and 0 interrupted iterations
default   [  36% ] 20/50 VUs  1m38.1s/4m30.0s

running (1m38.7s), 21/50 VUs, 580 complete and 0 interrupted iterations
default   [  37% ] 21/50 VUs  1m38.7s/4m30.0s
INFO:     127.0.0.1:33494 - "GET /health HTTP/1.1" 200 OK

running (1m39.7s), 22/50 VUs, 580 complete and 0 interrupted iterations
default   [  37% ] 22/50 VUs  1m39.7s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /health HTTP/1.1" 200 OK

running (1m40.8s), 24/50 VUs, 581 complete and 0 interrupted iterations
default   [  37% ] 24/50 VUs  1m40.8s/4m30.0s
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /health HTTP/1.1" 200 OK
2025-09-23 20:22:38,400 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:22:38,538 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:22:38,539 INFO sqlalchemy.engine.Engine [cached since 93.99s ago] ('2025-09-23 20:22:38.400366', 5, 10, 0)

running (1m41.8s), 25/50 VUs, 582 complete and 0 interrupted iterations
default   [  38% ] 25/50 VUs  1m41.8s/4m30.0s

running (1m42.9s), 27/50 VUs, 582 complete and 0 interrupted iterations
default   [  38% ] 27/50 VUs  1m42.9s/4m30.0s
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (1m43.7s), 27/50 VUs, 582 complete and 0 interrupted iterations
default   [  38% ] 27/50 VUs  1m43.7s/4m30.0s
INFO:     127.0.0.1:39032 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "GET /health HTTP/1.1" 200 OK
2025-09-23 20:22:40,796 INFO sqlalchemy.engine.Engine ROLLBACK

running (1m44.8s), 29/50 VUs, 583 complete and 0 interrupted iterations
default   [  39% ] 29/50 VUs  1m44.8s/4m30.0s

running (1m45.7s), 30/50 VUs, 583 complete and 0 interrupted iterations
default   [  39% ] 30/50 VUs  1m45.7s/4m30.0s

running (1m47.1s), 32/50 VUs, 583 complete and 0 interrupted iterations
default   [  40% ] 32/50 VUs  1m47.1s/4m30.0s

running (1m47.8s), 33/50 VUs, 583 complete and 0 interrupted iterations
default   [  40% ] 33/50 VUs  1m47.8s/4m30.0s

running (1m48.7s), 34/50 VUs, 583 complete and 0 interrupted iterations
default   [  40% ] 34/50 VUs  1m48.7s/4m30.0s
INFO:     127.0.0.1:39072 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /health HTTP/1.1" 200 OK

running (1m49.8s), 36/50 VUs, 584 complete and 0 interrupted iterations
default   [  41% ] 36/50 VUs  1m49.8s/4m30.0s

running (1m50.8s), 37/50 VUs, 584 complete and 0 interrupted iterations
default   [  41% ] 37/50 VUs  1m50.8s/4m30.0s
INFO:     127.0.0.1:39114 - "GET /health HTTP/1.1" 200 OK

running (1m51.7s), 38/50 VUs, 584 complete and 0 interrupted iterations
default   [  41% ] 38/50 VUs  1m51.7s/4m30.0s
INFO:     127.0.0.1:36274 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK

running (1m52.8s), 40/50 VUs, 584 complete and 0 interrupted iterations
default   [  42% ] 40/50 VUs  1m52.8s/4m30.0s
INFO:     127.0.0.1:36302 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /health HTTP/1.1" 200 OK

running (1m53.7s), 41/50 VUs, 586 complete and 0 interrupted iterations
default   [  42% ] 41/50 VUs  1m53.7s/4m30.0s

running (1m54.7s), 42/50 VUs, 586 complete and 0 interrupted iterations
default   [  42% ] 42/50 VUs  1m54.7s/4m30.0s
INFO:     127.0.0.1:36328 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "GET /health HTTP/1.1" 200 OK

running (1m55.7s), 44/50 VUs, 586 complete and 0 interrupted iterations
default   [  43% ] 44/50 VUs  1m55.7s/4m30.0s

running (1m56.7s), 45/50 VUs, 586 complete and 0 interrupted iterations
default   [  43% ] 45/50 VUs  1m56.7s/4m30.0s
INFO:     127.0.0.1:36338 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "GET /health HTTP/1.1" 200 OK

running (1m57.7s), 46/50 VUs, 586 complete and 0 interrupted iterations
default   [  44% ] 46/50 VUs  1m57.7s/4m30.0s

running (1m58.8s), 48/50 VUs, 586 complete and 0 interrupted iterations
default   [  44% ] 48/50 VUs  1m58.8s/4m30.0s
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36376 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "GET /health HTTP/1.1" 200 OK

running (1m59.8s), 49/50 VUs, 589 complete and 0 interrupted iterations
default   [  44% ] 49/50 VUs  1m59.8s/4m30.0s

running (2m00.7s), 50/50 VUs, 589 complete and 0 interrupted iterations
default   [  45% ] 50/50 VUs  2m00.7s/4m30.0s

running (2m02.0s), 50/50 VUs, 589 complete and 0 interrupted iterations
default   [  45% ] 50/50 VUs  2m02.0s/4m30.0s

running (2m02.8s), 50/50 VUs, 589 complete and 0 interrupted iterations
default   [  45% ] 50/50 VUs  2m02.8s/4m30.0s

running (2m03.9s), 50/50 VUs, 589 complete and 0 interrupted iterations
default   [  46% ] 50/50 VUs  2m03.9s/4m30.0s

running (2m04.8s), 50/50 VUs, 589 complete and 0 interrupted iterations
default   [  46% ] 50/50 VUs  2m04.8s/4m30.0s
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m05.8s), 50/50 VUs, 589 complete and 0 interrupted iterations
default   [  47% ] 50/50 VUs  2m05.8s/4m30.0s
INFO:     127.0.0.1:39004 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m06.8s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  47% ] 50/50 VUs  2m06.8s/4m30.0s

running (2m07.7s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  47% ] 50/50 VUs  2m07.7s/4m30.0s

running (2m08.7s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  48% ] 50/50 VUs  2m08.7s/4m30.0s

running (2m09.8s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  48% ] 50/50 VUs  2m09.8s/4m30.0s
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36376 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /health HTTP/1.1" 200 OK

running (2m10.8s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  48% ] 50/50 VUs  2m10.8s/4m30.0s

running (2m11.7s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  49% ] 50/50 VUs  2m11.7s/4m30.0s

running (2m12.9s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  49% ] 50/50 VUs  2m12.9s/4m30.0s

running (2m13.8s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  50% ] 50/50 VUs  2m13.8s/4m30.0s
INFO:     127.0.0.1:39058 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK

running (2m14.7s), 50/50 VUs, 591 complete and 0 interrupted iterations
default   [  50% ] 50/50 VUs  2m14.7s/4m30.0s
INFO:     127.0.0.1:39100 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (2m15.9s), 50/50 VUs, 598 complete and 0 interrupted iterations
default   [  50% ] 50/50 VUs  2m15.9s/4m30.0s

running (2m16.7s), 50/50 VUs, 598 complete and 0 interrupted iterations
default   [  51% ] 50/50 VUs  2m16.7s/4m30.0s

running (2m17.8s), 50/50 VUs, 598 complete and 0 interrupted iterations
default   [  51% ] 50/50 VUs  2m17.8s/4m30.0s
INFO:     127.0.0.1:36274 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /metrics HTTP/1.1" 200 OK

running (2m18.7s), 50/50 VUs, 598 complete and 0 interrupted iterations
default   [  51% ] 50/50 VUs  2m18.7s/4m30.0s
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /metrics HTTP/1.1" 200 OK

running (2m19.8s), 50/50 VUs, 603 complete and 0 interrupted iterations
default   [  52% ] 50/50 VUs  2m19.8s/4m30.0s

running (2m20.7s), 50/50 VUs, 603 complete and 0 interrupted iterations
default   [  52% ] 50/50 VUs  2m20.7s/4m30.0s

running (2m21.7s), 50/50 VUs, 603 complete and 0 interrupted iterations
default   [  52% ] 50/50 VUs  2m21.7s/4m30.0s
2025-09-23 20:23:18,788 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:23:18,789 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:23:18,789 INFO sqlalchemy.engine.Engine [cached since 134.2s ago] ('2025-09-23 20:23:18.787970', 5, 10, 0)
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m22.8s), 50/50 VUs, 603 complete and 0 interrupted iterations
default   [  53% ] 50/50 VUs  2m22.8s/4m30.0s
INFO:     127.0.0.1:36290 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (2m23.7s), 50/50 VUs, 605 complete and 0 interrupted iterations
default   [  53% ] 50/50 VUs  2m23.7s/4m30.0s
2025-09-23 20:23:21,282 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36376 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m24.9s), 50/50 VUs, 605 complete and 0 interrupted iterations
default   [  54% ] 50/50 VUs  2m24.9s/4m30.0s
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m25.8s), 50/50 VUs, 608 complete and 0 interrupted iterations
default   [  54% ] 50/50 VUs  2m25.8s/4m30.0s

running (2m26.7s), 50/50 VUs, 608 complete and 0 interrupted iterations
default   [  54% ] 50/50 VUs  2m26.7s/4m30.0s

running (2m27.7s), 50/50 VUs, 614 complete and 0 interrupted iterations
default   [  55% ] 50/50 VUs  2m27.7s/4m30.0s
INFO:     127.0.0.1:33448 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m28.7s), 50/50 VUs, 614 complete and 0 interrupted iterations
default   [  55% ] 50/50 VUs  2m28.7s/4m30.0s

running (2m29.7s), 50/50 VUs, 614 complete and 0 interrupted iterations
default   [  55% ] 50/50 VUs  2m29.7s/4m30.0s

running (2m30.8s), 50/50 VUs, 614 complete and 0 interrupted iterations
default   [  56% ] 50/50 VUs  2m30.8s/4m30.0s

running (2m31.7s), 50/50 VUs, 614 complete and 0 interrupted iterations
default   [  56% ] 50/50 VUs  2m31.7s/4m30.0s

running (2m32.7s), 50/50 VUs, 614 complete and 0 interrupted iterations
default   [  57% ] 50/50 VUs  2m32.7s/4m30.0s
INFO:     127.0.0.1:33470 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m33.9s), 50/50 VUs, 616 complete and 0 interrupted iterations
default   [  57% ] 50/50 VUs  2m33.9s/4m30.0s
INFO:     127.0.0.1:53392 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /docs HTTP/1.1" 200 OK

running (2m34.8s), 50/50 VUs, 616 complete and 0 interrupted iterations
default   [  57% ] 50/50 VUs  2m34.8s/4m30.0s
INFO:     127.0.0.1:33460 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /health HTTP/1.1" 200 OK

running (2m35.7s), 50/50 VUs, 623 complete and 0 interrupted iterations
default   [  58% ] 50/50 VUs  2m35.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m36.8s), 50/50 VUs, 623 complete and 0 interrupted iterations
default   [  58% ] 50/50 VUs  2m36.8s/4m30.0s

running (2m37.7s), 50/50 VUs, 623 complete and 0 interrupted iterations
default   [  58% ] 50/50 VUs  2m37.7s/4m30.0s
INFO:     127.0.0.1:33460 - "GET /metrics HTTP/1.1" 200 OK

running (2m38.9s), 50/50 VUs, 626 complete and 0 interrupted iterations
default   [  59% ] 50/50 VUs  2m38.9s/4m30.0s

running (2m39.7s), 50/50 VUs, 629 complete and 0 interrupted iterations
default   [  59% ] 50/50 VUs  2m39.7s/4m30.0s
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m40.7s), 50/50 VUs, 629 complete and 0 interrupted iterations
default   [  60% ] 50/50 VUs  2m40.7s/4m30.0s
INFO:     127.0.0.1:36376 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "GET /docs HTTP/1.1" 200 OK

running (2m41.9s), 50/50 VUs, 634 complete and 0 interrupted iterations
default   [  60% ] 50/50 VUs  2m41.9s/4m30.0s

running (2m42.7s), 50/50 VUs, 634 complete and 0 interrupted iterations
default   [  60% ] 50/50 VUs  2m42.7s/4m30.0s
INFO:     127.0.0.1:33478 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m43.9s), 50/50 VUs, 635 complete and 0 interrupted iterations
default   [  61% ] 50/50 VUs  2m43.9s/4m30.0s

running (2m44.7s), 50/50 VUs, 635 complete and 0 interrupted iterations
default   [  61% ] 50/50 VUs  2m44.7s/4m30.0s

running (2m45.7s), 50/50 VUs, 635 complete and 0 interrupted iterations
default   [  61% ] 50/50 VUs  2m45.7s/4m30.0s
INFO:     127.0.0.1:33494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK

running (2m46.7s), 50/50 VUs, 635 complete and 0 interrupted iterations
default   [  62% ] 50/50 VUs  2m46.7s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (2m47.7s), 50/50 VUs, 640 complete and 0 interrupted iterations
default   [  62% ] 50/50 VUs  2m47.7s/4m30.0s
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m48.7s), 50/50 VUs, 640 complete and 0 interrupted iterations
default   [  62% ] 50/50 VUs  2m48.7s/4m30.0s

running (2m49.8s), 50/50 VUs, 640 complete and 0 interrupted iterations
default   [  63% ] 50/50 VUs  2m49.8s/4m30.0s

running (2m50.8s), 50/50 VUs, 640 complete and 0 interrupted iterations
default   [  63% ] 50/50 VUs  2m50.8s/4m30.0s

running (2m51.7s), 50/50 VUs, 640 complete and 0 interrupted iterations
default   [  64% ] 50/50 VUs  2m51.7s/4m30.0s
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m52.8s), 50/50 VUs, 640 complete and 0 interrupted iterations
default   [  64% ] 50/50 VUs  2m52.8s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m53.8s), 50/50 VUs, 641 complete and 0 interrupted iterations
default   [  64% ] 50/50 VUs  2m53.8s/4m30.0s

running (2m54.7s), 50/50 VUs, 646 complete and 0 interrupted iterations
default   [  65% ] 50/50 VUs  2m54.7s/4m30.0s

running (2m55.7s), 50/50 VUs, 646 complete and 0 interrupted iterations
default   [  65% ] 50/50 VUs  2m55.7s/4m30.0s

running (2m56.7s), 50/50 VUs, 646 complete and 0 interrupted iterations
default   [  65% ] 50/50 VUs  2m56.7s/4m30.0s
2025-09-23 20:23:53,752 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:23:53,753 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:23:53,753 INFO sqlalchemy.engine.Engine [cached since 169.2s ago] ('2025-09-23 20:23:53.752294', 5, 10, 0)
INFO:     127.0.0.1:39100 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (2m57.7s), 50/50 VUs, 649 complete and 0 interrupted iterations
default   [  66% ] 50/50 VUs  2m57.7s/4m30.0s
2025-09-23 20:23:54,799 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:36306 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /docs HTTP/1.1" 200 OK

running (2m58.7s), 50/50 VUs, 651 complete and 0 interrupted iterations
default   [  66% ] 50/50 VUs  2m58.7s/4m30.0s

running (2m59.7s), 50/50 VUs, 651 complete and 0 interrupted iterations
default   [  67% ] 50/50 VUs  2m59.7s/4m30.0s
INFO:     127.0.0.1:39004 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /health HTTP/1.1" 200 OK

running (3m00.9s), 50/50 VUs, 651 complete and 0 interrupted iterations
default   [  67% ] 50/50 VUs  3m00.9s/4m30.0s

running (3m01.7s), 50/50 VUs, 651 complete and 0 interrupted iterations
default   [  67% ] 50/50 VUs  3m01.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m03.0s), 50/50 VUs, 651 complete and 0 interrupted iterations
default   [  68% ] 50/50 VUs  3m03.0s/4m30.0s
INFO:     127.0.0.1:33404 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (3m03.9s), 50/50 VUs, 654 complete and 0 interrupted iterations
default   [  68% ] 50/50 VUs  3m03.9s/4m30.0s
INFO:     127.0.0.1:36274 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m04.9s), 50/50 VUs, 655 complete and 0 interrupted iterations
default   [  68% ] 50/50 VUs  3m04.9s/4m30.0s

running (3m05.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  69% ] 50/50 VUs  3m05.7s/4m30.0s

running (3m06.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  69% ] 50/50 VUs  3m06.7s/4m30.0s

running (3m07.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  70% ] 50/50 VUs  3m07.7s/4m30.0s
INFO:     127.0.0.1:36376 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (3m08.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  70% ] 50/50 VUs  3m08.7s/4m30.0s
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m09.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  70% ] 50/50 VUs  3m09.7s/4m30.0s

running (3m10.9s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  71% ] 50/50 VUs  3m10.9s/4m30.0s
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /docs HTTP/1.1" 200 OK

running (3m11.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  71% ] 50/50 VUs  3m11.7s/4m30.0s
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m12.8s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  71% ] 50/50 VUs  3m12.8s/4m30.0s
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (3m13.7s), 50/50 VUs, 664 complete and 0 interrupted iterations
default   [  72% ] 50/50 VUs  3m13.7s/4m30.0s

running (3m14.7s), 50/50 VUs, 669 complete and 0 interrupted iterations
default   [  72% ] 50/50 VUs  3m14.7s/4m30.0s

running (3m15.7s), 50/50 VUs, 669 complete and 0 interrupted iterations
default   [  72% ] 50/50 VUs  3m15.7s/4m30.0s
INFO:     127.0.0.1:33470 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /health HTTP/1.1" 200 OK

running (3m16.7s), 50/50 VUs, 673 complete and 0 interrupted iterations
default   [  73% ] 50/50 VUs  3m16.7s/4m30.0s
INFO:     127.0.0.1:33478 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK

running (3m17.7s), 50/50 VUs, 673 complete and 0 interrupted iterations
default   [  73% ] 50/50 VUs  3m17.7s/4m30.0s

running (3m18.9s), 50/50 VUs, 680 complete and 0 interrupted iterations
default   [  74% ] 50/50 VUs  3m18.9s/4m30.0s

running (3m19.7s), 50/50 VUs, 680 complete and 0 interrupted iterations
default   [  74% ] 50/50 VUs  3m19.7s/4m30.0s

running (3m20.7s), 50/50 VUs, 680 complete and 0 interrupted iterations
default   [  74% ] 50/50 VUs  3m20.7s/4m30.0s
INFO:     127.0.0.1:33460 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36376 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK

running (3m21.7s), 50/50 VUs, 690 complete and 0 interrupted iterations
default   [  75% ] 50/50 VUs  3m21.7s/4m30.0s

running (3m22.7s), 50/50 VUs, 690 complete and 0 interrupted iterations
default   [  75% ] 50/50 VUs  3m22.7s/4m30.0s
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /health HTTP/1.1" 200 OK

running (3m23.7s), 50/50 VUs, 690 complete and 0 interrupted iterations
default   [  75% ] 50/50 VUs  3m23.7s/4m30.0s
INFO:     127.0.0.1:33494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK

running (3m24.8s), 50/50 VUs, 690 complete and 0 interrupted iterations
default   [  76% ] 50/50 VUs  3m24.8s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m25.7s), 50/50 VUs, 692 complete and 0 interrupted iterations
default   [  76% ] 50/50 VUs  3m25.7s/4m30.0s

running (3m26.8s), 50/50 VUs, 692 complete and 0 interrupted iterations
default   [  77% ] 50/50 VUs  3m26.8s/4m30.0s

running (3m27.7s), 50/50 VUs, 692 complete and 0 interrupted iterations
default   [  77% ] 50/50 VUs  3m27.7s/4m30.0s

running (3m28.8s), 50/50 VUs, 692 complete and 0 interrupted iterations
default   [  77% ] 50/50 VUs  3m28.8s/4m30.0s

running (3m29.8s), 50/50 VUs, 692 complete and 0 interrupted iterations
default   [  78% ] 50/50 VUs  3m29.8s/4m30.0s
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /docs HTTP/1.1" 200 OK
2025-09-23 20:24:27,667 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:24:27,667 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:24:27,668 INFO sqlalchemy.engine.Engine [cached since 203.1s ago] ('2025-09-23 20:24:27.667295', 5, 10, 0)

running (3m30.7s), 50/50 VUs, 692 complete and 0 interrupted iterations
default   [  78% ] 50/50 VUs  3m30.7s/4m30.0s
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36376 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /metrics HTTP/1.1" 200 OK
2025-09-23 20:24:28,154 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /health HTTP/1.1" 200 OK

running (3m31.8s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  78% ] 50/50 VUs  3m31.8s/4m30.0s

running (3m32.7s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  79% ] 50/50 VUs  3m32.7s/4m30.0s

running (3m33.7s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  79% ] 50/50 VUs  3m33.7s/4m30.0s

running (3m34.8s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  80% ] 50/50 VUs  3m34.8s/4m30.0s
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /docs HTTP/1.1" 200 OK

running (3m35.7s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  80% ] 50/50 VUs  3m35.7s/4m30.0s
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m36.8s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  80% ] 50/50 VUs  3m36.8s/4m30.0s

running (3m37.9s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  81% ] 50/50 VUs  3m37.9s/4m30.0s

running (3m38.7s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  81% ] 50/50 VUs  3m38.7s/4m30.0s

running (3m39.8s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  81% ] 50/50 VUs  3m39.8s/4m30.0s

running (3m40.9s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  82% ] 50/50 VUs  3m40.9s/4m30.0s

running (3m41.7s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  82% ] 50/50 VUs  3m41.7s/4m30.0s

running (3m42.8s), 50/50 VUs, 701 complete and 0 interrupted iterations
default   [  83% ] 50/50 VUs  3m42.8s/4m30.0s
INFO:     127.0.0.1:39076 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (3m43.7s), 50/50 VUs, 702 complete and 0 interrupted iterations
default   [  83% ] 50/50 VUs  3m43.7s/4m30.0s
INFO:     127.0.0.1:39096 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /metrics HTTP/1.1" 200 OK

running (3m44.7s), 50/50 VUs, 705 complete and 0 interrupted iterations
default   [  83% ] 50/50 VUs  3m44.7s/4m30.0s
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m45.7s), 50/50 VUs, 705 complete and 0 interrupted iterations
default   [  84% ] 50/50 VUs  3m45.7s/4m30.0s
INFO:     127.0.0.1:39026 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /metrics HTTP/1.1" 200 OK

running (3m46.7s), 50/50 VUs, 708 complete and 0 interrupted iterations
default   [  84% ] 50/50 VUs  3m46.7s/4m30.0s

running (3m47.7s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  84% ] 50/50 VUs  3m47.7s/4m30.0s

running (3m48.7s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  85% ] 50/50 VUs  3m48.7s/4m30.0s
INFO:     127.0.0.1:36274 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m49.7s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  85% ] 50/50 VUs  3m49.7s/4m30.0s

running (3m50.7s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  85% ] 50/50 VUs  3m50.7s/4m30.0s
INFO:     127.0.0.1:33420 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /docs HTTP/1.1" 200 OK

running (3m51.8s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  86% ] 50/50 VUs  3m51.8s/4m30.0s
INFO:     127.0.0.1:36330 - "GET /docs HTTP/1.1" 200 OK

running (3m52.8s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  86% ] 50/50 VUs  3m52.8s/4m30.0s
INFO:     127.0.0.1:36358 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m53.8s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  87% ] 50/50 VUs  3m53.8s/4m30.0s

running (3m54.8s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  87% ] 50/50 VUs  3m54.8s/4m30.0s
INFO:     127.0.0.1:33460 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (3m55.8s), 50/50 VUs, 714 complete and 0 interrupted iterations
default   [  87% ] 50/50 VUs  3m55.8s/4m30.0s
INFO:     127.0.0.1:33428 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36374 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36376 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53382 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53392 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:53402 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /metrics HTTP/1.1" 200 OK

running (3m56.7s), 50/50 VUs, 721 complete and 0 interrupted iterations
default   [  88% ] 50/50 VUs  3m56.7s/4m30.0s

running (3m57.7s), 50/50 VUs, 730 complete and 0 interrupted iterations
default   [  88% ] 50/50 VUs  3m57.7s/4m30.0s

running (3m58.7s), 50/50 VUs, 730 complete and 0 interrupted iterations
default   [  88% ] 50/50 VUs  3m58.7s/4m30.0s

running (3m59.7s), 50/50 VUs, 730 complete and 0 interrupted iterations
default   [  89% ] 50/50 VUs  3m59.7s/4m30.0s

running (4m00.7s), 50/50 VUs, 730 complete and 0 interrupted iterations
default   [  89% ] 50/50 VUs  4m00.7s/4m30.0s
INFO:     127.0.0.1:36274 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /health HTTP/1.1" 200 OK

running (4m01.8s), 50/50 VUs, 730 complete and 0 interrupted iterations
default   [  90% ] 50/50 VUs  4m01.8s/4m30.0s
INFO:     127.0.0.1:39004 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /docs HTTP/1.1" 200 OK

running (4m02.7s), 50/50 VUs, 730 complete and 0 interrupted iterations
default   [  90% ] 50/50 VUs  4m02.7s/4m30.0s
INFO:     127.0.0.1:39026 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36374 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53402 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53392 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36376 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:53382 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39018 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38998 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39004 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39058 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (4m03.9s), 47/50 VUs, 737 complete and 0 interrupted iterations
default   [  90% ] 47/50 VUs  4m03.9s/4m30.0s

running (4m04.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  91% ] 45/50 VUs  4m04.7s/4m30.0s
INFO:     127.0.0.1:39032 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /health HTTP/1.1" 200 OK
2025-09-23 20:25:02,166 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:25:02,241 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:25:02,241 INFO sqlalchemy.engine.Engine [cached since 237.7s ago] ('2025-09-23 20:25:02.166172', 5, 10, 0)
INFO:     127.0.0.1:39100 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /metrics HTTP/1.1" 200 OK

running (4m05.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  91% ] 45/50 VUs  4m05.7s/4m30.0s

running (4m06.9s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  91% ] 45/50 VUs  4m06.9s/4m30.0s

running (4m07.8s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  92% ] 45/50 VUs  4m07.8s/4m30.0s

running (4m08.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  92% ] 45/50 VUs  4m08.7s/4m30.0s

running (4m09.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  92% ] 45/50 VUs  4m09.7s/4m30.0s

running (4m11.4s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  93% ] 45/50 VUs  4m11.4s/4m30.0s

running (4m11.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  93% ] 45/50 VUs  4m11.7s/4m30.0s

running (4m12.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  94% ] 45/50 VUs  4m12.7s/4m30.0s

running (4m13.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  94% ] 45/50 VUs  4m13.7s/4m30.0s

running (4m14.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  94% ] 45/50 VUs  4m14.7s/4m30.0s

running (4m15.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  95% ] 45/50 VUs  4m15.7s/4m30.0s

running (4m16.7s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  95% ] 45/50 VUs  4m16.7s/4m30.0s
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39018 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39004 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:38998 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (4m17.8s), 45/50 VUs, 742 complete and 0 interrupted iterations
default   [  95% ] 45/50 VUs  4m17.8s/4m30.0s
2025-09-23 20:25:15,266 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     127.0.0.1:33400 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39048 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39086 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39114 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39072 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39026 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (4m18.9s), 42/50 VUs, 751 complete and 0 interrupted iterations
default   [  96% ] 42/50 VUs  4m18.9s/4m30.0s
INFO:     127.0.0.1:40488 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:33400 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39100 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39058 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39072 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39114 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39048 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39086 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /health HTTP/1.1" 200 OK

running (4m19.8s), 35/50 VUs, 761 complete and 0 interrupted iterations
default   [  96% ] 35/50 VUs  4m19.8s/4m30.0s

running (4m20.7s), 35/50 VUs, 761 complete and 0 interrupted iterations
default   [  97% ] 35/50 VUs  4m20.7s/4m30.0s

running (4m21.7s), 35/50 VUs, 761 complete and 0 interrupted iterations
default   [  97% ] 35/50 VUs  4m21.7s/4m30.0s

running (4m22.7s), 35/50 VUs, 761 complete and 0 interrupted iterations
default   [  97% ] 35/50 VUs  4m22.7s/4m30.0s

running (4m23.7s), 35/50 VUs, 761 complete and 0 interrupted iterations
default   [  98% ] 35/50 VUs  4m23.7s/4m30.0s
INFO:     127.0.0.1:39100 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33400 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36330 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:39032 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "GET /metrics HTTP/1.1" 200 OK

running (4m24.7s), 32/50 VUs, 764 complete and 0 interrupted iterations
default   [  98% ] 32/50 VUs  4m24.7s/4m30.0s
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33420 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36320 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36338 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36302 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36368 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33404 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36290 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36346 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:34810 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36310 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39076 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36306 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36274 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36328 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:39096 - "GET /docs HTTP/1.1" 200 OK

running (4m25.7s), 32/50 VUs, 764 complete and 0 interrupted iterations
default   [  98% ] 32/50 VUs  4m25.7s/4m30.0s

running (4m26.7s), 32/50 VUs, 764 complete and 0 interrupted iterations
default   [  99% ] 32/50 VUs  4m26.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36338 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:34810 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36310 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36290 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36274 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36306 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33420 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36368 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39096 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36320 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36328 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36346 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:39076 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36330 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33404 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36302 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /metrics HTTP/1.1" 200 OK

running (4m27.8s), 16/50 VUs, 780 complete and 0 interrupted iterations
default   [  99% ] 16/50 VUs  4m27.8s/4m30.0s
INFO:     127.0.0.1:36476 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36480 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33470 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36358 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33428 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33460 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33448 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36476 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36482 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40494 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40488 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33478 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:33470 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36358 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33428 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (4m28.7s), 16/50 VUs, 780 complete and 0 interrupted iterations
default   [ 100% ] 16/50 VUs  4m28.7s/4m30.0s
INFO:     127.0.0.1:36476 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36482 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33460 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33448 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36480 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36452 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36442 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:40474 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:33478 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40488 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:40494 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36442 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:36452 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (4m29.7s), 06/50 VUs, 791 complete and 0 interrupted iterations
default   [ 100% ] 06/50 VUs  4m29.7s/4m30.0s
INFO:     127.0.0.1:36468 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (4m30.7s), 01/50 VUs, 796 complete and 0 interrupted iterations
default ↓ [ 100% ] 01/50 VUs  4m30s
INFO:     127.0.0.1:36468 - "POST /webhooks/paypal HTTP/1.1" 400 Bad Request

running (4m31.7s), 01/50 VUs, 796 complete and 0 interrupted iterations
default ↓ [ 100% ] 01/50 VUs  4m30s
INFO:     127.0.0.1:36468 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:36468 - "POST /webhooks/stripe HTTP/1.1" 400 Bad Request

running (4m32.7s), 01/50 VUs, 796 complete and 0 interrupted iterations
default ↓ [ 100% ] 01/50 VUs  4m30s


  █ THRESHOLDS 

    errors
    ✗ 'rate<0.05' rate=100.00%

    http_req_duration
    ✗ 'p(95)<500' p(95)=14s

    http_req_failed
    ✗ 'rate<0.05' rate=60.07%


  █ TOTAL RESULTS 

    checks_total.......: 4130   15.13905/s
    checks_succeeded...: 38.37% 1585 out of 4130
    checks_failed......: 61.62% 2545 out of 4130

    ✗ health check status is 200
      ↳  39% — ✓ 317 / ✗ 480
    ✗ health response contains status
      ↳  39% — ✓ 317 / ✗ 480
    ✗ stripe webhook status is 200
      ↳  0% — ✓ 0 / ✗ 317
    ✗ stripe webhook processed
      ↳  0% — ✓ 0 / ✗ 317
    ✗ paypal webhook status is 200
      ↳  0% — ✓ 0 / ✗ 317
    ✗ paypal webhook processed
      ↳  0% — ✓ 0 / ✗ 317
    ✓ metrics endpoint accessible
    ✓ metrics contains prometheus format
    ✓ docs endpoint accessible
    ✗ duplicate webhook handled
      ↳  0% — ✓ 0 / ✗ 317

    CUSTOM
    errors.........................: 100.00% 951 out of 951

    HTTP
    http_req_duration..............: avg=3.5s   min=0s       med=1.59s  max=21.19s p(90)=9.91s  p(95)=14s   
      { expected_response:true }...: avg=2.32s  min=2.54ms   med=1.93s  max=12.72s p(90)=5.28s  p(95)=6.09s 
    http_req_failed................: 60.07%  1431 out of 2382
    http_reqs......................: 2382    8.73153/s

    EXECUTION
    iteration_duration.............: avg=11.07s min=101.97µs med=1.29ms max=48.81s p(90)=40.78s p(95)=43.42s
    iterations.....................: 797     2.921507/s
    vus............................: 1       min=1            max=50
    vus_max........................: 50      min=50           max=50

    NETWORK
    data_received..................: 5.5 MB  20 kB/s
    data_sent......................: 514 kB  1.9 kB/s




running (4m32.8s), 00/50 VUs, 797 complete and 0 interrupted iterations
default ✓ [ 100% ] 00/50 VUs  4m30s
2025-09-23 20:25:46,148 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:25:46,151 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:25:46,152 INFO sqlalchemy.engine.Engine [cached since 281.6s ago] ('2025-09-23 20:25:46.147972', 5, 10, 0)
2025-09-23 20:25:46,218 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:26:16,220 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:26:16,222 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:26:16,222 INFO sqlalchemy.engine.Engine [cached since 311.7s ago] ('2025-09-23 20:26:16.219729', 5, 10, 0)
2025-09-23 20:26:16,222 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:26:46,300 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:26:46,301 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:26:46,302 INFO sqlalchemy.engine.Engine [cached since 341.8s ago] ('2025-09-23 20:26:46.298729', 5, 10, 0)
2025-09-23 20:26:46,303 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:27:16,314 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:27:16,314 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:27:16,314 INFO sqlalchemy.engine.Engine [cached since 371.8s ago] ('2025-09-23 20:27:16.308289', 5, 10, 0)
2025-09-23 20:27:16,315 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:27:46,321 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:27:46,321 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:27:46,321 INFO sqlalchemy.engine.Engine [cached since 401.8s ago] ('2025-09-23 20:27:46.320955', 5, 10, 0)
2025-09-23 20:27:46,469 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:28:16,472 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:28:16,474 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:28:16,475 INFO sqlalchemy.engine.Engine [cached since 431.9s ago] ('2025-09-23 20:28:16.471822', 5, 10, 0)
2025-09-23 20:28:16,476 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:28:46,861 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:28:46,862 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:28:46,863 INFO sqlalchemy.engine.Engine [cached since 462.3s ago] ('2025-09-23 20:28:46.861022', 5, 10, 0)
2025-09-23 20:28:46,864 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:29:16,866 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:29:16,869 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:29:16,869 INFO sqlalchemy.engine.Engine [cached since 492.3s ago] ('2025-09-23 20:29:16.866433', 5, 10, 0)
2025-09-23 20:29:16,870 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:29:46,873 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:29:46,874 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:29:46,874 INFO sqlalchemy.engine.Engine [cached since 522.3s ago] ('2025-09-23 20:29:46.872424', 5, 10, 0)
2025-09-23 20:29:46,875 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:30:16,877 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:30:16,877 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:30:16,878 INFO sqlalchemy.engine.Engine [cached since 552.3s ago] ('2025-09-23 20:30:16.876868', 5, 10, 0)
2025-09-23 20:30:16,878 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:30:46,880 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:30:46,880 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:30:46,883 INFO sqlalchemy.engine.Engine [cached since 582.3s ago] ('2025-09-23 20:30:46.879609', 5, 10, 0)
2025-09-23 20:30:46,943 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:31:16,944 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:31:16,945 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:31:16,945 INFO sqlalchemy.engine.Engine [cached since 612.4s ago] ('2025-09-23 20:31:16.944358', 5, 10, 0)
2025-09-23 20:31:16,946 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:31:46,951 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:31:46,957 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:31:47,099 INFO sqlalchemy.engine.Engine [cached since 642.6s ago] ('2025-09-23 20:31:46.950957', 5, 10, 0)
2025-09-23 20:31:47,100 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:32:17,101 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:32:17,101 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:32:17,101 INFO sqlalchemy.engine.Engine [cached since 672.6s ago] ('2025-09-23 20:32:17.100483', 5, 10, 0)
2025-09-23 20:32:17,102 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:32:47,114 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:32:47,115 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:32:47,115 INFO sqlalchemy.engine.Engine [cached since 702.6s ago] ('2025-09-23 20:32:47.114510', 5, 10, 0)
2025-09-23 20:32:47,116 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:33:17,118 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:33:17,177 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:33:17,178 INFO sqlalchemy.engine.Engine [cached since 732.6s ago] ('2025-09-23 20:33:17.118010', 5, 10, 0)
2025-09-23 20:33:17,266 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:33:47,267 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:33:47,268 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:33:47,268 INFO sqlalchemy.engine.Engine [cached since 762.7s ago] ('2025-09-23 20:33:47.267254', 5, 10, 0)
2025-09-23 20:33:47,271 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:34:17,272 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:34:17,275 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:34:17,276 INFO sqlalchemy.engine.Engine [cached since 792.7s ago] ('2025-09-23 20:34:17.272222', 5, 10, 0)
2025-09-23 20:34:17,278 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:34:47,344 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:34:47,345 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:34:47,345 INFO sqlalchemy.engine.Engine [cached since 822.8s ago] ('2025-09-23 20:34:47.343736', 5, 10, 0)
2025-09-23 20:34:47,346 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:35:17,348 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:35:17,351 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:35:17,354 INFO sqlalchemy.engine.Engine [cached since 852.8s ago] ('2025-09-23 20:35:17.347959', 5, 10, 0)
2025-09-23 20:35:17,355 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:35:47,358 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:35:47,361 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:35:47,361 INFO sqlalchemy.engine.Engine [cached since 882.8s ago] ('2025-09-23 20:35:47.357963', 5, 10, 0)
2025-09-23 20:35:47,368 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:36:17,402 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:36:17,403 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:36:17,404 INFO sqlalchemy.engine.Engine [cached since 912.9s ago] ('2025-09-23 20:36:17.402176', 5, 10, 0)
2025-09-23 20:36:17,498 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:36:47,578 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:36:47,579 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:36:47,579 INFO sqlalchemy.engine.Engine [cached since 943s ago] ('2025-09-23 20:36:47.577880', 5, 10, 0)
2025-09-23 20:36:47,580 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:37:17,581 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:37:17,582 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:37:17,582 INFO sqlalchemy.engine.Engine [cached since 973s ago] ('2025-09-23 20:37:17.581200', 5, 10, 0)
2025-09-23 20:37:17,583 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:37:47,664 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:37:47,666 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:37:47,666 INFO sqlalchemy.engine.Engine [cached since 1003s ago] ('2025-09-23 20:37:47.663952', 5, 10, 0)
2025-09-23 20:37:47,667 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:38:17,668 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:38:17,669 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:38:17,669 INFO sqlalchemy.engine.Engine [cached since 1033s ago] ('2025-09-23 20:38:17.668532', 5, 10, 0)
2025-09-23 20:38:17,670 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:38:47,671 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:38:47,679 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:38:47,679 INFO sqlalchemy.engine.Engine [cached since 1063s ago] ('2025-09-23 20:38:47.671278', 5, 10, 0)
2025-09-23 20:38:47,680 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:39:17,739 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:39:17,740 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:39:17,740 INFO sqlalchemy.engine.Engine [cached since 1093s ago] ('2025-09-23 20:39:17.739115', 5, 10, 0)
2025-09-23 20:39:17,743 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:39:47,822 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:39:47,824 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:39:47,825 INFO sqlalchemy.engine.Engine [cached since 1123s ago] ('2025-09-23 20:39:47.822042', 5, 10, 0)
2025-09-23 20:39:47,825 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:40:17,978 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:40:17,978 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:40:17,978 INFO sqlalchemy.engine.Engine [cached since 1153s ago] ('2025-09-23 20:40:17.977757', 5, 10, 0)
2025-09-23 20:40:18,061 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:40:48,063 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:40:48,064 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:40:48,064 INFO sqlalchemy.engine.Engine [cached since 1184s ago] ('2025-09-23 20:40:48.062163', 5, 10, 0)
2025-09-23 20:40:48,067 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:41:18,069 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:41:18,071 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:41:18,072 INFO sqlalchemy.engine.Engine [cached since 1214s ago] ('2025-09-23 20:41:18.068982', 5, 10, 0)
2025-09-23 20:41:18,072 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:41:48,074 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:41:48,075 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:41:48,075 INFO sqlalchemy.engine.Engine [cached since 1244s ago] ('2025-09-23 20:41:48.073736', 5, 10, 0)
2025-09-23 20:41:48,076 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:42:18,078 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:42:18,080 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:42:18,080 INFO sqlalchemy.engine.Engine [cached since 1274s ago] ('2025-09-23 20:42:18.077940', 5, 10, 0)
2025-09-23 20:42:18,140 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:42:48,153 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:42:48,153 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:42:48,153 INFO sqlalchemy.engine.Engine [cached since 1304s ago] ('2025-09-23 20:42:48.147067', 5, 10, 0)
2025-09-23 20:42:48,156 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:43:18,220 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:43:18,222 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:43:18,222 INFO sqlalchemy.engine.Engine [cached since 1334s ago] ('2025-09-23 20:43:18.219974', 5, 10, 0)
2025-09-23 20:43:18,223 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:43:48,224 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:43:48,225 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:43:48,225 INFO sqlalchemy.engine.Engine [cached since 1364s ago] ('2025-09-23 20:43:48.224430', 5, 10, 0)
2025-09-23 20:43:48,225 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:44:18,227 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:44:18,229 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:44:18,230 INFO sqlalchemy.engine.Engine [cached since 1394s ago] ('2025-09-23 20:44:18.227161', 5, 10, 0)
2025-09-23 20:44:18,231 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:44:48,233 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:44:48,301 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:44:48,302 INFO sqlalchemy.engine.Engine [cached since 1424s ago] ('2025-09-23 20:44:48.233185', 5, 10, 0)
2025-09-23 20:44:48,303 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:45:18,324 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:45:18,382 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:45:18,382 INFO sqlalchemy.engine.Engine [cached since 1454s ago] ('2025-09-23 20:45:18.323612', 5, 10, 0)
2025-09-23 20:45:18,392 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:45:48,458 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:45:48,458 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:45:48,459 INFO sqlalchemy.engine.Engine [cached since 1484s ago] ('2025-09-23 20:45:48.457803', 5, 10, 0)
2025-09-23 20:45:48,461 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:46:18,590 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:46:18,591 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:46:18,591 INFO sqlalchemy.engine.Engine [cached since 1514s ago] ('2025-09-23 20:46:18.539470', 5, 10, 0)
2025-09-23 20:46:18,592 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:46:48,618 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:46:48,619 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:46:48,619 INFO sqlalchemy.engine.Engine [cached since 1544s ago] ('2025-09-23 20:46:48.617936', 5, 10, 0)
2025-09-23 20:46:48,620 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:47:18,622 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:47:18,622 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:47:18,623 INFO sqlalchemy.engine.Engine [cached since 1574s ago] ('2025-09-23 20:47:18.621967', 5, 10, 0)
2025-09-23 20:47:18,626 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:47:48,632 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:47:48,635 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:47:48,635 INFO sqlalchemy.engine.Engine [cached since 1604s ago] ('2025-09-23 20:47:48.631122', 5, 10, 0)
2025-09-23 20:47:48,638 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:48:18,700 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:48:18,700 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:48:18,701 INFO sqlalchemy.engine.Engine [cached since 1634s ago] ('2025-09-23 20:48:18.699873', 5, 10, 0)
2025-09-23 20:48:18,702 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:48:48,712 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:48:48,713 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:48:48,713 INFO sqlalchemy.engine.Engine [cached since 1664s ago] ('2025-09-23 20:48:48.712467', 5, 10, 0)
2025-09-23 20:48:48,716 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:49:18,719 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:49:18,721 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:49:18,721 INFO sqlalchemy.engine.Engine [cached since 1694s ago] ('2025-09-23 20:49:18.718984', 5, 10, 0)
2025-09-23 20:49:18,723 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:49:48,780 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:49:48,781 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:49:48,781 INFO sqlalchemy.engine.Engine [cached since 1724s ago] ('2025-09-23 20:49:48.778800', 5, 10, 0)
2025-09-23 20:49:48,785 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:50:18,787 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:50:18,790 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:50:18,793 INFO sqlalchemy.engine.Engine [cached since 1754s ago] ('2025-09-23 20:50:18.786981', 5, 10, 0)
2025-09-23 20:50:18,862 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:50:48,866 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:50:48,939 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:50:48,941 INFO sqlalchemy.engine.Engine [cached since 1784s ago] ('2025-09-23 20:50:48.865963', 5, 10, 0)
2025-09-23 20:50:48,942 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:51:18,942 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:51:18,943 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:51:18,943 INFO sqlalchemy.engine.Engine [cached since 1814s ago] ('2025-09-23 20:51:18.942136', 5, 10, 0)
2025-09-23 20:51:18,944 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:51:48,946 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:51:48,948 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:51:48,948 INFO sqlalchemy.engine.Engine [cached since 1844s ago] ('2025-09-23 20:51:48.945961', 5, 10, 0)
2025-09-23 20:51:48,949 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:52:18,950 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:52:18,951 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:52:18,951 INFO sqlalchemy.engine.Engine [cached since 1874s ago] ('2025-09-23 20:52:18.950191', 5, 10, 0)
2025-09-23 20:52:18,954 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:52:48,956 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:52:48,957 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:52:48,957 INFO sqlalchemy.engine.Engine [cached since 1904s ago] ('2025-09-23 20:52:48.955743', 5, 10, 0)
2025-09-23 20:52:49,020 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:53:19,024 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:53:19,032 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:53:19,033 INFO sqlalchemy.engine.Engine [cached since 1934s ago] ('2025-09-23 20:53:19.022690', 5, 10, 0)
2025-09-23 20:53:19,034 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:53:49,036 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:53:49,039 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:53:49,040 INFO sqlalchemy.engine.Engine [cached since 1964s ago] ('2025-09-23 20:53:49.036287', 5, 10, 0)
2025-09-23 20:53:49,040 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:54:19,101 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:54:19,106 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:54:19,106 INFO sqlalchemy.engine.Engine [cached since 1995s ago] ('2025-09-23 20:54:19.100706', 5, 10, 0)
2025-09-23 20:54:19,108 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:54:49,179 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:54:49,181 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:54:49,181 INFO sqlalchemy.engine.Engine [cached since 2025s ago] ('2025-09-23 20:54:49.179322', 5, 10, 0)
2025-09-23 20:54:49,182 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:55:19,278 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:55:19,341 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:55:19,341 INFO sqlalchemy.engine.Engine [cached since 2055s ago] ('2025-09-23 20:55:19.277850', 5, 10, 0)
2025-09-23 20:55:19,422 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:55:49,505 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:55:49,505 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:55:49,505 INFO sqlalchemy.engine.Engine [cached since 2085s ago] ('2025-09-23 20:55:49.503168', 5, 10, 0)
2025-09-23 20:55:49,514 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:56:19,518 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:56:19,579 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:56:19,580 INFO sqlalchemy.engine.Engine [cached since 2115s ago] ('2025-09-23 20:56:19.518067', 5, 10, 0)
2025-09-23 20:56:19,580 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:56:49,592 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:56:49,598 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:56:49,599 INFO sqlalchemy.engine.Engine [cached since 2145s ago] ('2025-09-23 20:56:49.592201', 5, 10, 0)
2025-09-23 20:56:49,600 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:57:19,658 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:57:19,659 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:57:19,660 INFO sqlalchemy.engine.Engine [cached since 2175s ago] ('2025-09-23 20:57:19.658056', 5, 10, 0)
2025-09-23 20:57:19,661 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:57:49,663 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:57:49,663 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:57:49,663 INFO sqlalchemy.engine.Engine [cached since 2205s ago] ('2025-09-23 20:57:49.662637', 5, 10, 0)
2025-09-23 20:57:49,664 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:58:19,664 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:58:19,665 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:58:19,668 INFO sqlalchemy.engine.Engine [cached since 2235s ago] ('2025-09-23 20:58:19.664112', 5, 10, 0)
2025-09-23 20:58:19,669 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:58:49,671 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:58:49,671 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:58:49,671 INFO sqlalchemy.engine.Engine [cached since 2265s ago] ('2025-09-23 20:58:49.670970', 5, 10, 0)
2025-09-23 20:58:49,675 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:59:19,676 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:59:19,678 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:59:19,679 INFO sqlalchemy.engine.Engine [cached since 2295s ago] ('2025-09-23 20:59:19.676217', 5, 10, 0)
2025-09-23 20:59:19,681 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 20:59:49,683 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 20:59:49,683 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 20:59:49,683 INFO sqlalchemy.engine.Engine [cached since 2325s ago] ('2025-09-23 20:59:49.682696', 5, 10, 0)
2025-09-23 20:59:49,747 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:00:19,748 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:00:19,750 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:00:19,752 INFO sqlalchemy.engine.Engine [cached since 2355s ago] ('2025-09-23 21:00:19.748160', 5, 10, 0)
2025-09-23 21:00:19,753 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:00:49,819 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:00:49,819 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:00:49,819 INFO sqlalchemy.engine.Engine [cached since 2385s ago] ('2025-09-23 21:00:49.818928', 5, 10, 0)
2025-09-23 21:00:49,820 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:01:20,059 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:01:20,059 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:01:20,059 INFO sqlalchemy.engine.Engine [cached since 2416s ago] ('2025-09-23 21:01:20.058704', 5, 10, 0)
2025-09-23 21:01:20,298 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:01:50,299 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:01:50,300 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:01:50,300 INFO sqlalchemy.engine.Engine [cached since 2446s ago] ('2025-09-23 21:01:50.299394', 5, 10, 0)
2025-09-23 21:01:50,301 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:02:20,308 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:02:20,308 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:02:20,308 INFO sqlalchemy.engine.Engine [cached since 2476s ago] ('2025-09-23 21:02:20.307567', 5, 10, 0)
2025-09-23 21:02:20,308 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:02:50,328 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:02:50,328 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:02:50,328 INFO sqlalchemy.engine.Engine [cached since 2506s ago] ('2025-09-23 21:02:50.328030', 5, 10, 0)
2025-09-23 21:02:50,379 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:03:20,398 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:03:20,458 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:03:20,459 INFO sqlalchemy.engine.Engine [cached since 2536s ago] ('2025-09-23 21:03:20.397962', 5, 10, 0)
2025-09-23 21:03:20,463 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:03:50,464 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:03:50,466 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:03:50,466 INFO sqlalchemy.engine.Engine [cached since 2566s ago] ('2025-09-23 21:03:50.464277', 5, 10, 0)
2025-09-23 21:03:50,624 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:04:20,626 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:04:20,628 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:04:20,628 INFO sqlalchemy.engine.Engine [cached since 2596s ago] ('2025-09-23 21:04:20.625913', 5, 10, 0)
2025-09-23 21:04:20,629 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:04:50,699 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:04:50,719 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:04:50,719 INFO sqlalchemy.engine.Engine [cached since 2626s ago] ('2025-09-23 21:04:50.698010', 5, 10, 0)
2025-09-23 21:04:50,779 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:05:20,782 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:05:20,783 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:05:20,783 INFO sqlalchemy.engine.Engine [cached since 2656s ago] ('2025-09-23 21:05:20.781990', 5, 10, 0)
2025-09-23 21:05:20,784 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:05:50,785 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:05:50,786 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:05:50,786 INFO sqlalchemy.engine.Engine [cached since 2686s ago] ('2025-09-23 21:05:50.785159', 5, 10, 0)
2025-09-23 21:05:50,788 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:06:20,789 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:06:20,792 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:06:20,793 INFO sqlalchemy.engine.Engine [cached since 2716s ago] ('2025-09-23 21:06:20.789174', 5, 10, 0)
2025-09-23 21:06:20,794 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:06:50,858 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:06:50,861 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:06:50,861 INFO sqlalchemy.engine.Engine [cached since 2746s ago] ('2025-09-23 21:06:50.858079', 5, 10, 0)
2025-09-23 21:06:50,862 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:07:20,875 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:07:20,876 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:07:20,876 INFO sqlalchemy.engine.Engine [cached since 2776s ago] ('2025-09-23 21:07:20.874749', 5, 10, 0)
2025-09-23 21:07:20,879 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:07:51,028 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:07:51,030 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:07:51,030 INFO sqlalchemy.engine.Engine [cached since 2806s ago] ('2025-09-23 21:07:51.028151', 5, 10, 0)
2025-09-23 21:07:51,036 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:08:21,037 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:08:21,038 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:08:21,038 INFO sqlalchemy.engine.Engine [cached since 2836s ago] ('2025-09-23 21:08:21.036937', 5, 10, 0)
2025-09-23 21:08:21,039 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:08:51,108 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:08:51,108 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:08:51,108 INFO sqlalchemy.engine.Engine [cached since 2867s ago] ('2025-09-23 21:08:51.107965', 5, 10, 0)
2025-09-23 21:08:51,111 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:09:21,113 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:09:21,117 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:09:21,117 INFO sqlalchemy.engine.Engine [cached since 2897s ago] ('2025-09-23 21:09:21.112977', 5, 10, 0)
2025-09-23 21:09:21,120 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:09:51,260 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:09:51,261 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:09:51,262 INFO sqlalchemy.engine.Engine [cached since 2927s ago] ('2025-09-23 21:09:51.121164', 5, 10, 0)
2025-09-23 21:09:51,263 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:10:21,265 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:10:21,266 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:10:21,266 INFO sqlalchemy.engine.Engine [cached since 2957s ago] ('2025-09-23 21:10:21.265510', 5, 10, 0)
2025-09-23 21:10:21,266 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:10:51,339 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:10:51,339 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:10:51,340 INFO sqlalchemy.engine.Engine [cached since 2987s ago] ('2025-09-23 21:10:51.338574', 5, 10, 0)
2025-09-23 21:10:51,341 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:11:21,345 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:11:21,346 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:11:21,347 INFO sqlalchemy.engine.Engine [cached since 3017s ago] ('2025-09-23 21:11:21.342411', 5, 10, 0)
2025-09-23 21:11:21,348 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:11:51,350 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:11:51,350 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:11:51,350 INFO sqlalchemy.engine.Engine [cached since 3047s ago] ('2025-09-23 21:11:51.349653', 5, 10, 0)
2025-09-23 21:11:51,364 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:12:21,580 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:12:21,581 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:12:21,581 INFO sqlalchemy.engine.Engine [cached since 3077s ago] ('2025-09-23 21:12:21.580239', 5, 10, 0)
2025-09-23 21:12:21,582 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:12:51,582 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:12:51,583 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:12:51,583 INFO sqlalchemy.engine.Engine [cached since 3107s ago] ('2025-09-23 21:12:51.582409', 5, 10, 0)
2025-09-23 21:12:51,584 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:13:21,586 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:13:21,587 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:13:21,587 INFO sqlalchemy.engine.Engine [cached since 3137s ago] ('2025-09-23 21:13:21.586199', 5, 10, 0)
2025-09-23 21:13:21,593 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:13:51,594 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:13:51,596 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:13:51,596 INFO sqlalchemy.engine.Engine [cached since 3167s ago] ('2025-09-23 21:13:51.594314', 5, 10, 0)
2025-09-23 21:13:51,598 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:14:21,603 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:14:21,603 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:14:21,603 INFO sqlalchemy.engine.Engine [cached since 3197s ago] ('2025-09-23 21:14:21.602954', 5, 10, 0)
2025-09-23 21:14:21,604 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:14:51,659 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:14:51,659 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:14:51,663 INFO sqlalchemy.engine.Engine [cached since 3227s ago] ('2025-09-23 21:14:51.658345', 5, 10, 0)
2025-09-23 21:14:51,669 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:15:21,675 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:15:21,676 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:15:21,676 INFO sqlalchemy.engine.Engine [cached since 3257s ago] ('2025-09-23 21:15:21.675382', 5, 10, 0)
2025-09-23 21:15:21,738 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:15:51,739 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:15:51,740 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:15:51,741 INFO sqlalchemy.engine.Engine [cached since 3287s ago] ('2025-09-23 21:15:51.739249', 5, 10, 0)
2025-09-23 21:15:51,745 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:16:21,746 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:16:21,748 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:16:21,748 INFO sqlalchemy.engine.Engine [cached since 3317s ago] ('2025-09-23 21:16:21.746186', 5, 10, 0)
2025-09-23 21:16:21,750 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:16:51,898 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:16:51,898 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:16:51,899 INFO sqlalchemy.engine.Engine [cached since 3347s ago] ('2025-09-23 21:16:51.897871', 5, 10, 0)
2025-09-23 21:16:51,900 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:17:21,918 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:17:21,919 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:17:21,919 INFO sqlalchemy.engine.Engine [cached since 3377s ago] ('2025-09-23 21:17:21.917260', 5, 10, 0)
2025-09-23 21:17:21,920 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:17:51,982 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:17:51,982 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:17:51,985 INFO sqlalchemy.engine.Engine [cached since 3407s ago] ('2025-09-23 21:17:51.981991', 5, 10, 0)
2025-09-23 21:17:51,987 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:18:22,072 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:18:22,313 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:18:22,319 INFO sqlalchemy.engine.Engine [cached since 3438s ago] ('2025-09-23 21:18:22.072120', 5, 10, 0)
2025-09-23 21:18:22,320 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:18:52,387 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:18:52,388 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:18:52,388 INFO sqlalchemy.engine.Engine [cached since 3468s ago] ('2025-09-23 21:18:52.387014', 5, 10, 0)
2025-09-23 21:18:52,392 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:19:22,393 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:19:22,393 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:19:22,394 INFO sqlalchemy.engine.Engine [cached since 3498s ago] ('2025-09-23 21:19:22.393149', 5, 10, 0)
2025-09-23 21:19:22,459 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:19:52,538 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:19:52,539 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:19:52,539 INFO sqlalchemy.engine.Engine [cached since 3528s ago] ('2025-09-23 21:19:52.538334', 5, 10, 0)
2025-09-23 21:19:52,542 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:20:22,620 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:20:22,621 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:20:22,621 INFO sqlalchemy.engine.Engine [cached since 3558s ago] ('2025-09-23 21:20:22.620290', 5, 10, 0)
2025-09-23 21:20:22,625 INFO sqlalchemy.engine.Engine ROLLBACK
2025-09-23 21:20:52,699 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-09-23 21:20:52,701 INFO sqlalchemy.engine.Engine SELECT dlq_messages.id, dlq_messages.provider, dlq_messages.event_id, dlq_messages.payload_json, dlq_messages.error_kind, dlq_messages.attempts, dlq_messages.next_retry_at, dlq_messages.created_at 
FROM dlq_messages 
WHERE dlq_messages.next_retry_at <= ? AND dlq_messages.attempts < ?
 LIMIT ? OFFSET ?
2025-09-23 21:20:52,702 INFO sqlalchemy.engine.Engine [cached since 3588s ago] ('2025-09-23 21:20:52.699029', 5, 10, 0)
2025-09-23 21:20:52,703 INFO sqlalchemy.engine.Engine ROLLBACK
