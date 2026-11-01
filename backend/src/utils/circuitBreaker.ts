/**
 * @file circuitBreaker.ts
 * @description Implementación minimalista y robusta de Circuit Breaker para protección de base de datos.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

type State = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export class CircuitBreaker {
  private state: State = 'CLOSED';
  private failures = 0;
  private openedAt = 0;

  constructor(
    private readonly threshold = 5,
    private readonly resetMs = 30_000,
    private readonly timeoutMs = 3_000
  ) {}

  public getState(): State {
    return this.state;
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.openedAt > this.resetMs) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('CIRCUIT_OPEN: El circuito de base de datos está abierto para proteger la infraestructura.');
      }
    }

    let timer: NodeJS.Timeout | undefined;
    try {
      const result = await Promise.race([
        fn(),
        new Promise<never>((_, rej) => {
          timer = setTimeout(() => rej(new Error('CIRCUIT_TIMEOUT: Tiempo de espera de base de datos agotado.')), this.timeoutMs);
        }),
      ]);
      this.failures = 0;
      this.state = 'CLOSED';
      return result;
    } catch (err) {
      this.failures += 1;
      if (this.failures >= this.threshold) {
        this.state = 'OPEN';
        this.openedAt = Date.now();
      }
      throw err;
    } finally {
      if (timer) clearTimeout(timer);
    }
  }
}

export const dbBreaker = new CircuitBreaker(5, 30_000, 3_000);
