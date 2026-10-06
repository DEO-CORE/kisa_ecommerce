import { useEffect, useState } from 'react';
import './cookies.scss';

const storageKey = 'kisa-cookie-notice-v1';
const lifetime = 180 * 24 * 60 * 60 * 1000;

function hasAcknowledged() {
    try {
        const saved: unknown = JSON.parse(localStorage.getItem(storageKey) ?? 'null');
        if (!saved || typeof saved !== 'object' || !('acknowledgedAt' in saved)) return false;
        const timestamp = saved.acknowledgedAt;
        return typeof timestamp === 'number' && timestamp <= Date.now() && Date.now() - timestamp < lifetime;
    } catch {
        return false;
    }
}

export const CookieBanner = () => {
    const [visible, setVisible] = useState(() => !hasAcknowledged());
    const [details, setDetails] = useState(false);

    useEffect(() => {
        const open = () => { setVisible(true); setDetails(true); };
        const sync = (event: StorageEvent) => {
            if (event.key === storageKey || event.key === null) setVisible(!hasAcknowledged());
        };
        window.addEventListener('kisa:cookie-settings', open);
        window.addEventListener('storage', sync);
        return () => {
            window.removeEventListener('kisa:cookie-settings', open);
            window.removeEventListener('storage', sync);
        };
    }, []);

    const acknowledge = () => {
        try { localStorage.setItem(storageKey, JSON.stringify({ acknowledgedAt: Date.now() })); } catch { /* The notice can still be dismissed when storage is unavailable. */ }
        setVisible(false);
        setDetails(false);
    };

    if (!visible) return null;

    return (
        <section className="cookie-banner" aria-labelledby="cookie-title">
            <span className="cookie-banner__mark" aria-hidden="true">KISA</span>
            <div className="cookie-banner__copy">
                <h2 id="cookie-title">НЕМНОГО О COOKIE</h2>
                <p>Мы используем необходимые cookie и хранилище браузера для работы сайта, корзины и ваших настроек.</p>
                <p id="cookie-details" hidden={!details} className="cookie-banner__details">Рекламные и аналитические трекеры не подключены. Корзина сохраняется на вашем устройстве. Подтверждение этого уведомления хранится 180 дней. Посмотреть информацию снова можно внизу сайта, нажав «Cookie».</p>
            </div>
            <div className="cookie-banner__actions">
                <button type="button" className="cookie-banner__more" aria-expanded={details} aria-controls="cookie-details" onClick={() => setDetails(!details)}>{details ? 'Свернуть' : 'Подробнее'} ↗</button>
                <button type="button" className="cookie-banner__confirm" onClick={acknowledge}>Понятно →</button>
            </div>
        </section>
    );
};
