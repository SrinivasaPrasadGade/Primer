"use client";
import { CSSProperties, useEffect, useRef, useState } from "react";
import L, { LatLngBounds } from "leaflet";
import "leaflet/dist/leaflet.css";
import { GeoIncident, HeatmapCell, HotspotPrediction } from "@/lib/api";
import { HeatmapLayer } from "./HeatmapLayer";
import styles from "@/styles/geo.module.css";

const MUMBAI_CENTER: [number, number] = [19.07, 72.88];
const DEFAULT_ZOOM = 11;

function toBoundsString(bounds: LatLngBounds): string {
    return [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()].map((n) => n.toFixed(5)).join(",");
}

export function CrimeMap({
    heatmap,
    incidents,
    predictions,
    onBoundsChange,
    onIncidentClick,
    style,
    interactive = true,
    zoom = 11,
}: {
    heatmap: HeatmapCell[];
    incidents: GeoIncident[];
    predictions: HotspotPrediction[];
    onBoundsChange: (bounds: string) => void;
    onIncidentClick: (incident: GeoIncident) => void;
    style?: CSSProperties;
    interactive?: boolean;
    zoom?: number;
}) {
    const containerRef = useRef<HTMLDivElement>(null);
    const mapRef = useRef<L.Map | null>(null);
    const [map, setMap] = useState<L.Map | null>(null);
    const incidentsLayerRef = useRef<L.LayerGroup | null>(null);
    const predictionsLayerRef = useRef<L.LayerGroup | null>(null);

    useEffect(() => {
        if (!containerRef.current || mapRef.current) return;

        const m = L.map(containerRef.current).setView(MUMBAI_CENTER, zoom);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
        }).addTo(m);

        mapRef.current = m;

        // Create layer groups for incidents and predictions
        incidentsLayerRef.current = L.layerGroup().addTo(m);
        predictionsLayerRef.current = L.layerGroup().addTo(m);

        m.on("moveend", () => onBoundsChange(toBoundsString(m.getBounds())));
        onBoundsChange(toBoundsString(m.getBounds()));
        setMap(m);

        if (!interactive) m.dragging.disable();

        return () => {
            m.remove();
            mapRef.current = null;
            incidentsLayerRef.current = null;
            predictionsLayerRef.current = null;
            setMap(null);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        if (!incidentsLayerRef.current) return;
        incidentsLayerRef.current.clearLayers();

        incidents.forEach((incident) => {
            const color = {
                cyber_fraud: "#3B82F6",
                upi_fraud: "#F59E0B",
                phishing: "#A855F7",
                extortion: "#EF4444",
                counterfeit: "#22C55E",
            }[incident.crime_type] || "#EF4444";

            const marker = L.circleMarker([incident.lat, incident.lng], {
                radius: 5,
                fillColor: color,
                color: "#fff",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8,
            });

            marker.on("click", () => onIncidentClick(incident));
            marker.addTo(incidentsLayerRef.current!);
        });
    }, [incidents, onIncidentClick]);

    useEffect(() => {
        if (!predictionsLayerRef.current) return;
        predictionsLayerRef.current.clearLayers();

        predictions.forEach((p) => {
            const radius = Math.min(Math.max(p.radius_km * 10, 10), 50);
            const circle = L.circleMarker([p.lat, p.lng], {
                radius,
                fillColor: "rgba(245,158,11,0.15)",
                color: "#F59E0B",
                weight: 1.5,
                opacity: 1,
                fillOpacity: 0.15,
            });

            circle.addTo(predictionsLayerRef.current!);
        });
    }, [predictions]);

    return (
        <>
            <div ref={containerRef} className={styles.map} style={style} />
            <HeatmapLayer map={map} data={heatmap} />
        </>
    );
}
