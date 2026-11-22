// =============================================================================
// TLS 1.2/1.3 & CRYPTOGRAPHIC HARDENING POLICY - LEOFIT SECURITY
// Fundamentado en Polanía Tovar (2024), RFC 8446 (TLS 1.3), RFC 7525 y RFC 7465
// =============================================================================

import crypto from 'node:crypto';
import tls from 'node:tls';

/**
 * Protocolos heredados estrictamente prohibidos por vulnerabilidades conocidas:
 * - SSLv2 / SSLv3: Vulnerables a DROWN y POODLE (Padding Oracle).
 * - TLSv1.0 / TLSv1.1: Vulnerables a BEAST, CRIME y carecen de AEAD moderno.
 */
export const PROHIBITED_TLS_VERSIONS = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.0', 'TLSv1.1'] as const;

/**
 * Versiones TLS permitidas en tránsito (Mínimo TLS 1.2, Preferido TLS 1.3).
 */
export const ALLOWED_TLS_VERSIONS = ['TLSv1.2', 'TLSv1.3'] as const;

/**
 * Conjuntos de cifrado (Ciphersuites) aprobados:
 * Exclusivamente AEAD (Galois/Counter Mode - GCM y ChaCha20-Poly1305) con
 * intercambio de claves efímero ECDHE para Perfect Forward Secrecy (PFS).
 */
export const APPROVED_CIPHERSUITES = [
  // TLS 1.3 AEAD Ciphersuites (RFC 8446)
  'TLS_AES_256_GCM_SHA384',
  'TLS_CHACHA20_POLY1305_SHA256',
  'TLS_AES_128_GCM_SHA256',
  // TLS 1.2 AEAD + ECDHE (PFS) Ciphersuites
  'ECDHE-ECDSA-AES256-GCM-SHA384',
  'ECDHE-RSA-AES256-GCM-SHA384',
  'ECDHE-ECDSA-CHACHA20-POLY1305',
  'ECDHE-RSA-CHACHA20-POLY1305',
  'ECDHE-ECDSA-AES128-GCM-SHA256',
  'ECDHE-RSA-AES128-GCM-SHA256'
] as const;

/**
 * Primitivas y modos prohibidos (Mitigación de FREAK, Logjam, RC4 bias, Sweet32 y POODLE):
 * - RC4: Cifrado de flujo vulnerado en 2013 (RFC 7465).
 * - DES / 3DES: Bloques de 64 bits vulnerables a fuerza bruta (56 bits) y Sweet32.
 * - EXPORT / EXP / LOW / 512: Claves cortas de grado de exportación (Ataque FREAK).
 * - NULL / aNULL / eNULL: Sin cifrado o sin autenticación.
 * - MD5 / SHA1: Funciones hash con colisiones demostradas.
 * - ECB / CBC: Modos de bloque vulnerables a patrones o Padding Oracle.
 */
export const PROHIBITED_CIPHER_PATTERNS = [
  /RC4/i,
  /\bDES\b/i,
  /3DES/i,
  /DES-CBC/i,
  /EXPORT/i,
  /\bEXP\b/i,
  /NULL/i,
  /MD5/i,
  /\bAECDH\b/i,
  /\bADH\b/i,
  /CBC/i,
  /ECB/i
] as const;

/**
 * Curvas elípticas (ECC) aprobadas para ECDHE (Previene Cross-Protocol ECC Attacks).
 */
export const APPROVED_ECC_CURVES = ['X25519', 'prime256v1', 'secp384r1'] as const;

/**
 * Longitud mínima de clave RSA exigida (2048 bits = 112 bits de seguridad simétrica).
 * Claves de 512 bits (Export) o 1024 bits son rechazadas.
 */
export const MIN_RSA_KEY_BITS = 2048;

export interface TlsAuditResult {
  valid: boolean;
  reasons: string[];
}

/**
 * Audita si una configuración de versión TLS, ciphersuite y longitud RSA cumple
 * las políticas criptográficas contra ataques MITM, Downgrade y FREAK.
 */
export function auditTlsParameters(params: {
  protocolVersion: string;
  cipherSuite: string;
  rsaKeyBits?: number;
  compressionEnabled?: boolean;
}): TlsAuditResult {
  const reasons: string[] = [];

  if (!ALLOWED_TLS_VERSIONS.includes(params.protocolVersion as any)) {
    reasons.push(`PROTOCOL_DOWNGRADE_REJECTED: ${params.protocolVersion} está prohibido.`);
  }

  for (const pattern of PROHIBITED_CIPHER_PATTERNS) {
    if (pattern.test(params.cipherSuite)) {
      reasons.push(`WEAK_CIPHERSUITE_REJECTED: ${params.cipherSuite} contiene primitiva insegura (${pattern.source}).`);
      break;
    }
  }

  if (typeof params.rsaKeyBits === 'number' && params.rsaKeyBits < MIN_RSA_KEY_BITS) {
    reasons.push(`SHORT_KEY_FREAK_RISK: Clave RSA de ${params.rsaKeyBits} bits inferior al mínimo de ${MIN_RSA_KEY_BITS} bits.`);
  }

  if (params.compressionEnabled === true) {
    reasons.push('TLS_COMPRESSION_CRIME_RISK: La compresión a nivel TLS debe estar desactivada para prevenir CRIME/BREACH.');
  }

  return {
    valid: reasons.length === 0,
    reasons
  };
}

/**
 * Construye las opciones seguras de TLS para servidores o conexiones salientes Node.js.
 */
export function getSecureTlsOptions(): tls.TlsOptions {
  return {
    minVersion: 'TLSv1.2',
    maxVersion: 'TLSv1.3',
    ciphers: APPROVED_CIPHERSUITES.join(':'),
    honorCipherOrder: true,
    ecdhCurve: APPROVED_ECC_CURVES.join(':')
  };
}

/**
 * Cifrado Simétrico Autenticado AEAD con AES-256-GCM (Bloques de 128 bits, Clave de 256 bits).
 * Proporciona simultáneamente Confidencialidad e Integridad (Authentication Tag de 128 bits),
 * erradicando las vulnerabilidades de relleno de CBC y patrones de ECB.
 */
export class Aes256GcmCipher {
  private static readonly ALGORITHM = 'aes-256-gcm';
  private static readonly IV_LENGTH_BYTES = 12; // 96 bits recomendados por NIST SP 800-38D
  private static readonly TAG_LENGTH_BYTES = 16; // 128 bits authentication tag

  public static encrypt(plaintext: string, key32Bytes: Buffer, aad?: string): {
    ciphertextHex: string;
    ivHex: string;
    authTagHex: string;
  } {
    if (key32Bytes.length !== 32) {
      throw new Error('AES_256_INVALID_KEY_LENGTH: Se requiere una clave exacta de 32 bytes (256 bits).');
    }

    const iv = crypto.randomBytes(this.IV_LENGTH_BYTES);
    const cipher = crypto.createCipheriv(this.ALGORITHM, key32Bytes, iv, {
      authTagLength: this.TAG_LENGTH_BYTES
    });

    if (aad) {
      cipher.setAAD(Buffer.from(aad, 'utf8'));
    }

    const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
    const authTag = cipher.getAuthTag();

    return {
      ciphertextHex: encrypted.toString('hex'),
      ivHex: iv.toString('hex'),
      authTagHex: authTag.toString('hex')
    };
  }

  public static decrypt(
    payload: { ciphertextHex: string; ivHex: string; authTagHex: string },
    key32Bytes: Buffer,
    aad?: string
  ): string {
    if (key32Bytes.length !== 32) {
      throw new Error('AES_256_INVALID_KEY_LENGTH: Se requiere una clave exacta de 32 bytes (256 bits).');
    }

    const iv = Buffer.from(payload.ivHex, 'hex');
    const authTag = Buffer.from(payload.authTagHex, 'hex');
    const ciphertext = Buffer.from(payload.ciphertextHex, 'hex');

    if (iv.length !== this.IV_LENGTH_BYTES || authTag.length !== this.TAG_LENGTH_BYTES) {
      throw new Error('AES_256_GCM_INVALID_PARAMETERS');
    }

    const decipher = crypto.createDecipheriv(this.ALGORITHM, key32Bytes, iv, {
      authTagLength: this.TAG_LENGTH_BYTES
    });

    if (aad) {
      decipher.setAAD(Buffer.from(aad, 'utf8'));
    }

    decipher.setAuthTag(authTag);

    const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
    return decrypted.toString('utf8');
  }
}
