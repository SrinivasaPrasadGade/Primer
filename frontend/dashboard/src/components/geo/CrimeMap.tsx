"use client";
import { CSSProperties, useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { GeoIncident, HeatmapCell, HotspotPrediction } from "@/lib/api";
import { HeatmapLayer } from "./HeatmapLayer";
import styles from "@/styles/geo.module.css";

const MUMBAI_CENTER: [number, number] = [72.88, 19.07];
const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN ?? "";

function toBoundsString(bounds: mapboxgl.LngLatBounds): string {
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
    const mapRef = useRef<mapboxgl.Map | null>(null);
    const [map, setMap] = useState<mapboxgl.Map | null>(null);

    useEffect(() => {
        if (!containerRef.current || mapRef.current) return;
        mapboxgl.accessToken = MAPBOX_TOKEN;

        const m = new mapboxgl.Map({
            container: containerRef.current,
            style: "mapbox://styles/mapbox/dark-v11",
            center: MUMBAI_CENTER,
            zoom,
            interactive,
        });
        mapRef.current = m;

        m.on("load", () => {
            m.addSource("incidents", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
            m.addLayer({
                id: "incidents-layer",
                type: "circle",
                source: "incidents",
                paint: {
                    // Colour-coded by crime type (UI/UX §6.3)
                    "circle-radius": 5,
                    "circle-color": [
                        "match", ["get", "crime_type"],
                        "cyber_fraud", "#3B82F6",
                        "upi_fraud", "#F59E0B",
                        "phishing", "#A855F7",
                        "extortion", "#EF4444",
                        "counterfeit", "#22C55E",
                        "#EF4444",
                    ],
                    "circle-stroke-width": 1,
                    "circle-stroke-color": "#fff",
                },
            });

            m.addSource("predictions", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
            m.addLayer({
                id: "predictions-layer",
                type: "circle",
                source: "predictions",
                paint: {
                    "circle-radius": ["interpolate", ["linear"], ["get", "radius_km"], 0, 10, 5, 50],
                    "circle-color": "rgba(245,158,11,0.15)",
                    "circle-stroke-width": 1.5,
                    "circle-stroke-color": "#F59E0B",
                },
            });

            m.on("click", "incidents-layer", (e) => {
                const feature = e.features?.[0];
                if (feature?.properties) onIncidentClick(feature.properties as unknown as GeoIncident);
            });

            onBoundsChange(toBoundsString(m.getBounds()!));
            setMap(m);
        });

        m.on("moveend", () => onBoundsChange(toBoundsString(m.getBounds()!)));

        return () => {
            m.remove();
            mapRef.current = null;
            setMap(null);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        if (!map || !map.getSource("incidents")) return;
        (map.getSource("incidents") as mapboxgl.GeoJSONSource).setData({
            type: "FeatureCollection",
            features: incidents.map((incident) => ({
                type: "Feature",
                geometry: { type: "Point", coordinates: [incident.lng, incident.lat] },
                properties: incident,
            })),
        });
    }, [map, incidents]);

    useEffect(() => {
        if (!map || !map.getSource("predictions")) return;
        (map.getSource("predictions") as mapboxgl.GeoJSONSource).setData({
            type: "FeatureCollection",
            features: predictions.map((p) => ({
                type: "Feature",
                geometry: { type: "Point", coordinates: [p.lng, p.lat] },
                properties: p,
            })),
        });
    }, [map, predictions]);

    return (
        <>
            <div ref={containerRef} className={styles.map} style={style} />
            <HeatmapLayer map={map} data={heatmap} />
        </>
    );
}
