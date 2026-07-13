"use client";
import { useEffect } from "react";
import type maplibregl from "maplibre-gl";
import { HeatmapCell } from "@/lib/api";

// Manages the crime heatmap source + layer on a given MapLibre map instance.
// Red-orange-yellow gradient per UI/UX §6.3.
export function HeatmapLayer({ map, data }: { map: maplibregl.Map | null; data: HeatmapCell[] }) {
    useEffect(() => {
        if (!map) return;

        function setup() {
            if (!map || map.getSource("heatmap-points")) return;
            map.addSource("heatmap-points", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
            map.addLayer({
                id: "heatmap-layer",
                type: "heatmap",
                source: "heatmap-points",
                paint: {
                    "heatmap-weight": ["get", "intensity"],
                    "heatmap-intensity": 1.2,
                    "heatmap-color": [
                        "interpolate", ["linear"], ["heatmap-density"],
                        0, "rgba(234,179,8,0)",
                        0.35, "rgba(234,179,8,0.6)",
                        0.65, "rgba(245,158,11,0.75)",
                        1, "rgba(239,68,68,0.9)",
                    ],
                    "heatmap-radius": 28,
                },
            });
        }

        if (map.isStyleLoaded()) setup();
        else map.on("load", setup);
    }, [map]);

    useEffect(() => {
        if (!map) return;
        const source = map.getSource("heatmap-points") as maplibregl.GeoJSONSource | undefined;
        if (!source) return;
        source.setData({
            type: "FeatureCollection",
            features: data.map((cell) => ({
                type: "Feature",
                geometry: { type: "Point", coordinates: [cell.lng, cell.lat] },
                properties: { intensity: cell.intensity, crime_type: cell.crime_type },
            })),
        });
    }, [map, data]);

    return null;
}
