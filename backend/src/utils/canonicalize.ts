/**
 * @file canonicalize.ts
 * @description Implementación exacta del estándar RFC 8785 (JSON Canonicalization Scheme - JCS).
 * @reference https://datatracker.ietf.org/doc/html/rfc8785
 */

function serializeString(value: string): string {
  if (typeof (value as any).isWellFormed === 'function' && !(value as any).isWellFormed()) {
    throw new Error('Lone surrogate is not allowed in RFC 8785');
  }
  return JSON.stringify(value);
}

function serializePrimitive(value: any): string {
  switch (typeof value) {
    case 'number':
      if (isNaN(value)) {
        throw new Error('NaN is not allowed in RFC 8785');
      }
      if (!isFinite(value)) {
        throw new Error('Infinity is not allowed in RFC 8785');
      }
      return JSON.stringify(value);
    case 'string':
      return serializeString(value);
    case 'boolean':
      return value ? 'true' : 'false';
    default:
      return JSON.stringify(value);
  }
}

interface Frame {
  container: any;
  keys: string[] | null;
  index: number;
  first: boolean;
  wrappers: any[] | null;
}

function enterValue(value: any, seen: Set<any>): Frame | string | undefined {
  let wrappers: any[] | null = null;
  while (value !== null && typeof value === 'object' && typeof value.toJSON === 'function') {
    if (seen.has(value)) {
      throw new Error('Circular reference detected');
    }
    seen.add(value);
    (wrappers ??= []).push(value);
    value = value.toJSON();
  }

  if (value instanceof Number || value instanceof String || value instanceof Boolean) {
    value = value.valueOf();
  }

  if (value === null || typeof value !== 'object') {
    if (wrappers !== null) {
      for (const wrapper of wrappers) seen.delete(wrapper);
    }
    return serializePrimitive(value);
  }

  if (seen.has(value)) {
    throw new Error('Circular reference detected');
  }
  seen.add(value);

  return {
    container: value,
    keys: Array.isArray(value) ? null : Object.keys(value).sort(),
    index: 0,
    first: true,
    wrappers
  };
}

/**
 * Serializa cualquier estructura de datos JSON conforme a RFC 8785 (JCS).
 */
export function canonicalize(object: any): string {
  if (object === null || typeof object !== 'object') {
    return serializePrimitive(object);
  }

  const seen = new Set<any>();
  const root = enterValue(object, seen);
  if (typeof root !== 'object') {
    return root as string;
  }

  let result = root.keys === null ? '[' : '{';
  const stack: Frame[] = [root];

  outer:
  while (stack.length > 0) {
    const frame = stack[stack.length - 1];
    const container = frame.container;

    if (frame.keys === null) {
      while (frame.index < container.length) {
        const i = frame.index++;
        if (i > 0) {
          result += ',';
        }
        const element = container[i];
        const val = element === undefined || typeof element === 'symbol' || typeof element === 'function' ? null : element;
        if (val === null || typeof val !== 'object') {
          result += serializePrimitive(val);
          continue;
        }
        const child = enterValue(val, seen);
        if (typeof child !== 'object') {
          result += child === undefined ? 'null' : child;
          continue;
        }
        result += child.keys === null ? '[' : '{';
        stack.push(child);
        continue outer;
      }
      result += ']';
    } else {
      const keys = frame.keys;
      while (frame.index < keys.length) {
        const key = keys[frame.index++];
        const val = container[key];
        if (val === undefined || typeof val === 'symbol' || typeof val === 'function') {
          continue;
        }
        if (val === null || typeof val !== 'object') {
          if (frame.first) {
            frame.first = false;
          } else {
            result += ',';
          }
          result += serializeString(key) + ':' + serializePrimitive(val);
          continue;
        }
        const child = enterValue(val, seen);
        if (child === undefined) {
          continue;
        }
        if (frame.first) {
          frame.first = false;
        } else {
          result += ',';
        }
        result += serializeString(key) + ':';
        if (typeof child !== 'object') {
          result += child;
          continue;
        }
        result += child.keys === null ? '[' : '{';
        stack.push(child);
        continue outer;
      }
      result += '}';
    }

    seen.delete(container);
    if (frame.wrappers !== null) {
      for (const wrapper of frame.wrappers) seen.delete(wrapper);
    }
    stack.pop();
  }

  return result;
}

export default canonicalize;
