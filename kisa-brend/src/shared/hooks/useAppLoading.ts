import { useState, useEffect } from 'react';

// A single, bounded brand entrance per app mount; navigation does not restart it.
export const useAppLoading = (initialDelay = 560) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isReady, setIsReady] = useState(false);

    useEffect(() => {
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const readyTimer = window.setTimeout(() => setIsReady(true), reducedMotion ? 0 : initialDelay);
        const exitTimer = window.setTimeout(() => setIsLoading(false), reducedMotion ? 0 : initialDelay + 240);
        return () => {
            window.clearTimeout(readyTimer);
            window.clearTimeout(exitTimer);
        };
    }, [initialDelay]);

    return { isLoading, isReady };
};
