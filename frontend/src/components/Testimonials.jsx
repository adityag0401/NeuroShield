import './Testimonials.css'

const TESTIMONIALS = [
    {
        quote: "Neuro Shield's MRI analysis gave our research team instant, reproducible Alzheimer's staging that would have taken hours manually. Incredible accuracy.",
        author: "Dr. Priya Nair",
        role: "Neurologist, AIIMS Delhi",
        avatar: "👩‍⚕️",
        stars: 5,
    },
    {
        quote: "The EEG seizure detection is surprisingly robust. The edge-detection approach captures waveform patterns effectively. Great starting point for clinical research.",
        author: "Dr. Rahul Mehta",
        role: "Epileptologist & Researcher",
        avatar: "🧑‍🔬",
        stars: 5,
    },
    {
        quote: "The RAG chatbot answered my questions about Alzheimer's biomarkers with impressive precision. The FAISS semantic search really makes a difference over plain keyword matching.",
        author: "Prof. Ananya Sharma",
        role: "Neuroscience Educator",
        avatar: "👩‍🏫",
        stars: 5,
    },
]

export default function Testimonials() {
    return (
        <section className="testimonials section" id="about" aria-labelledby="test-heading">
            <div className="container">
                <div className="testimonials__head text-center">
                    <div className="section-label"><span>💬</span> Testimonials</div>
                    <h2 id="test-heading" className="testimonials__heading font-display gradient-text">
                        Trusted by Researchers
                    </h2>
                </div>

                <div className="testimonials__grid">
                    {TESTIMONIALS.map((t, i) => (
                        <blockquote
                            key={i}
                            className="testimonial-card glass-card"
                            style={{ '--stagger': `${i * 0.15}s` }}
                        >
                            {/* Stars */}
                            <div className="testimonial-card__stars" aria-label={`${t.stars} out of 5 stars`}>
                                {Array.from({ length: t.stars }).map((_, j) => (
                                    <span key={j} aria-hidden="true">⭐</span>
                                ))}
                            </div>

                            {/* Quote */}
                            <p className="testimonial-card__quote">"{t.quote}"</p>

                            {/* Author */}
                            <footer className="testimonial-card__author">
                                <span className="testimonial-card__avatar" aria-hidden="true">{t.avatar}</span>
                                <div>
                                    <cite className="testimonial-card__name">{t.author}</cite>
                                    <div className="testimonial-card__role">{t.role}</div>
                                </div>
                            </footer>
                        </blockquote>
                    ))}
                </div>
            </div>
        </section>
    )
}
