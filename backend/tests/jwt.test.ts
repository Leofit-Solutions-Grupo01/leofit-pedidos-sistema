import { JWTService } from '../src/infrastructure/security/jwt.utils';

describe('JWTService Fail-Fast Mechanism', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetModules(); // clears the cache
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  it('Debe arrojar un error si JWT_SECRET no está definido en el entorno', () => {
    delete process.env.JWT_SECRET;

    expect(() => {
      require('../src/infrastructure/security/jwt.utils');
    }).toThrow('FATAL ERROR: JWT_SECRET must be defined in the environment.');
  });

  it('Debe rechazar tokens manipulados con alg: none (Confusión de Algoritmo)', () => {
    process.env.JWT_SECRET = 'test_secret_for_algorithm';
    const JWTService = require('../src/infrastructure/security/jwt.utils').JWTService;
    // Creamos un token falso con alg: none, codificando el header y el payload en base64url sin firma
    const header = Buffer.from(JSON.stringify({ alg: 'none', typ: 'JWT' })).toString('base64url');
    const payload = Buffer.from(JSON.stringify({ userId: 1, role: 'ADMIN' })).toString('base64url');
    const token = `${header}.${payload}.`; // Sin firma

    const result = JWTService.verifyToken(token);
    expect(result).toBeNull();
  });
});
