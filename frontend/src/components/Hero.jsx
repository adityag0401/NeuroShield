import { useEffect, useRef } from 'react'
import './Hero.css'

const GRADIO_URL = 'http://127.0.0.1:7860'

const PARTICLES = Array.from({ length: 18 }, (_, i) => ({
    id: i,
    size: 2 + Math.random() * 5,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: 6 + Math.random() * 10,
    delay: Math.random() * 5,
}))

export default function Hero() {
    const heroRef = useRef(null)

    useEffect(() => {
        // Parallax effect on mouse move
        const hero = heroRef.current
        if (!hero) return

        const onMove = (e) => {
            const { clientX, clientY } = e
            const { innerWidth, innerHeight } = window
            const x = (clientX / innerWidth - 0.5) * 20
            const y = (clientY / innerHeight - 0.5) * 20

            hero.querySelectorAll('.hero__orb').forEach((orb, i) => {
                const factor = (i + 1) * 0.3
                orb.style.transform = `translate(${x * factor}px, ${y * factor}px)`
            })
        }

        window.addEventListener('mousemove', onMove, { passive: true })
        return () => window.removeEventListener('mousemove', onMove)
    }, [])

    return (
        <section className="hero" ref={heroRef} aria-labelledby="hero-heading">
            {/* Ambient orbs */}
            <div className="hero__orb hero__orb--1" aria-hidden="true" />
            <div className="hero__orb hero__orb--2" aria-hidden="true" />
            <div className="hero__orb hero__orb--3" aria-hidden="true" />

            {/* Floating particles */}
            <div className="hero__particles" aria-hidden="true">
                {PARTICLES.map(p => (
                    <span
                        key={p.id}
                        className="hero__particle"
                        style={{
                            width: p.size, height: p.size,
                            left: `${p.x}%`, top: `${p.y}%`,
                            animationDuration: `${p.duration}s`,
                            animationDelay: `${p.delay}s`,
                        }}
                    />
                ))}
            </div>

            <div className="container hero__content">
                {/* Badge */}
                <div className="hero__badge animate-in">
                    <span className="hero__badge-dot" aria-hidden="true" />
                    AI-Powered Neurology Diagnostics
                </div>

                {/* Heading */}
                <h1 id="hero-heading" className="hero__heading font-display animate-in animate-in-delay-1">
                    Protecting Minds with{' '}
                    <span className="gradient-text">Advanced AI</span>
                </h1>

                {/* Sub */}
                <p className="hero__sub animate-in animate-in-delay-2">
                    Neuro Shield harnesses deep learning to detect <strong>Alzheimer's stages</strong> from MRI scans,
                    predict <strong>epileptic seizures</strong> from EEG signals, and answer
                    <strong> neurology questions</strong> using a FAISS-powered RAG chatbot.
                </p>

                {/* CTA Buttons */}
                <div className="hero__actions animate-in animate-in-delay-3">
                    <a
                        id="hero-launch-btn"
                        href={GRADIO_URL}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary btn-lg"
                    >
                        🚀 Launch Diagnostic App
                    </a>
                    <a href="#how-it-works" className="btn btn-outline btn-lg">
                        See How It Works ↓
                    </a>
                </div>

                {/* Trust badges */}
                <div className="hero__trust animate-in animate-in-delay-4">
                    {[
                        { icon: '🧠', label: 'MRI Analysis' },
                        { icon: '⚡', label: 'EEG Detection' },
                        { icon: '📚', label: 'RAG Chatbot' },
                        { icon: '📄', label: 'PDF Reports' },
                    ].map(({ icon, label }) => (
                        <div key={label} className="hero__trust-badge">
                            <span aria-hidden="true">{icon}</span>
                            <span>{label}</span>
                        </div>
                    ))}
                </div>

                {/* Visual card */}
                <div className="hero__visual animate-in animate-in-delay-5" aria-hidden="true">
                    <div className="hero__brain-card glass-card">
                        <div className="hero__brain-icon">🧠</div>
                        <div className="hero__brain-lines">
                            {[85, 62, 91, 48, 76].map((w, i) => (
                                <div key={i} className="hero__brain-line" style={{ '--w': `${w}%`, '--delay': `${i * 0.2}s` }} />
                            ))}
                        </div>
                        <div className="hero__brain-label">EEG Signal Analysis</div>
                        <div className="hero__brain-status">
                            <span className="hero__status-dot" />
                            Analyzing...
                        </div>
                    </div>
                </div>
            </div>

            {/* Scroll indicator */}
            <div className="hero__scroll" aria-label="Scroll down">
                <div className="hero__scroll-mouse" />
                <span>Scroll to explore</span>
            </div>
        </section>
    )
}
