import { useRef, useEffect, useState } from 'react'
import './Stats.css'

const STATS = [
    {
        value: 98,
        suffix: '%',
        label: 'MRI Dataset Accuracy',
        desc: 'Alzheimer\'s stage classification',
        icon: '🧠',
        color: 'var(--color-accent-indigo)',
    },
    {
        value: 97,
        suffix: '%',
        label: 'EEG Detection Accuracy',
        desc: 'Seizure vs. non-seizure prediction',
        icon: '⚡',
        color: 'var(--color-accent-cyan)',
    },
    {
        value: 50,
        suffix: '+',
        label: 'Neurology Q&A Pairs',
        desc: 'Expert-curated knowledge base',
        icon: '📚',
        color: 'var(--color-accent-emerald)',
    },
    {
        value: 4,
        suffix: '',
        label: 'Alzheimer\'s Stages',
        desc: 'Classified from MRI scans',
        icon: '🔬',
        color: 'var(--color-accent-violet)',
    },
]

function AnimatedCounter({ value, suffix, active }) {
    const [display, setDisplay] = useState(0)

    useEffect(() => {
        if (!active) return
        const duration = 2000
        const steps = 60
        const increment = value / steps
        let current = 0
        const timer = setInterval(() => {
            current += increment
            if (current >= value) {
                setDisplay(value)
                clearInterval(timer)
            } else {
                setDisplay(Math.floor(current))
            }
        }, duration / steps)
        return () => clearInterval(timer)
    }, [active, value])

    return (
        <span className="stat-card__num">
            {display}
            <span className="stat-card__suffix">{suffix}</span>
        </span>
    )
}

export default function Stats() {
    const [visible, setVisible] = useState(false)
    const sectionRef = useRef(null)

    useEffect(() => {
        const el = sectionRef.current
        if (!el) return
        const observer = new IntersectionObserver(
            ([entry]) => { if (entry.isIntersecting) setVisible(true) },
            { threshold: 0.3 }
        )
        observer.observe(el)
        return () => observer.disconnect()
    }, [])

    return (
        <section className="stats section" id="stats" ref={sectionRef} aria-labelledby="stats-heading">
            <div className="container">
                <div className="stats__head text-center">
                    <div className="section-label"><span>📊</span> Performance</div>
                    <h2 id="stats-heading" className="stats__heading font-display gradient-text">
                        Model Performance at a Glance
                    </h2>
                </div>

                <div className="stats__grid">
                    {STATS.map((stat, i) => (
                        <article
                            key={stat.label}
                            className={`stat-card glass-card${visible ? ' stat-card--visible' : ''}`}
                            style={{ '--stat-color': stat.color, '--stagger': `${i * 0.1}s` }}
                        >
                            <div className="stat-card__icon" aria-hidden="true">{stat.icon}</div>
                            <AnimatedCounter value={stat.value} suffix={stat.suffix} active={visible} />
                            <div className="stat-card__label">{stat.label}</div>
                            <div className="stat-card__desc">{stat.desc}</div>
                            <div className="stat-card__bar">
                                <div
                                    className="stat-card__bar-fill"
                                    style={{
                                        width: visible ? (stat.suffix === '%' ? `${stat.value}%` : '80%') : '0%',
                                        background: `linear-gradient(90deg, ${stat.color}, white)`,
                                        transitionDelay: `${i * 0.1 + 0.5}s`,
                                    }}
                                />
                            </div>
                        </article>
                    ))}
                </div>
            </div>
        </section>
    )
}
