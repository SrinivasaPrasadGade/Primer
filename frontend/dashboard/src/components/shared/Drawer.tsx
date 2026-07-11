"use client";
import { ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import styles from "./shared.module.css";

export function Drawer({ open, onClose, children }: { open: boolean; onClose: () => void; children: ReactNode }) {
    return (
        <AnimatePresence>
            {open && (
                <>
                    <motion.div
                        className={styles.drawerBackdrop}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                    />
                    <motion.div
                        className={styles.drawer}
                        initial={{ x: "100%" }}
                        animate={{ x: 0 }}
                        exit={{ x: "100%" }}
                        transition={{ duration: 0.3, ease: [0.23, 1.0, 0.32, 1.0] }}
                    >
                        {children}
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
