export function ConfidenceBar({ value }: { value: number }) {
    return (
        <div className="confidence-bar">
            <div className="fill" style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
        </div>
    );
}
