import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = { vus: 1, duration: '10s' };

export default function () {
  const res = http.get('http://localhost:8001/healthz', { headers: { 'X-API-Key': 'demo-key' } });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
