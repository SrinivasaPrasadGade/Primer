import Link from "next/link";
import { ShieldAlert, PhoneCall, Landmark, Share2, Map, MessageSquareText, ArrowRight } from "lucide-react";
import styles from "@/styles/landing.module.css";

const MODULES = [
    { icon: PhoneCall, title: "Scam Sentinel", body: "Real-time call scoring across five explainable AI signals with RED/AMBER/YELLOW alerts." },
    { icon: Share2, title: "Fraud Graph", body: "Trace money flow and entity networks across phones, accounts, UPI IDs, and devices." },
    { icon: Map, title: "Geo Intel", body: "Live crime heatmaps with model-predicted hotspot zones across the city." },
    { icon: Landmark, title: "Note Verify", body: "Camera-based counterfeit currency detection with per-feature explainability." },
    { icon: MessageSquareText, title: "AI Copilot", body: "Ask natural-language questions and get answers grounded in real platform data." },
    { icon: ShieldAlert, title: "Case Summarizer", body: "Turn scattered evidence into a structured, cited investigation dossier in seconds." },
];

export const metadata = {
    title: "Primer — Digital Public Safety Intelligence",
    description: "AI-powered fraud and scam intelligence for law enforcement.",
};

export default function LandingPage() {
    return (
        <div className={styles.page}>
            <header className={styles.nav}>
                <div className={styles.brand}>
                    <ShieldAlert size={20} color="var(--accent-500)" />
                    <span>Primer</span>
                </div>
                <Link href="/login" className={styles.navCta}>
                    Sign in
                </Link>
            </header>

            <section className={styles.hero}>
                <span className={styles.eyebrow}>AI-Powered Digital Public Safety</span>
                <h1 className={styles.title}>
                    Stop fraud before the money moves.
                </h1>
                <p className={styles.subtitle}>
                    Primer unifies scam-call detection, fraud-graph analysis, geospatial intelligence, and an
                    investigation copilot into one platform built for law enforcement and financial crime teams.
                </p>
                <div className={styles.heroActions}>
                    <Link href="/login" className={styles.primaryBtn}>
                        Launch dashboard <ArrowRight size={16} />
                    </Link>
                    <a href="#modules" className={styles.secondaryBtn}>
                        Explore modules
                    </a>
                </div>
                <div className={styles.stats}>
                    <div className={styles.stat}>
                        <strong>6</strong>
                        <span>intelligence modules</span>
                    </div>
                    <div className={styles.stat}>
                        <strong>5</strong>
                        <span>explainable scam signals</span>
                    </div>
                    <div className={styles.stat}>
                        <strong>&lt;1s</strong>
                        <span>real-time alerting</span>
                    </div>
                </div>
            </section>

            <section id="modules" className={styles.modules}>
                <h2 className={styles.sectionTitle}>One platform, six lenses on fraud</h2>
                <div className={styles.grid}>
                    {MODULES.map(({ icon: Icon, title, body }) => (
                        <div key={title} className={styles.card}>
                            <span className={styles.cardIcon}>
                                <Icon size={20} />
                            </span>
                            <h3 className={styles.cardTitle}>{title}</h3>
                            <p className={styles.cardBody}>{body}</p>
                        </div>
                    ))}
                </div>
            </section>

            <section className={styles.cta}>
                <h2 className={styles.ctaTitle}>Ready to see the network?</h2>
                <p className={styles.ctaBody}>Sign in to explore live intelligence across every Primer module.</p>
                <Link href="/login" className={styles.primaryBtn}>
                    Launch dashboard <ArrowRight size={16} />
                </Link>
            </section>

            <footer className={styles.footer}>
                <span>Primer — Digital Public Safety Intelligence Platform</span>
            </footer>
        </div>
    );
}
