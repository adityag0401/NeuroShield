import { useRef, useEffect } from 'react'
import './Features.css'

const GRADIO_URL = 'http://127.0.0.1:7860'

const FEATURES = [
    {
        id: 'mri',
        icon: '🧠',
        color: '--color-accent-indigo',
        gradient: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
        tag: 'Computer Vision',
        title: "Alzheimer's MRI Detection",
        description:
            "Upload a brain MRI scan and receive AI-powered classification into Alzheimer's stages — No Impairment, Very Mild, Mild, or Moderate — with real confidence scores and detailed PDF reports.",
        bullets: [
            '4-class CNN classifier trained on MRI scans',
            'Instant confidence scoring per prediction',
            'Downloadable branded PDF diagnosis report',
            'Personalized care & medication guidance',
        ],
    },
    {
        id: 'eeg',
        icon: '⚡',
        color: '--color-accent-cyan',
        gradient: 'linear-gradient(135deg, #0ea5e9, #22d3ee)',
        tag: 'Signal Processing',
        title: 'EEG Seizure Detection',
        description:
            "Upload an EEG graph image to detect epileptic seizure activity. Our signal-processing pipeline extracts features from EEG waveforms and classifies them as SEIZURE or NON-SEIZURE with confidence.",
        bullets: [
            'EEG image → signal extraction via edge detection',
            'Dense neural network for binary classification',
            'Real-time confidence-scored predictions',
            'Seizure management & medication advice included',
        ],
    },
    {
        id: 'rag',
        icon: '📚',
        color: '--color-accent-emerald',
        gradient: 'linear-gradient(135deg, #10b981, #34d399)',
        tag: 'RAG · FAISS · NLP',
        title: 'Neurology Q&A Chatbot',
        description:
            "Ask any question about EEG, Alzheimer's disease, epilepsy, dementia, or brain health. Our FAISS-powered RAG chatbot retrieves the most semantically relevant answers from a curated database of 50+ expert Q&As.",
        bullets: [
            'FAISS vector search for fast retrieval',
            'Sentence Transformers for semantic understanding',
            '50+ curated neurology Q&A pairs',
            'Multi-turn conversation with history',
        ],
    },
]

function FeatureCard({ feature, index }) {
    const cardRef = useRef(null)

    useEffect(() => {
        const card = cardRef.current
        if (!card) return
        const observer = new IntersectionObserver(
            ([entry]) => { if (entry.isIntersecting) card.classList.add('animate-in') },
            { threshold: 0.15 }
        )
        observer.observe(card)
        return () => observer.disconnect()
    }, [])

    return (
        <article
            ref={cardRef}
            className={`feature-card glass-card animate-in-delay-${index + 1}`}
            id={`feature-${feature.id}`}
        >
            {/* Top accent bar */}
            <div className="feature-card__bar" style={{ background: feature.gradient }} />

            {/* Tag */}
            <div className="feature-card__tag" style={{ background: 'rgba(255,255,255,0.07)', border: '1px solid rgba(255,255,255,0.12)' }}>
                <span style={{ backgroundImage: feature.gradient, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    {feature.tag}
                </span>
            </div>

            {/* Icon */}
            <div className="feature-card__icon" style={{ background: `${feature.gradient}20` }}>
                <span aria-hidden="true">{feature.icon}</span>
            </div>

            {/* Content */}
            <h3 className="feature-card__title font-display">{feature.title}</h3>
            <p className="feature-card__desc">{feature.description}</p>

            {/* Bullets */}
            <ul className="feature-card__bullets">
                {feature.bullets.map(b => (
                    <li key={b} className="feature-card__bullet">
                        <span className="feature-card__check" style={{ background: feature.gradient }} aria-hidden="true">✓</span>
                        {b}
                    </li>
                ))}
            </ul>

            {/* CTA */}
            <a
                href={GRADIO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="feature-card__cta btn"
                style={{ background: feature.gradient }}
                id={`feature-cta-${feature.id}`}
            >
                Try Now →
            </a>
        </article>
    )
}

export default function Features() {
    const headRef = useRef(null)

    useEffect(() => {
        const el = headRef.current
        if (!el) return
        const observer = new IntersectionObserver(
            ([entry]) => { if (entry.isIntersecting) el.classList.add('animate-in') },
            { threshold: 0.2 }
        )
        observer.observe(el)
        return () => observer.disconnect()
    }, [])

    return (
        <section className="features section" id="features" aria-labelledby="features-heading">
            <div className="container">
                <div className="features__head text-center" ref={headRef}>
                    <div className="section-label">
                        <span>⚡</span> Core Capabilities
                    </div>
                    <h2 id="features-heading" className="features__heading font-display gradient-text">
                        Three Powerful Diagnostic Tools
                    </h2>
                    <p className="features__sub">
                        Neuro Shield combines computer vision, signal processing, and natural language AI
                        into a unified platform for brain health diagnostics.
                    </p>
                </div>

                <div className="features__grid">
                    {FEATURES.map((feat, i) => (
                        <FeatureCard key={feat.id} feature={feat} index={i} />
                    ))}
                </div>
            </div>
        </section>
    )
}
