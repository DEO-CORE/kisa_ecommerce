import './footer.scss';
import { useState } from 'react';
import { useContent, useList } from '@/shared/api/content';
import { Modal } from '@/shared/ui/Modal';
interface InfoPage { page_type: string; title: string; content: string }

import { useLocation } from 'react-router-dom';

export const Footer = ({ shop = false }: { shop?: boolean }) => {
    const contacts = useContent<{ telegram_url: string; phone: string; address: string }>('/footer/contacts/');
    const partnership = useContent<{ email: string }>('/footer/partnership/');
    const support = useContent<{ email: string; telegram_url: string }>('/footer/support/');
    const pages = useList<InfoPage>('/footer/info-pages/');
    const [opened, setOpened] = useState<InfoPage | null>(null);
    const { pathname } = useLocation();
    const isShop = shop || pathname === '/catalog';
    return (
        <>
        <footer className={`footer${isShop ? ' footer--shop' : ''}`}>
            <div className="container footer__container">
                <div className="footer__info">
                    <div className="footer__column">
                        <section className="footer__group" aria-label="Контакты">
                            <h2 className="footer__title">Контакты →</h2>
                            <div className="footer__links">{contacts.data?.telegram_url && <a href={contacts.data.telegram_url}>Telegram</a>}{contacts.data?.phone && <a href={`tel:${contacts.data.phone}`}>{contacts.data.phone}</a>}{contacts.data?.address && <p>{contacts.data.address}</p>}</div>
                        </section>
                        <section className="footer__group" aria-label="Сотрудничество">
                            <h2 className="footer__title">Сотрудничество →</h2>
                            <div className="footer__links">
                                {partnership.data?.email && <a className="footer__link" href={`mailto:${partnership.data.email}`}>{partnership.data.email}</a>}
                            </div>
                        </section>
                    </div>
                    <div className="footer__column">
                        <section className="footer__group" aria-label="Покупателям">
                            <h2 className="footer__title">Покупателям →</h2>
                            <div className="footer__links footer__links--buyers">
                                {(pages.data ?? []).map(page => <button className="footer__link" type="button" key={page.page_type} onClick={() => setOpened(page)}>{page.title}</button>)}
                            </div>
                        </section>
                        <section className="footer__group" aria-label="Поддержка">
                            <h2 className="footer__title">Поддержка →</h2>
                            <div className="footer__links">
                                {support.data?.telegram_url && <a className="footer__link" href={support.data.telegram_url}>Telegram</a>}
                                {support.data?.email && <a className="footer__link" href={`mailto:${support.data.email}`}>{support.data.email}</a>}
                            </div>
                        </section>
                    </div>
                    <p className="footer__copyright">
                        <span className="footer__copyright-line">KISA E COMMERCE©</span>
                        <span className="footer__copyright-line">ALL RIGHTS RESERVED</span>
                    </p>
                </div>
                {isShop && <div className="footer__wordmark footer__wordmark--mono" aria-label="KISA">KISA</div>}
                <img className="footer__wordmark" src="/images/brand/kisa-display.png" alt="KISA" width={1440} height={446} />
            </div>
        </footer>
        <Modal open={opened !== null} onClose={() => setOpened(null)} title={opened?.title ?? "Информация"}>{opened && <><h2>{opened.title}</h2><p style={{ whiteSpace: "pre-wrap" }}>{opened.content}</p></>}</Modal>
        </>
    );
};
