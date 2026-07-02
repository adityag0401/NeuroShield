import './CTA.css'

const GRADIO_URL = 'http://127.0.0.1:7860'

export default function CTA() {
    return (
        <section className="cta section" aria-labelledby="cta-heading">
            <div className="container">
                <div className="cta__card glass-card">
                    {/* Orbs */}
                    <div className="cta__orb cta__orb--1" aria-hidden="true" />
                    <div className="cta__orb cta__orb--2" aria-hidden="true" />

                    <div className="cta__content">
                        <span className="cta__emoji" aria-hidden="true">🛡️</span>
                        <h2 id="cta-heading" className="cta__heading font-display">
                            Ready to Protect Brain Health?
                        </h2>
                        <p className="cta__sub">
                            Launch the Neuro Shield app and start analyzing MRI scans, EEG data,
                            and asking neurology questions — all powered by AI.
                        </p>
                        <div className="cta__actions">
                            <a
                                id="cta-launch-btn"
                                href={GRADIO_URL}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="btn btn-primary btn-lg cta__btn-main"
                            >
                                🚀 Launch Neuro Shield App
                            </a>
                            <a
                                href="#features"
                                className="btn btn-outline btn-lg"
                            >
                                Learn More ↑
                            </a>
                        </div>
                        <p className="cta__note">
                            Free · No account needed · Powered by deep learning
                        </p>
                    </div>
                </div>
            </div>
        </section>
    )
}
