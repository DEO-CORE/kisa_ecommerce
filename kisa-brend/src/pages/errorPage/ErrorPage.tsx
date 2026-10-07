import { StudioCredit } from '@/shared/ui/studioCredit/StudioCredit';
import { useEffect } from 'react';
import { isRouteErrorResponse, Link, useRouteError } from 'react-router-dom';
import { StateScreen } from '@/shared/ui/stateScreen/StateScreen';
import './errorPage.scss';

export const ErrorPage = ({ notFound = false }: { notFound?: boolean }) => {
    const error = useRouteError();
    const missing = notFound || (isRouteErrorResponse(error) && error.status === 404);
    useEffect(() => {
        document.title = `${missing ? 'Страница не найдена' : 'Не удалось открыть страницу'} — KISA`;
        return () => { document.title = 'KISA — одежда как личное пространство'; };
    }, [missing]);
    return <div className="error-page">
        <header className="error-page__header"><Link to="/" aria-label="KISA — главная">KISA</Link><span>НЕ ВСЁ ИДЁТ ПО ВЫКРОЙКЕ</span><Link to="/contacts">Связаться ↗</Link></header>
        <main><StateScreen code={missing ? '404' : 'ERR'} label={missing ? 'Страница не найдена' : 'Что-то пошло не так'} title={missing ? 'Эта страница вне коллекции.' : 'Кажется, разошёлся шов.'} description={missing ? 'Возможно, она сменила адрес или её больше нет. Но ваш следующий любимый образ уже ждёт в магазине.' : 'Не удалось открыть страницу. Попробуйте загрузить её ещё раз или вернитесь на главную.'} action={missing ? undefined : { label: 'Попробовать снова', onClick: () => window.location.reload() }} /></main>
        <footer className="error-page__footer"><span>KISA E COMMERCE©</span><StudioCredit /></footer>
    </div>;
};
