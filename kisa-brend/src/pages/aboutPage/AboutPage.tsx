import { EditorialImage } from '@/shared/ui/EditorialImage';
import './about.scss';

import { useContent, useList } from '@/shared/api/content';

export const AboutPage = () => {
    const main = useContent<{ slogan: string; manifesto: string; team_photo_url: string | null }>('/about/main-page/');
    const partnership = useContent<{ email: string }>('/footer/partnership/');
    const team = useContent<{ text: string; photo_url: string | null }>('/about/team/');
    const principleQuery = useList<{ title: string; description: string }>('/about/principles/');
    const historyQuery = useList<{ year: string; description: string }>('/about/history/');
    const principles = (principleQuery.data ?? []).map(row => [row.title, row.description]);
    const history = (historyQuery.data ?? []).map(row => [row.year, row.description]);
    return (
    <article className="aboutPage editorial">
        {main.error && <p role="alert">Не удалось загрузить информацию о бренде.</p>}
        <header className="aboutPage__intro editorial__container">
            <p className="editorial__eyebrow">KISA / ИЗ МОСКВЫ С 2022</p>
            <h1>{main.data?.slogan || 'KISA'}</h1>
            <p className="aboutPage__lead">{main.data?.slogan}</p>
        </header>
        {main.data?.team_photo_url ? <img className="aboutPage__hero" src={main.data.team_photo_url} alt="KISA" width={1440} height={780} /> : <EditorialImage className="aboutPage__hero" name="about-hero" alt="KISA" width={1440} height={780} />}
        <div className="editorial__container">
            <section className="aboutPage__manifesto" aria-labelledby="manifesto-title">
                <div className="editorial__eyebrow"><h2 id="manifesto-title">МАНИФЕСТ</h2><span>01–04</span></div>
                <p>{main.data?.manifesto}</p>
            </section>
            <div className="aboutPage__photos">
                <EditorialImage name="fabric" alt="Крупный план фактуры плотного хлопка" width={632} height={680} loading="lazy" />
                <EditorialImage name="fitting" alt="Работа над посадкой худи в ателье" width={632} height={680} loading="lazy" />
            </div>
            <section className="aboutPage__principles" aria-labelledby="principles-title">
                <div className="editorial__section-heading"><h2 id="principles-title">НАШИ ПРИНЦИПЫ</h2><span>МЕНЬШЕ, НО ТОЧНЕЕ</span></div>
                <div className="aboutPage__principle-grid">{principles.map(([title, text], index) => (
                    <div className="aboutPage__principle" key={title}><span className="editorial__eyebrow">0{index + 1}</span><h3>{title}</h3><p>{text}</p></div>
                ))}</div>
            </section>
        </div>
        <section className="aboutPage__history" aria-labelledby="history-title">
            <div className="editorial__container aboutPage__history-grid">
                <div><p className="editorial__eyebrow">КАК МЫ РОСЛИ</p><h2 id="history-title">Три года, один<br />ясный язык.</h2></div>
                <dl>{history.map(([year, text]) => <div key={year}><dt>{year}</dt><dd>{text}</dd></div>)}</dl>
            </div>
        </section>
        <section className="aboutPage__team editorial__container" aria-labelledby="team-title">
            {team.data?.photo_url && <img src={team.data.photo_url} alt="Команда KISA" width={612} height={620} loading="lazy" />}
            <div><p className="editorial__eyebrow">КОМАНДА</p><h2 id="team-title">KISA — маленькая команда с полным вниманием к каждой вещи.</h2><p className="aboutPage__team-description">{team.data?.text}</p>{partnership.data?.email && <a className="aboutPage__contact" href={`mailto:${partnership.data.email}`}>НАПИСАТЬ НАМ ↗</a>}</div>
        </section>
    </article>
    );
};
