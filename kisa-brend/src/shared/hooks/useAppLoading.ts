import { useState, useEffect } from 'react';

export const useAppLoading = (initialDelay: number = 1000) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isReady, setIsReady] = useState(false);

    useEffect(() => {
        const checkAppReady = () => {
            const isDOMReady = document.readyState === 'complete' || document.readyState === 'interactive';

            if (isDOMReady) {
                const timer = setTimeout(() => {
                    setIsLoading(false);
                    setIsReady(true);
                }, initialDelay);

                return () => clearTimeout(timer);
            } else {
                const handleReady = () => {
                    const timer = setTimeout(() => {
                        setIsLoading(false);
                        setIsReady(true);
                    }, initialDelay);
                    return () => clearTimeout(timer);
                };

                document.addEventListener('DOMContentLoaded', handleReady);
                window.addEventListener('load', handleReady);

                return () => {
                    document.removeEventListener('DOMContentLoaded', handleReady);
                    window.removeEventListener('load', handleReady);
                };
            }
        };

        const cleanup = checkAppReady();
        return cleanup;
    }, [initialDelay]);

    return { isLoading, isReady };
};
