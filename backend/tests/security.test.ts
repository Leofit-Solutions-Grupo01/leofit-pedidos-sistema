// =============================================================================
// SECURITY, OWASP & SSL/TLS CRYPTOGRAPHIC AUDIT TESTS - LEOFIT SECURITY
// Fundamentado en Polanía Tovar (2024), ISO/IEC 25010:2023 e ISO/IEC/IEEE 29119
// =============================================================================

import crypto from 'node:crypto';
import request from 'supertest';
import { createApp } from '../src/app';
import {
  Aes256GcmCipher,
  auditTlsParameters,
  getSecureTlsOptions,
  MIN_RSA_KEY_BITS
} from '../src/infrastructure/security/tls.policy';

const app = createApp();

describe('Auditoría de Seguridad Web, OWASP Top 10 & Blindaje SSL/TLS (/api)', () => {
  it('Debe incluir cabeceras de seguridad HTTP (Helmet, HSTS RFC 6797 y Política TLS 1.3 AEAD)', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
    expect(res.headers['x-dns-prefetch-control']).toBeDefined();
    expect(res.headers['x-content-type-options']).toBe('nosniff');
    expect(['SAMEORIGIN', 'DENY']).toContain(res.headers['x-frame-options']);
    expect(res.headers['strict-transport-security']).toContain('max-age=31536000');
    expect(res.headers['strict-transport-security']).toContain('includeSubDomains');
    expect(res.headers['x-tls-policy']).toBe('TLSv1.3; AEAD=AES-256-GCM; KEX=ECDHE-X25519-PFS');
  });

  it('Debe neutralizar intentos de inyección SQL en consultas de búsqueda', async () => {
    const maliciousPayload = "' OR '1'='1; DROP TABLE users; --";
    const res = await request(app).get(`/api/products?search=${encodeURIComponent(maliciousPayload)}`);
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
  });

  it('Debe rechazar payloads malformados con XSS o tipos incorrectos en validación Zod', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: '<script>alert("xss")</script>',
        password: 12345 // type error
      });

    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });

  it('Debe validar la política criptográfica SSL/TLS rechazando Downgrade, RC4, CBC, FREAK (512-bit) y CRIME', () => {
    // 1. Configuración óptima TLS 1.3 AEAD + RSA 2048 + sin compresión
    const secureAudit = auditTlsParameters({
      protocolVersion: 'TLSv1.3',
      cipherSuite: 'TLS_AES_256_GCM_SHA384',
      rsaKeyBits: 2048,
      compressionEnabled: false
    });
    expect(secureAudit.valid).toBe(true);
    expect(secureAudit.reasons).toHaveLength(0);

    // 2. Ataque de degradación (Downgrade a SSLv3 / POODLE + CBC + Clave de exportación 512 bits FREAK + CRIME)
    const mitmAttackAudit = auditTlsParameters({
      protocolVersion: 'SSLv3',
      cipherSuite: 'EXP-RC4-MD5-CBC',
      rsaKeyBits: 512,
      compressionEnabled: true
    });
    expect(mitmAttackAudit.valid).toBe(false);
    expect(mitmAttackAudit.reasons.some((r) => r.includes('PROTOCOL_DOWNGRADE_REJECTED'))).toBe(true);
    expect(mitmAttackAudit.reasons.some((r) => r.includes('WEAK_CIPHERSUITE_REJECTED'))).toBe(true);
    expect(mitmAttackAudit.reasons.some((r) => r.includes('SHORT_KEY_FREAK_RISK'))).toBe(true);
    expect(mitmAttackAudit.reasons.some((r) => r.includes('TLS_COMPRESSION_CRIME_RISK'))).toBe(true);

    // 3. Opciones nativas de TLS con curvas elípticas seguras (X25519) para Perfect Forward Secrecy
    const tlsOpts = getSecureTlsOptions();
    expect(tlsOpts.minVersion).toBe('TLSv1.2');
    expect(tlsOpts.maxVersion).toBe('TLSv1.3');
    expect(tlsOpts.ecdhCurve).toContain('X25519');
    expect(MIN_RSA_KEY_BITS).toBe(2048);
  });

  it('Debe cifrar, autenticar y detectar manipulación MITM con AES-256-GCM (AEAD)', () => {
    const key = crypto.randomBytes(32); // 256 bits
    const secretOrderData = JSON.stringify({ orderId: 1050, totalSoles: '189.90', ruc: '20609874512' });
    const aad = 'leofit-order-transaction-v1';

    const encrypted = Aes256GcmCipher.encrypt(secretOrderData, key, aad);
    const decrypted = Aes256GcmCipher.decrypt(encrypted, key, aad);
    expect(decrypted).toBe(secretOrderData);

    // Simulación de ataque activo MITM que altera 1 byte del texto cifrado (debe fallar la verificación del GCM Tag)
    const tamperedCiphertext =
      (encrypted.ciphertextHex.startsWith('a') ? 'b' : 'a') + encrypted.ciphertextHex.slice(1);
    expect(() =>
      Aes256GcmCipher.decrypt({ ...encrypted, ciphertextHex: tamperedCiphertext }, key, aad)
    ).toThrow();
  });
});
