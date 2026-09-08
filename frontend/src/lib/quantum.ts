// A small, real state-vector quantum simulator (up to a few qubits).
// Qubit q maps to bit (n - 1 - q) so |q0 q1 q2> reads left-to-right.

export type Complex = { re: number; im: number }

const c = (re: number, im = 0): Complex => ({ re, im })
const cadd = (a: Complex, b: Complex): Complex => ({ re: a.re + b.re, im: a.im + b.im })
const cmul = (a: Complex, b: Complex): Complex => ({
  re: a.re * b.re - a.im * b.im,
  im: a.re * b.im + a.im * b.re,
})
const cabs2 = (a: Complex) => a.re * a.re + a.im * a.im

export type SingleGate = 'H' | 'X' | 'Y' | 'Z' | 'S' | 'T'

const SQRT1_2 = Math.SQRT1_2

const GATES: Record<SingleGate, [Complex, Complex, Complex, Complex]> = {
  H: [c(SQRT1_2), c(SQRT1_2), c(SQRT1_2), c(-SQRT1_2)],
  X: [c(0), c(1), c(1), c(0)],
  Y: [c(0), c(0, -1), c(0, 1), c(0)],
  Z: [c(1), c(0), c(0), c(-1)],
  S: [c(1), c(0), c(0), c(0, 1)],
  T: [c(1), c(0), c(0), c(Math.cos(Math.PI / 4), Math.sin(Math.PI / 4))],
}

export type Op =
  | { kind: 'single'; gate: SingleGate; qubit: number }
  | { kind: 'cnot'; control: number; target: number }
  | { kind: 'swap'; a: number; b: number }

export type SimResult = {
  n: number
  amplitudes: Complex[]
  distribution: { state: string; prob: number }[]
  perQubit: { qubit: number; p0: number; p1: number }[]
  topState: string
}

function bit(index: number, n: number, qubit: number) {
  return (index >> (n - 1 - qubit)) & 1
}

function applySingle(state: Complex[], n: number, gate: SingleGate, qubit: number) {
  const [a, b, cc, d] = GATES[gate]
  const next = state.slice()
  const bitpos = n - 1 - qubit
  const mask = 1 << bitpos
  for (let i = 0; i < state.length; i++) {
    if ((i & mask) === 0) {
      const j = i | mask
      const x0 = state[i]
      const x1 = state[j]
      next[i] = cadd(cmul(a, x0), cmul(b, x1))
      next[j] = cadd(cmul(cc, x0), cmul(d, x1))
    }
  }
  return next
}

function applyCNOT(state: Complex[], n: number, control: number, target: number) {
  const out = new Array<Complex>(state.length)
  for (let i = 0; i < state.length; i++) {
    if (bit(i, n, control) === 1) {
      const tmask = 1 << (n - 1 - target)
      out[i] = state[i ^ tmask]
    } else {
      out[i] = state[i]
    }
  }
  return out
}

function applySWAP(state: Complex[], n: number, a: number, b: number) {
  const out = new Array<Complex>(state.length)
  for (let i = 0; i < state.length; i++) {
    const ba = bit(i, n, a)
    const bb = bit(i, n, b)
    if (ba === bb) {
      out[i] = state[i]
    } else {
      const j = i ^ (1 << (n - 1 - a)) ^ (1 << (n - 1 - b))
      out[i] = state[j]
    }
  }
  return out
}

export function simulate(n: number, ops: Op[]): SimResult {
  const N = 1 << n
  let state: Complex[] = new Array(N).fill(null).map((_, i) => (i === 0 ? c(1) : c(0)))

  for (const op of ops) {
    if (op.kind === 'single') state = applySingle(state, n, op.gate, op.qubit)
    else if (op.kind === 'cnot') state = applyCNOT(state, n, op.control, op.target)
    else if (op.kind === 'swap') state = applySWAP(state, n, op.a, op.b)
  }

  const distribution = state
    .map((amp, i) => ({ state: i.toString(2).padStart(n, '0'), prob: cabs2(amp) }))
    .filter((d) => d.prob > 1e-9)
    .sort((a, b) => b.prob - a.prob)

  const perQubit = Array.from({ length: n }, (_, q) => {
    let p1 = 0
    for (let i = 0; i < N; i++) {
      if (bit(i, n, q) === 1) p1 += cabs2(state[i])
    }
    return { qubit: q, p0: 1 - p1, p1 }
  })

  return {
    n,
    amplitudes: state,
    distribution,
    perQubit,
    topState: distribution[0]?.state ?? '0'.repeat(n),
  }
}

export function formatComplex(a: Complex) {
  const r = Math.abs(a.re) < 1e-9 ? 0 : a.re
  const im = Math.abs(a.im) < 1e-9 ? 0 : a.im
  if (im === 0) return r.toFixed(3)
  if (r === 0) return `${im.toFixed(3)}i`
  return `${r.toFixed(3)}${im >= 0 ? '+' : '-'}${Math.abs(im).toFixed(3)}i`
}
