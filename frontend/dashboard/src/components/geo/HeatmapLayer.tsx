"use client";
import { useEffect, useRef } from "react";
import L from "leaflet";
import { HeatmapCell } from "@/lib/api";

export function HeatmapLayer({ map, data }: { map: L.Map | null; data: HeatmapCell[] }) {
    const layerRef = useRef<L.LayerGroup | null>(null);

    useEffect(() => {
        if (!map) return;

        if (!layerRef.current) {
            layerRef.current = L.layerGroup().addTo(map);
        }

        layerRef.current.clearLayers();

        data.forEach((cell) => {
            const intensity = Math.min(cell.intensity, 1);
            const color = intensity > 0.65 ? "#EF4444" : intensity > 0.35 ? "#F59E0B" : "#EAB308";

            const marker = L.circleMarker([cell.lat, cell.lng], {
                radius: 4,
                fillColor: color,
                color: color,
                weight: 0,
                opacity: 1,
                fillOpacity: intensity * 0.7,
            });

            marker.addTo(layerRef.current!);
        });
    }, [map, data]);

    return null;
}
