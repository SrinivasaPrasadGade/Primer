# UI/UX Design Document

## **Primer — AI-Powered Digital Public Safety Intelligence Platform**

| Field | Detail |
|---|---|
| **Document Version** | 2.0 — Hackathon MVP |
| **Date** | 5 July 2026 |
| **Design Philosophy** | Apple-inspired — Slim · Sleek · Purposeful · Premium |
| **Companion Documents** | [PRD](product_requirements_document.md) · [TRD](technical_requirements_document.md) · [App Flow](application_flow_document.md) |

---

## 1. Design Philosophy

> *"Clarity is the ultimate sophistication."*

Primer handles life-critical data — scam alerts, counterfeit detections, fraud networks. Every interaction must be **instant, clear, and effortless**. Nothing is decorative unless it communicates meaning.

### Core Principles

```
○ CLARITY FIRST       — Information is the hero. Chrome is the servant.
○ PURPOSEFUL MOTION   — Every animation reveals, guides, or confirms. Never decorates.
○ QUIET LUXURY        — Premium without loudness.
○ DEPTH WITHOUT NOISE — Hierarchy through weight and space, not borders and boxes.
○ BREATHING ROOM      — Generous whitespace. Every element has room to breathe.
```

### MVP Design Priority

**Ship beautiful, not pixel-perfect.** Focus effort on these high-impact screens:

1. 🚨 Scam Sentinel Live Monitor (the "wow" screen for judges)
2. 📊 Home Dashboard (first impression)
3. 🕸️ Fraud Graph Explorer (technical impressiveness)
4. 📱 Citizen App — QR Scanner + Call Screening (innovation showcase)
5. 🗺️ Geo Intel Crime Map (visual impact)

---

## 2. Design Language

### Surface Hierarchy (Dark Mode Only for MVP)

```
Layer 0 — Page Background      #0A0A0F  (near-black with cool tint)
Layer 1 — Primary Card         #111118  (elevated surface)
Layer 2 — Secondary Card       #16161F  (deeper in-card content)
Layer 3 — Input / Control      #1C1C27  (interactive fields)
Layer 4 — Hover State          #222233  (hover elevation)
```

### Alert Colour System

```
🔴 RED     — #EF4444  — Active threat, immediate action required
🟠 AMBER   — #F59E0B  — Monitoring, possible threat
🟡 YELLOW  — #EAB308  — Low confidence, logged
🟢 GREEN   — #22C55E  — Safe, genuine, clean
🔵 ACCENT  — #3B82F6  — Interactive elements, links, focus
```

---

## 3. Design Tokens (CSS Variables)

```css
:root {
    /* ─── Surfaces ─── */
    --color-bg-primary:   #0A0A0F;
    --color-layer-1:      #111118;
    --color-layer-2:      #16161F;
    --color-layer-3:      #1C1C27;
    --color-layer-4:      #222233;

    /* ─── Text ─── */
    --color-text-primary:    #F5F5F7;
    --color-text-secondary:  #AEAEB2;
    --color-text-tertiary:   #636366;

    /* ─── Borders ─── */
    --color-border-subtle:   rgba(255, 255, 255, 0.06);
    --color-border-default:  rgba(255, 255, 255, 0.10);

    /* ─── Accent ─── */
    --accent-500: #3B82F6;
    --accent-600: #2563EB;

    /* ─── Alerts ─── */
    --color-red:       #EF4444;
    --color-red-bg:    rgba(239, 68, 68, 0.08);
    --color-red-border:rgba(239, 68, 68, 0.20);
    --color-amber:     #F59E0B;
    --color-amber-bg:  rgba(245, 158, 11, 0.08);
    --color-green:     #22C55E;
    --color-green-bg:  rgba(34, 197, 94, 0.08);

    /* ─── Typography ─── */
    --font-display: "Inter", -apple-system, sans-serif;
    --font-mono:    "JetBrains Mono", monospace;

    /* ─── Spacing ─── */
    --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
    --space-6: 24px; --space-8: 32px;

    /* ─── Radius ─── */
    --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;
    --radius-xl: 16px; --radius-full: 9999px;

    /* ─── Shadows ─── */
    --shadow-sm:  0 2px 8px rgba(0,0,0,0.12);
    --shadow-lg:  0 8px 32px rgba(0,0,0,0.20);
    --shadow-red: 0 4px 24px rgba(239,68,68,0.25);

    /* ─── Easing ─── */
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1.0);
    --ease-smooth: cubic-bezier(0.23, 1.0, 0.32, 1.0);

    /* ─── Layout ─── */
    --nav-height: 56px;
    --sidebar-width: 240px;
    --sidebar-collapsed: 64px;
}
```

---

## 4. Typography

```
Display / Page Title    — Inter 700, 28px, -0.02em tracking
Section Header         — Inter 600, 20px
Card Title             — Inter 600, 16px
Body                   — Inter 400, 14px, line-height 1.5
Small / Label          — Inter 500, 12px, 0.04em tracking
Mono / Data            — JetBrains Mono 400, 13px
```

Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 5. Component Specifications (MVP Set)

### 5.1 Card

```css
.card {
    background: var(--color-layer-1);
    border: 1px solid var(--color-border-subtle);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), var(--shadow-sm);
    transition: transform 200ms var(--ease-smooth), box-shadow 200ms;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
.card.red {
    background: var(--color-red-bg);
    border-color: var(--color-red-border);
    animation: redPulse 4s ease-in-out infinite;
}
@keyframes redPulse {
    0%, 100% { box-shadow: var(--shadow-sm), 0 0 0 0 rgba(239,68,68,0); }
    50%       { box-shadow: var(--shadow-sm), 0 0 24px -4px rgba(239,68,68,0.2); }
}
```

### 5.2 Alert Badge

```css
.badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 8px; border-radius: var(--radius-full);
    font: 600 11px var(--font-display);
    text-transform: uppercase;
}
.badge.red { background: var(--color-red-bg); color: #FCA5A5; }
.badge.red::before {
    content: ''; width: 5px; height: 5px; border-radius: 50%;
    background: var(--color-red); animation: pulse 2s infinite;
}
```

### 5.3 Confidence Bar

```css
.confidence-bar {
    height: 6px; border-radius: 3px;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
}
.confidence-bar .fill {
    height: 100%; border-radius: 3px;
    background: linear-gradient(90deg, var(--accent-500), var(--accent-600));
    transition: width 800ms var(--ease-smooth);
}
```

### 5.4 Glassmorphism Navbar

```css
.navbar {
    position: fixed; top: 0; left: 0; right: 0;
    height: var(--nav-height);
    backdrop-filter: blur(24px) saturate(1.8) brightness(0.92);
    background: rgba(10, 10, 15, 0.85);
    border-bottom: 1px solid var(--color-border-subtle);
    z-index: 100;
}
```

---

## 6. Key Screen Designs

### 6.1 Scam Sentinel — Live Monitor (Hero Screen)

The most important screen for the demo. RED alert cards should feel urgent and alive.

**Key visual elements:**
- RED cards pulse with ambient glow every 4 seconds
- Duration timer ticks up in monospace font (no layout shift)
- New sessions animate in from top with 800ms red glow burst
- Confidence bars fill with staggered animation on card appear
- Alert dot has 2s breathing pulse

**Explainable AI section:**
- Each signal gets its own bar (0–100%)
- Below each bar: one-line plain-English explanation
- Overall confidence shown as large radial gauge

### 6.2 Fraud Graph Explorer

**Key visual elements:**
- Full-width interactive canvas (dark background, bright nodes)
- Node colours by type: 📱 blue, 💰 green, 👤 orange, 🖥️ purple
- Edge thickness proportional to transaction amount
- Hover on node → glow + detail panel slides in from right
- AI Copilot chat bar pinned to bottom

### 6.3 Geo Intel Crime Map

**Key visual elements:**
- Full-bleed Mapbox dark style
- Heatmap layer with red-orange-yellow gradient
- Prediction zones: dashed circle outlines with pulsing fill
- Incident pins colour-coded by crime type
- Time slider at bottom for temporal filtering

### 6.4 Citizen App — QR Scanner

**Key visual elements:**
- Camera viewfinder with animated scanning line
- QR frame guides (corner brackets)
- Result card slides up from bottom with verdict
- 🚫 DANGEROUS: red gradient background, shake animation
- ✅ SAFE: green checkmark with scale-in animation

### 6.5 Citizen App — Call Screening Overlay

**Key visual elements:**
- Translucent overlay on top of incoming call screen
- Risk indicator: large coloured bar (green → yellow → red)
- "Checking..." state with animated spinner
- Result appears with slide-up animation
- Two buttons: Reject (red, prominent) and Answer Anyway (grey, smaller)

### 6.6 Citizen App — Panic Button

**Key visual elements:**
- Hidden by default — activated by gesture or app shortcut
- NO visible UI to the scammer — screen stays normal
- After call: notification slides down with shield icon
- "Primer Protected You" — reassuring green card

---

## 7. Animation Specifications (MVP Subset)

Only implement animations that directly impact demo impressiveness:

| Animation | Duration | Easing | Where |
|---|---|---|---|
| RED card glow pulse | 4s infinite | ease-in-out | Scam Sentinel cards |
| Alert dot breathing | 2s infinite | ease-in-out | Badge dots |
| New card slide-in | 400ms | ease-smooth | Live monitor feed |
| Confidence bar fill | 800ms (staggered 60ms) | ease-smooth | Session detail |
| Drawer slide-in | 400ms | ease-smooth | Right panel |
| Count-up (numbers) | 1200ms | ease-out | Dashboard KPIs |
| Card hover lift | 200ms | ease-smooth | All hoverable cards |
| Map pin drop | 300ms | ease-spring | Geo Intel pins |
| QR scan line | 2s infinite | linear | QR scanner |
| Verdict card slide-up | 400ms | ease-spring | Scan results |

---

## 8. Mobile App Screens (Citizen — Sumanth)

### Screen List (8 screens total)

1. **Home** — Feature grid: Scan Note, QR Scanner, Check Number, Chat, Learn
2. **Note Scanner** — Camera → Quality check → Result
3. **Scan Result** — Verdict card + feature breakdown
4. **QR Scanner** — Camera → Decode → Risk result
5. **QR Result** — Risk verdict + details
6. **Number Check** — Input → Reputation result
7. **AI Chat** — Conversational interface
8. **Panic SOS** — Activation confirmation + post-call report

### Mobile Design Rules

```
• Bottom tab navigation (4 tabs: Home, Scan, Chat, Profile)
• Cards have 16px margin, 12px radius
• Text: 16px body, 20px titles (legibility on phone)
• Buttons: 48px min touch target
• Scan results: full-screen overlay from bottom (sheet)
• Colours and tokens: same as web (shared CSS variables)
```

---

## 9. Glassmorphism & Visual Effects

Use sparingly for premium feel on:

| Element | Effect |
|---|---|
| Navbar | `backdrop-filter: blur(24px) saturate(1.8)` |
| Modal overlay | `backdrop-filter: blur(8px)` + `rgba(0,0,0,0.5)` |
| Call screening overlay | `backdrop-filter: blur(16px)` + gradient tint |
| Toast notifications | `backdrop-filter: blur(12px)` + `rgba(layer-1, 0.9)` |

**Do NOT use glassmorphism on**: cards, sidebars, or data tables — it hurts readability.

---

## 10. Accessibility (MVP Minimum)

- [ ] All interactive elements have `aria-label`
- [ ] Colour is never the only indicator (always text + icon alongside)
- [ ] Focus styles visible (2px solid accent-400, 2px offset)
- [ ] Alert levels use text labels, not just dots
- [ ] Minimum contrast: 4.5:1 for body text
- [ ] `prefers-reduced-motion`: disable all animations
