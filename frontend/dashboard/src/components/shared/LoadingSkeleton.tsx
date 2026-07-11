import styles from "./shared.module.css";

export function LoadingSkeleton({ height = 16, width = "100%" }: { height?: number | string; width?: number | string }) {
    return <div className={styles.skeleton} style={{ height, width }} />;
}
