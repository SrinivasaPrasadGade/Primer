type Level = "RED" | "AMBER" | "YELLOW" | "GREEN";

export function Badge({ level, label }: { level: Level; label?: string }) {
    return (
        <span className={`badge ${level.toLowerCase()}`}>
            <span className="dot" />
            {label ?? level}
        </span>
    );
}
