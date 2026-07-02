import './Footer.css'

const GRADIO_URL = 'http://127.0.0.1:7860'

const LINKS = {
    App: [
        { label: 'MRI Analysis', href: `${GRADIO_URL}/` },
        { label: 'EEG Detection', href: `${GRADIO_URL}/` },
        { label: 'Neurology Chatbot', href: `${GRADIO_URL}/` },
        { label: 'Learn Videos', href: `${GRADIO_URL}/` },
    ],
    Resources: [
        { label: "Alzheimer's Association", href: 'https://www.alz.org', external: true },
        { label: 'Epilepsy Foundation', href: 'https://www.epilepsy.com', external: true },
        { label: 'WHO Dementia Facts', href: 'https://www.who.int/news-room/fact-sheets/detail/dementia', external: true },
        { label: 'NINDS Neurology', href: 'https://www.ninds.nih.gov', external: true },
    ],
    Tech: [
        { label: 'TensorFlow', href: 'https://tensorflow.org', external: true },
        { label: 'FAISS', href: 'https://faiss.ai', external: true },
        { label: 'Sentence Transformers', href: 'https://sbert.net', external: true },
        { label: 'Gradio', href: 'https://gradio.app', external: true },
    ],
}

export default function Footer() {
    return (
        <footer className="footer" role="contentinfo">
            <div className="container">
                <div className="footer__top">
                    {/* Brand */}
                    <div className="footer__brand">
                        <div className="footer__logo">
                            <span aria-hidden="true">🛡️</span>
                            <span className="footer__logo-text font-display">Neuro Shield</span>
                        </div>
                        <p className="footer__tagline">
                            AI-powered brain health diagnostics for Alzheimer's detection,
                            EEG seizure analysis, and neurology Q&A.
                        </p>
                        <a
                            href={GRADIO_URL}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn btn-primary footer__cta"
                            id="footer-launch-btn"
                        >
                            🚀 Launch App
                        </a>
                    </div>

                    {/* Links */}
                    {Object.entries(LINKS).map(([category, links]) => (
                        <nav key={category} aria-label={`${category} links`}>
                            <h3 className="footer__col-title">{category}</h3>
                            <ul className="footer__col-links">
                                {links.map(link => (
                                    <li key={link.label}>
                                        <a
                                            href={link.href}
                                            target={link.external ? '_blank' : undefined}
                                            rel={link.external ? 'noopener noreferrer' : undefined}
                                            className="footer__link"
                                        >
                                            {link.label}
                                            {link.external && <span aria-hidden="true"> ↗</span>}
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </nav>
                    ))}
                </div>

                {/* Divider */}
                <div className="footer__divider" role="separator" />

                {/* Bottom */}
                <div className="footer__bottom">
                    <p className="footer__copyright">
                        © 2026 Neuro Shield · Built with ❤️ using TensorFlow, FAISS &amp; React
                    </p>
                    <p className="footer__disclaimer">
                        ⚠️ For educational &amp; research purposes only. Not a substitute for professional medical advice.
                    </p>
                </div>
            </div>
        </footer>
    )
}
