import { StateScreen } from '@/shared/ui/stateScreen/StateScreen';
import { useState } from 'react';
import { Modal } from '@/shared/ui/Modal';
import { useContent, useList, subscribe } from '@/shared/api/content';
import './news.scss';

interface Publication {
    slug: string; title: string; pub_type: string; published_at: string;
    preview_text: string; preview_image_url: string | null; is_featured: boolean;
    content?: string; hero_image_url?: string | null;
}
const categories: Record<string, string> = { ITEM: 'ВЕЩИ', PEOPLE: 'ЛЮДИ', GUIDE: 'ГИДЫ', EVENT: 'СОБЫТИЯ' };
const ArticlePreview = ({ slug }: { slug: string }) => {
    const query = useContent<Publication>(`/journal/publications/${encodeURIComponent(slug)}/`);
    if (query.isPending) return <p role="status">Загрузка…</p>;
    if (query.error) return <StateScreen compact code="OFF" label="Публикация недоступна" title="История прервалась." description="Не удалось открыть публикацию. Попробуйте загрузить её ещё раз." action={{ label: 'Повторить', onClick: () => void query.refetch(), busy: query.isFetching }} />;
    const article = query.data;
    return <>{(article.hero_image_url || article.preview_image_url) && <img src={article.hero_image_url || article.preview_image_url!} alt={article.title} />}<h2>{article.title}</h2><p style={{ whiteSpace: 'pre-wrap' }}>{article.content || article.preview_text}</p></>;
};
export const NewsPage = () => {
    const query = useList<Publication>('/journal/publications/');
    const [subscriptionMessage, setSubscriptionMessage] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [category, setCategory] = useState('ВСЕ');
    const [limit, setLimit] = useState(6);
    const [opened, setOpened] = useState<Publication | null>(null);
    const articles = (query.data ?? []).filter(row => category === 'ВСЕ' || row.pub_type === category);
    return <div className="news editorial">
        <header className="news__intro editorial__container"><p className="editorial__eyebrow">KISA JOURNAL</p><h1>НОВОСТИ</h1><p>Коллекции, люди, процессы и всё, что формирует мир KISA.</p></header>
        <nav className="news__navigation" aria-label="Категории новостей"><div className="editorial__container">{['ВСЕ', ...Object.keys(categories)].map(value => <button type="button" key={value} aria-pressed={category === value} onClick={() => { setCategory(value); setLimit(6); }}>{categories[value] || value}</button>)}</div></nav>
        <div className="editorial__container news__content">
            {query.isPending && <p role="status">Загрузка…</p>}
            {query.error && <StateScreen compact code="OFF" label="Журнал недоступен" title="Истории немного подождут." description="Не удалось загрузить журнал. Проверьте подключение и попробуйте снова." action={{ label: 'Повторить', onClick: () => void query.refetch(), busy: query.isFetching }} />}
            {query.isSuccess && !articles.length && <p>Публикаций пока нет.</p>}
            <section className="news__latest"><div className="news__grid">{articles.slice(0, limit).map(article => <article className="news__card" key={article.slug}>
                <button className="news__image-button" type="button" onClick={() => setOpened(article)} aria-label={article.title}>{article.preview_image_url && <img src={article.preview_image_url} alt={article.title} width={410} height={450} loading="lazy" />}</button>
                <div className="news__meta editorial__eyebrow"><span>{categories[article.pub_type]}</span><time dateTime={article.published_at}>{new Date(article.published_at).toLocaleDateString('ru')}</time></div>
                <h3><button type="button" onClick={() => setOpened(article)}>{article.title}</button></h3><p>{article.preview_text}</p>
            </article>)}</div>{articles.length > limit && <button className="news__more" type="button" onClick={() => setLimit(limit + 6)}>ЗАГРУЗИТЬ ЕЩЁ</button>}</section>
        </div>
        <section className="news__subscribe"><div className="editorial__container news__subscribe-inner">
            <div><h2>Новости дропов — без лишнего.</h2><p>Редкие письма о новых вещах и событиях.</p></div>
            <form onSubmit={async event => {
                event.preventDefault();
                const email = String(new FormData(event.currentTarget).get('email'));
                setSubmitting(true);
                try { setSubscriptionMessage(await subscribe(email)); }
                catch (error) { setSubscriptionMessage(error instanceof Error ? error.message : 'Не удалось подписаться.'); }
                finally { setSubmitting(false); }
            }}><div className="news__email"><input type="email" name="email" placeholder="ВАШ EMAIL" aria-label="Ваш email" autoComplete="email" required /><button type="submit" disabled={submitting} aria-label="Подписаться">→</button></div><p role="status">{subscriptionMessage}</p></form>
        </div></section>
        <Modal open={opened !== null} onClose={() => setOpened(null)} title={opened?.title ?? 'Публикация'} className="news__preview">{opened && <ArticlePreview slug={opened.slug} />}</Modal>
    </div>;
};
