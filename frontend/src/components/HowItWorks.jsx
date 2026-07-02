import { useRef, useEffect } from 'react'
import './HowItWorks.css'

const STEPS = [
    {
        num: '01',
        icon: '📤',
        title: 'Upload Your Data',
        desc: 'Upload a brain MRI image, an EEG graph image, or simply type a neurology question into the chatbot.',
        color: 'var(--color-accent-indigo)',
    },
    {
        num: '02',
        icon: '🤖',
        title: 'AI Analysis',
        desc: 'Our deep learning models process your input — CNN for MRI, signal extraction for EEG, and FAISS semantic search for Q&A.',
        color: 'var(--color-accent-violet)',
    },
    {
        num: '03',
        icon: '📊',
        title: 'Confidence Scoring',
        desc: 'Every prediction comes with a real confidence score, not a hardcoded value — giving you transparent, trustworthy results.',
        color: 'var(--color-accent-cyan)',
    },
    {
        num: '04',
        icon: '📄',
        title: 'Get Your Report',
        desc: 'Download a branded PDF report with your diagnosis, confidence score, precautionary measures, and medication suggestions.',
        color: 'var(--color-accent-emerald)',
    },
]

export default function HowItWorks() {
    const sectionRef = useRef(null)
    const itemsRef = useRef([])

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) entry.target.classList.add('hiw-step--visible')
                })
            },
            { threshold: 0.2 }
        )
        itemsRef.current.forEach(el => el && observer.observe(el))
        return () => observer.disconnect()
    }, [])

    return (
        <section className="hiw section" id="how-it-works" aria-labelledby="hiw-heading">
            <div className="container">
                <div className="hiw__head text-center">
                    <div className="section-label"><span>🔄</span> Process</div>
                    <h2 id="hiw-heading" className="hiw__heading font-display gradient-text">
                        How Neuro Shield Works
                    </h2>
                    <p className="hiw__sub">
                        From data upload to diagnosis in seconds — here's how our AI pipeline works.
                    </p>
                </div>

                <div className="hiw__steps">
                    {STEPS.map((step, i) => (
                        <div
                            key={step.num}
                            className="hiw-step"
                            ref={el => (itemsRef.current[i] = el)}
                            style={{ '--step-color': step.color, '--stagger': `${i * 0.15}s` }}
                        >
                            {/* Connector line */}
                            {i < STEPS.length - 1 && <div className="hiw-step__connector" aria-hidden="true" />}

                            {/* Number bubble */}
                            <div className="hiw-step__num glass-card" aria-hidden="true">
                                <span className="hiw-step__num-text">{step.num}</span>
                            </div>

                            {/* Icon */}
                            <div className="hiw-step__icon" aria-hidden="true">{step.icon}</div>

                            {/* Content */}
                            <h3 className="hiw-step__title font-display">{step.title}</h3>
                            <p className="hiw-step__desc">{step.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}
