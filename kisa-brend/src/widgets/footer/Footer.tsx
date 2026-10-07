import { StudioCredit } from '@/shared/ui/studioCredit/StudioCredit';
import './footer.scss';
import { Link } from 'react-router-dom';
import { useContent, useList } from '@/shared/api/content';
import { documents, isPublicEmail, type InfoDocument } from '@/pages/info/documents';

import { useLocation } from 'react-router-dom';

export const Footer = ({ shop = false }: { shop?: boolean }) => {
    const contacts = useContent<{ telegram_url: string; phone: string; address: string }>('/footer/contacts/');
    const partnership = useContent<{ email: string }>('/footer/partnership/');
    const support = useContent<{ email: string; telegram_url: string }>('/footer/support/');
    const pages = useList<InfoDocument>('/footer/info-pages/');
    const available = pages.data ? documents.filter(item => pages.data.some(page => page.page_type === item.type)) : documents;
    const { pathname } = useLocation();
    const isShop = shop || pathname === '/catalog';
    return (
        <>
        <footer className={`footer${isShop ? ' footer--shop' : ''}`}>
            <div className="container footer__container">
                <div className="footer__info">
                    <div className="footer__column">
                        <section className="footer__group" aria-label="Контакты">
                            <h2 className="footer__title"><Link to="/contacts">Контакты →</Link></h2>
                            <div className="footer__links">{contacts.data?.telegram_url && <a href={contacts.data.telegram_url}>Telegram</a>}{contacts.data?.phone && <a href={`tel:${contacts.data.phone}`}>{contacts.data.phone}</a>}{contacts.data?.address && <p>{contacts.data.address}</p>}</div>
                        </section>
                        <section className="footer__group" aria-label="Сотрудничество">
                            <h2 className="footer__title">Сотрудничество →</h2>
                            <div className="footer__links">
                                {isPublicEmail(partnership.data?.email) && <a className="footer__link" href={`mailto:${partnership.data!.email}`}>{partnership.data!.email}</a>}
                            </div>
                        </section>
                    </div>
                    <div className="footer__column">
                        <section className="footer__group" aria-label="Покупателям">
                            <h2 className="footer__title">Покупателям →</h2>
                            <div className="footer__links footer__links--buyers">
                                {available.map(page => <Link className="footer__link" key={page.type} to={page.path}>{page.label}</Link>)}
                                <button className="footer__link" type="button" onClick={() => window.dispatchEvent(new Event('kisa:cookie-settings'))}>Настройки cookie</button>
                            </div>
                        </section>
                        <section className="footer__group" aria-label="Поддержка">
                            <h2 className="footer__title">Поддержка →</h2>
                            <div className="footer__links">
                                {support.data?.telegram_url && <a className="footer__link" href={support.data.telegram_url}>Telegram</a>}
                                {isPublicEmail(support.data?.email) && <a className="footer__link" href={`mailto:${support.data!.email}`}>{support.data!.email}</a>}
                            </div>
                        </section>
                    </div>
                    <p className="footer__copyright">
                        <span className="footer__copyright-line">KISA E COMMERCE©</span>
                        <span className="footer__copyright-line">ALL RIGHTS RESERVED</span>
                    </p>
                </div>
                <div className="footer__studio"><StudioCredit /></div>
                {isShop && <div className="footer__wordmark footer__wordmark--mono" aria-label="KISA">KISA</div>}
                <img className="footer__wordmark" src="/images/brand/kisa-display.png" alt="KISA" width={1440} height={446} />
            </div>
        </footer>
        </>
    );
};
