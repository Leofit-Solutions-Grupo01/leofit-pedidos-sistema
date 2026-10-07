/**
 * k6_workload.js
 * Workload transaccional para evaluación de aislamiento en LeoFit Pedidos.
 *
 * Uso:
 *   k6 run --env ISOLATION_LEVEL=SERIALIZABLE --env BASE_URL=http://localhost:3000 \
 *          --vus 50 --duration 6m k6_workload.js
 */

import http from 'k6/http';
import { sleep } from 'k6';
import { Trend, Counter } from 'k6/metrics';
import exec from 'k6/execution';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const ISOLATION_LEVEL = __ENV.ISOLATION_LEVEL || 'READ COMMITTED';
const RAMP_UP_SECONDS = parseInt(__ENV.RAMP_UP_SECONDS || '60', 10);
const NUM_USERS = parseInt(__ENV.NUM_USERS || '50', 10);

const logicalTxnDuration = new Trend('logical_txn_duration_ms', true);
const logicalTxnSuccess = new Counter('logical_txn_success');
const logicalTxnFailed = new Counter('logical_txn_failed');
const endpointCatalog = new Counter('endpoint_catalog');
const endpointClientCreate = new Counter('endpoint_client_create');
const endpointCheckout = new Counter('endpoint_checkout');
const endpointStatusChange = new Counter('endpoint_status_change');

export const options = {
  scenarios: {
    leofit_workload: {
      executor: 'constant-vus',
      vus: parseInt(__ENV.VUS || '50', 10),
      duration: __ENV.DURATION || '6m',
      gracefulStop: '10s',
    },
  },
  thresholds: {
    http_req_failed: [],
    http_req_duration: [],
  },
};

export function setup() {
  console.log(JSON.stringify({
    event: 'setup_start',
    base_url: BASE_URL,
    isolation_level: ISOLATION_LEVEL,
    num_users: NUM_USERS,
  }));

  const tokens = [];
  // Utilizamos usuarios generados dinámicamente o los que se generen en el seed
  const credentials = getCredentials(NUM_USERS);

  for (const cred of credentials) {
    const res = http.post(
      `${BASE_URL}/api/auth/login`,
      JSON.stringify({ email: cred.email, password: cred.password }),
      { headers: { 'Content-Type': 'application/json' } }
    );
    if (res.status === 200) {
      const body = res.json();
      const token = body.data?.token ?? body.token ?? body.accessToken;
      if (token) {
        tokens.push(token);
      } else {
        console.warn(`token_missing_in_response: ${JSON.stringify(body).slice(0, 200)}`);
      }
    } else {
      console.warn(`login_failed email=${cred.email} status=${res.status}`);
    }
  }

  if (tokens.length === 0) {
    throw new Error('No se pudo autenticar ningún usuario. Abortando setup.');
  }

  const variantIds = [];
  const clientIds = [];
  let page = 1;
  const pageSize = 100;

  while (true) {
    const res = http.get(`${BASE_URL}/api/products/?page=${page}&limit=${pageSize}`, { headers: authHeader(tokens[0]) });
    if (res.status !== 200) break;
    const result = res.json();
    const items = result.data || result; // Por si hay paginación wrapper
    if (!items || items.length === 0) break;

    for (const product of items) {
      if (product.variants && Array.isArray(product.variants)) {
        for (const v of product.variants) {
          variantIds.push(v.id);
        }
      }
    }
    if (items.length < pageSize) break;
    page++;
  }

  page = 1;
  while (true) {
    const res = http.get(`${BASE_URL}/api/clients/?page=${page}&limit=${pageSize}`, { headers: authHeader(tokens[0]) });
    if (res.status !== 200) break;
    const result = res.json();
    const items = result.data || result;
    if (!items || items.length === 0) break;
    for (const c of items) clientIds.push(c.id);
    if (items.length < pageSize) break;
    page++;
  }

  console.log(JSON.stringify({
    event: 'setup_complete',
    tokens_count: tokens.length,
    variant_ids_count: variantIds.length,
    client_ids_count: clientIds.length,
  }));

  const zipfCdf = buildZipfCdf(variantIds.length, 0.9, 1000);

  return { tokens, variantIds, clientIds, zipfCdf };
}

export default function (data) {
  const { tokens, variantIds, clientIds, zipfCdf } = data;
  const vuIndex = exec.vu.idInTest;
  const userToken = tokens[(vuIndex - 1) % tokens.length];

  const elapsedSeconds = (Date.now() - exec.scenario.startTime) / 1000;
  
  if (elapsedSeconds < RAMP_UP_SECONDS) {
    if (elapsedSeconds < 30) {
      const result = doCheckout(userToken, variantIds, clientIds, zipfCdf, 1 + Math.floor(Math.random() * 3));
      endpointCheckout.add(1);
      if (result.ok) {
        logicalTxnSuccess.add(1);
      } else {
        logicalTxnFailed.add(1);
      }
      sleep(0.1 + Math.random() * 0.2);
      return;  // No emitir log JSON durante ramp-up
    }
  }

  const roll = Math.random() * 100;
  let result;
  
  if (roll < 50) {
    result = doCatalog(userToken);
    endpointCatalog.add(1);
  } else if (roll < 80) {
    result = doClientCreate(userToken);
    endpointClientCreate.add(1);
  } else if (roll < 95) {
    result = doCheckout(userToken, variantIds, clientIds, zipfCdf, 1 + Math.floor(Math.random() * 3));
    endpointCheckout.add(1);
  } else {
    result = doStatusChange(userToken);
    endpointStatusChange.add(1);
  }

  if (result.ok) {
    logicalTxnSuccess.add(1);
    logicalTxnDuration.add(result.durationMs);
  } else {
    logicalTxnFailed.add(1);
  }

  if (elapsedSeconds >= RAMP_UP_SECONDS) {
    console.log(JSON.stringify({
      event: 'logical_txn',
      transaction_id: result.txnId,
      endpoint: result.endpoint,
      isolation_level: ISOLATION_LEVEL,
      vu: vuIndex,
      attempt_number: 1, // Gestionado por backend
      start_ts: result.startTs,
      end_ts: result.endTs,
      latency_ms: result.durationMs,
      http_status: result.httpStatus,
      ok: result.ok,
    }));
  }

  sleep(0.1 + Math.random() * 0.3);
}

function doCatalog(token) {
  const txnId = newTxnId();
  const startTs = Date.now();
  const res = http.get(`${BASE_URL}/api/products/?page=1&limit=20`, { headers: authHeader(token), tags: { endpoint: 'catalog' } });
  const endTs = Date.now();
  return buildResult(txnId, 'catalog', startTs, endTs, res);
}

function doClientCreate(token) {
  const txnId = newTxnId();
  const startTs = Date.now();
  const email = `test-${txnId}@leofit.test`;
  const res = http.post(
    `${BASE_URL}/api/clients/`,
    JSON.stringify({
      fullName: `Test Client ${txnId}`,
      email,
      phone: `+51${Math.floor(900000000 + Math.random() * 99999999)}`,
      address: 'Calle Falsa 123',
      district: 'La Victoria'
    }),
    { headers: { ...authHeader(token), 'Content-Type': 'application/json' }, tags: { endpoint: 'client_create' } }
  );
  const endTs = Date.now();
  return buildResult(txnId, 'client_create', startTs, endTs, res);
}

function doCheckout(token, variantIds, clientIds, zipfCdf, numItems) {
  const txnId = newTxnId();
  const startTs = Date.now();

  if (variantIds.length === 0 || clientIds.length === 0) {
    return { ok: false, txnId, endpoint: 'checkout', startTs, endTs: startTs, durationMs: 0, httpStatus: 0 };
  }

  const items = [];
  const seen = new Set();
  for (let i = 0; i < numItems; i++) {
    let vid;
    let attempts = 0;
    do {
      vid = sampleZipf(zipfCdf, variantIds);
      attempts++;
    } while (seen.has(vid) && attempts < 5);
    seen.add(vid);
    items.push({ variantId: vid, quantity: 1, unitPrice: 50.0 }); // Ajustado a camelCase según backend
  }

  const clientId = clientIds[Math.floor(Math.random() * clientIds.length)];

  const res = http.post(
    `${BASE_URL}/api/orders/`,
    JSON.stringify({ clientId: clientId, items, paymentMethod: 'YAPE', shippingCost: 10 }), // Ajustado a DTO
    {
      headers: {
        ...authHeader(token),
        'Content-Type': 'application/json',
        'X-Isolation-Level': ISOLATION_LEVEL,
      },
      tags: { endpoint: 'checkout' },
    }
  );
  const endTs = Date.now();
  return buildResult(txnId, 'checkout', startTs, endTs, res);
}

function doStatusChange(token) {
  const txnId = newTxnId();
  const startTs = Date.now();
  const orderId = Math.floor(1 + Math.random() * 500); // Esto se mejorará iterando orders válidos si se requiere
  const res = http.patch(
    `${BASE_URL}/api/orders/${orderId}/status`,
    JSON.stringify({ status: 'EN_CAMINO' }),
    { headers: { ...authHeader(token), 'Content-Type': 'application/json' }, tags: { endpoint: 'status_change' } }
  );
  const endTs = Date.now();
  return buildResult(txnId, 'status_change', startTs, endTs, res);
}

function authHeader(token) { return { Authorization: `Bearer ${token}` }; }

let txnCounter = 0;
function newTxnId() { return `${Date.now()}-${exec.vu.idInTest}-${++txnCounter}-${Math.random().toString(36).slice(2, 8)}`; }

function buildResult(txnId, endpoint, startTs, endTs, res) {
  const ok = res.status >= 200 && res.status < 400;
  return { ok, txnId, endpoint, startTs, endTs, durationMs: endTs - startTs, httpStatus: res.status };
}

function buildZipfCdf(n, theta, buckets) {
  const cdf = new Array(buckets);
  let sum = 0;
  const weights = new Array(buckets);
  for (let i = 0; i < buckets; i++) {
    const k = 1 + (i * (n - 1)) / (buckets - 1);
    weights[i] = 1 / Math.pow(k, theta);
    sum += weights[i];
  }
  let acc = 0;
  for (let i = 0; i < buckets; i++) {
    acc += weights[i] / sum;
    cdf[i] = acc;
  }
  return cdf;
}

function sampleZipf(cdf, variantIds) {
  const u = Math.random();
  let lo = 0;
  let hi = cdf.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (cdf[mid] < u) lo = mid + 1;
    else hi = mid;
  }
  const idx = Math.floor((lo * variantIds.length) / cdf.length);
  return variantIds[Math.min(idx, variantIds.length - 1)];
}

function getCredentials(n) {
  const creds = [];
  // Agrego los nativos del seed actual para el smoke test
  creds.push({ email: 'admin@leofit.pe', password: 'password' });
  creds.push({ email: 'operador@leofit.pe', password: 'password' });
  // Para los que genere el seed de 50k
  for (let i = 1; i <= n; i++) {
    creds.push({ email: `operator${i}@leofit.pe`, password: 'password' });
  }
  return creds;
}
