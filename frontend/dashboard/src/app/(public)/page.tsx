"use client";
import Link from "next/link";
import { ShieldAlert, PhoneCall, Landmark, Share2, Map, MessageSquareText, FileSearch, ArrowRight } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import styles from "@/styles/landing.module.css";

const MODULES = [
    {
        icon: PhoneCall,
        name: "Scam Sentinel",
        blurb: "Scores live calls for scam signals and raises red, amber or yellow alerts as a session unfolds.",
    },
    {
        icon: Landmark,
        name: "Note Verify",
        blurb: "Checks currency notes against known counterfeit markers and returns a verdict with confidence.",
    },
    {
        icon: Share2,
        name: "Fraud Graph",
        blurb: "Links phones, accounts, devices and UPI handles into clusters, and traces money between them.",
    },
    {
        icon: Map,
        name: "Geo Intel",
        blurb: "Maps incident density and forecasts hotspots so patrols can be placed before crimes cluster.",
    },
    {
        icon: MessageSquareText,
        name: "AI Copilot",
        blurb: "Answers plain-language questions by querying the platform directly and showing its working.",
    },
    {
        icon: FileSearch,
        name: "Case Summarizer",
        blurb: "Pulls an entity's history into a briefing an officer can read before picking up the case.",
    },
];

export default function LandingPage() {
    const { user, loading } = useAuth();

    // While the session resolves, useAuth may be about to bounce a signed-in
    // officer to /dashboard — don't flash marketing copy at them first.
    if (loading || user) return null;

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <div className={styles.brand}>
                    <ShieldAlert size={22} color="var(--accent-500)" />
                    <span>Primer</span>
                </div>
                <Link href="/login" className={styles.headerCta}>
                    Sign in
                </Link>
            </header>

            <main>
                <section className={styles.hero}>
                    <p className={styles.eyebrow}>Digital Public Safety Intelligence</p>
                    <h1 className={styles.heroTitle}>
                        Six investigative tools,
                        <br />
                        one operating picture.
                    </h1>
                    <p className={styles.heroLede}>
                        Primer brings call analysis, counterfeit detection, fraud-network tracing and geospatial
                        forecasting into a single console — so an officer can move from a single phone number to the
                        cluster behind it without leaving the platform.
                    </p>
                    <div className={styles.heroActions}>
                        <Link href="/login" className={styles.primaryCta}>
                            Sign in to console
                            <ArrowRight size={16} />
                        </Link>
                        <a href="#modules" className={styles.secondaryCta}>
                            See the modules
                        </a>
                    </div>
                </section>

                <section id="modules" className={styles.modules}>
                    <h2 className={styles.sectionTitle}>Platform modules</h2>
                    <div className={styles.moduleGrid}>
                        {MODULES.map(({ icon: Icon, name, blurb }) => (
                            <article key={name} className={styles.moduleCard}>
                                <Icon size={18} className={styles.moduleIcon} />
                                <h3 className={styles.moduleName}>{name}</h3>
                                <p className={styles.moduleBlurb}>{blurb}</p>
                            </article>
                        ))}
                    </div>
                </section>
            </main>

            <footer className={styles.footer}>
                <span>Primer — Digital Public Safety Intelligence Platform</span>
                <Link href="/login" className={styles.footerLink}>
                    Sign in
                </Link>
            </footer>
        </div>
    );
}
