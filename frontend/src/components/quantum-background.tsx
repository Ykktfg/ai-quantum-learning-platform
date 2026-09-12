export function QuantumBackground() {
  // Static, deterministic particle positions to avoid hydration mismatch.
  const particles = [
    { top: '12%', left: '18%', size: 3, delay: '0s', dur: '7s' },
    { top: '24%', left: '72%', size: 2, delay: '1.2s', dur: '9s' },
    { top: '46%', left: '38%', size: 4, delay: '0.5s', dur: '8s' },
    { top: '62%', left: '84%', size: 2, delay: '2s', dur: '11s' },
    { top: '78%', left: '22%', size: 3, delay: '0.9s', dur: '6.5s' },
    { top: '34%', left: '54%', size: 2, delay: '1.8s', dur: '10s' },
    { top: '84%', left: '62%', size: 3, delay: '0.3s', dur: '7.5s' },
    { top: '8%', left: '46%', size: 2, delay: '2.4s', dur: '9.5s' },
  ]

  return (
    <div aria-hidden className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      {/* base grid */}
      <div className="absolute inset-0 bg-grid opacity-60" />
      {/* glowing orbs */}
      <div
        className="absolute -top-24 -left-24 h-[28rem] w-[28rem] rounded-full blur-[120px]"
        style={{ background: 'radial-gradient(circle, oklch(0.75 0.15 197 / 22%), transparent 70%)', animation: 'quantum-pulse 9s ease-in-out infinite' }}
      />
      <div
        className="absolute top-1/3 -right-32 h-[32rem] w-[32rem] rounded-full blur-[130px]"
        style={{ background: 'radial-gradient(circle, oklch(0.62 0.22 300 / 20%), transparent 70%)', animation: 'quantum-pulse 11s ease-in-out infinite' }}
      />
      <div
        className="absolute bottom-0 left-1/3 h-[24rem] w-[24rem] rounded-full blur-[120px]"
        style={{ background: 'radial-gradient(circle, oklch(0.7 0.16 160 / 14%), transparent 70%)', animation: 'quantum-pulse 13s ease-in-out infinite' }}
      />
      {/* floating quantum particles */}
      {particles.map((p, i) => (
        <span
          key={i}
          className="absolute rounded-full bg-primary"
          style={{
            top: p.top,
            left: p.left,
            width: p.size,
            height: p.size,
            boxShadow: '0 0 12px 2px oklch(0.75 0.15 197 / 60%)',
            animation: `quantum-float ${p.dur} ease-in-out ${p.delay} infinite`,
          }}
        />
      ))}
    </div>
  )
}
