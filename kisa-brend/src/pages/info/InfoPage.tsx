import { Fragment, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useContent } from '@/shared/api/content';
import { documents, isPublicEmail, type InfoDocument, type StoreContacts } from './documents';
import './info.scss';

export const InfoPage = ({ pageType }: { pageType: string }) => {
    const definition = documents.find(item => item.type === pageType);
    const page = useContent<InfoDocument>(`/footer/info-pages/${pageType}/`);
    const contacts = useContent<StoreContacts>('/footer/contacts/');
    const support = useContent<{ email: string; telegram_url: string }>('/footer/support/');
    const title = page.data?.title ?? definition?.title ?? 'Информация';
    const showContacts = pageType === 'contacts';
    useEffect(() => {
        document.title = `${title} — KISA`;
        window.scrollTo(0, 0);
        return () => { document.title = 'KISA — одежда как личное пространство'; };
    }, [title]);
    const details = contacts.data;
    const contactEmail = isPublicEmail(details?.email) ? details?.email : isPublicEmail(support.data?.email) ? support.data?.email : undefined;
    const telegram = details?.telegram_url || support.data?.telegram_url;
    const fields = details ? [
        ['Продавец', details.seller_name], ['Страна регистрации', details.country],
        ['Регистрационный номер', details.registration_number], ['ИНН / налоговый номер', details.tax_id],
        ['Юридический адрес', details.legal_address], ['Адрес', details.address], ['Режим работы', details.work_hours],
    ].filter(([, value]) => Boolean(value)) : [];
    return (
        <article className="info-page">
            <Link className="info-page__back" to="/">← KISA / ИНФОРМАЦИЯ</Link>
            <h1>{title}</h1>
            {page.data?.updated_at && <p className="info-page__date">Обновлено {new Date(page.data.updated_at).toLocaleDateString('ru-RU')}</p>}
            <div className="info-page__layout">
                <nav className="info-page__nav" aria-label="Документы магазина">{documents.map(item => <Link key={item.type} to={item.path} aria-current={item.type === pageType ? 'page' : undefined}>{item.label} <span aria-hidden="true">↗</span></Link>)}</nav>
                <div className="info-page__content">
                    {page.isPending && <p role="status">Загружаем информацию…</p>}
                    {page.isError && <div role="alert"><p>Страница пока недоступна.</p><button type="button" onClick={() => void page.refetch()}>Попробовать снова →</button></div>}
                    {page.data?.content.split(/\n\s*\n/).map((block, index) => {
                        if (!block.startsWith('## ')) return <p key={index}>{block}</p>;
                        const [heading, ...lines] = block.split('\n');
                        const body = lines.join('\n').trim();
                        return <Fragment key={index}><h2>{heading.slice(3)}</h2>{body && <p>{body}</p>}</Fragment>;
                    })}
                    {showContacts && <section aria-label="Контактные данные">
                        {fields.length > 0 && <dl className="info-page__requisites">{fields.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>}
                        <div className="info-page__contacts">
                            {details?.phone && <a href={`tel:${details.phone}`}>{details.phone}</a>}
                            {contactEmail && <a href={`mailto:${contactEmail}`}>{contactEmail}</a>}
                            {telegram && <a href={telegram} target="_blank" rel="noreferrer">Telegram ↗</a>}
                            {!contacts.isPending && !support.isPending && !details?.phone && !contactEmail && !telegram && <p>Контактные данные магазина уточняются и будут опубликованы здесь.</p>}
                        </div>
                    </section>}
                    {pageType === 'cookies' && <button className="info-page__button" type="button" onClick={() => window.dispatchEvent(new Event('kisa:cookie-settings'))}>Настройки cookie →</button>}
                    <div className="info-page__related"><Link to="/contacts">Контакты и реквизиты →</Link><Link to="/catalog">Перейти в магазин →</Link></div>
                </div>
            </div>
        </article>
    );
};
