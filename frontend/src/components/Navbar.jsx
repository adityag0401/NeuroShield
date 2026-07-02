import { useState, useEffect } from 'react'
import './Navbar.css'

const GRADIO_URL = 'http://127.0.0.1:7860'

export default function Navbar() {
    const [scrolled, setScrolled] = useState(false)
    const [menuOpen, setMenuOpen] = useState(false)

    useEffect(() => {
        const onScroll = () => setScrolled(window.scrollY > 20)
        window.addEventListener('scroll', onScroll, { passive: true })
        return () => window.removeEventListener('scroll', onScroll)
    }, [])

    const navLinks = [
        { label: 'Features', href: '#features' },
        { label: 'How It Works', href: '#how-it-works' },
        { label: 'Stats', href: '#stats' },
        { label: 'About', href: '#about' },
    ]

    return (
        <header className={`navbar${scrolled ? ' navbar--scrolled' : ''}`} role="banner">
            <div className="container navbar__inner">
                {/* Logo */}
                <a href="#" className="navbar__logo" aria-label="Neuro Shield home">
                    <span className="navbar__logo-icon" aria-hidden="true">🛡️</span>
                    <span className="navbar__logo-text font-display">Neuro Shield</span>
                </a>

                {/* Desktop Nav */}
                <nav className="navbar__links" aria-label="Primary navigation">
                    {navLinks.map(link => (
                        <a key={link.href} href={link.href} className="navbar__link">
                            {link.label}
                        </a>
                    ))}
                </nav>

                {/* CTA */}
                <a
                    href={GRADIO_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary navbar__cta"
                    id="navbar-launch-btn"
                >
                    Launch App ↗
                </a>

                {/* Mobile hamburger */}
                <button
                    className={`navbar__hamburger${menuOpen ? ' open' : ''}`}
                    onClick={() => setMenuOpen(v => !v)}
                    aria-label={menuOpen ? 'Close menu' : 'Open menu'}
                    aria-expanded={menuOpen}
                >
                    <span /><span /><span />
                </button>
            </div>

            {/* Mobile Menu */}
            {menuOpen && (
                <nav className="navbar__mobile-menu" aria-label="Mobile navigation">
                    {navLinks.map(link => (
                        <a
                            key={link.href}
                            href={link.href}
                            className="navbar__mobile-link"
                            onClick={() => setMenuOpen(false)}
                        >
                            {link.label}
                        </a>
                    ))}
                    <a
                        href={GRADIO_URL}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary"
                        onClick={() => setMenuOpen(false)}
                    >
                        Launch App ↗
                    </a>
                </nav>
            )}
        </header>
    )
}
