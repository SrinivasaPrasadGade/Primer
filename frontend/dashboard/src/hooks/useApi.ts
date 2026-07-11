"use client";
import useSWR, { SWRConfiguration } from "swr";

export function useApi<T>(key: string | null, fetcher: () => Promise<T>, config?: SWRConfiguration) {
    return useSWR<T>(key, fetcher, {
        revalidateOnFocus: false,
        shouldRetryOnError: false,
        ...config,
    });
}
