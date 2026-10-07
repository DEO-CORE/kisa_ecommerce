import './loading.scss';

export const LoadingPage = ({ leaving = false }: { leaving?: boolean }) => (
    <div className={`kisa-loader${leaving ? ' kisa-loader--leaving' : ''}`} role="status" aria-label="Загружаем KISA">
        <div className="kisa-loader__top" aria-hidden="true"><span>KISA / E COMMERCE</span><span>ОДЕЖДА КАК ЛИЧНОЕ ПРОСТРАНСТВО</span></div>
        <div className="kisa-loader__center" aria-hidden="true">
            <span className="kisa-loader__cross kisa-loader__cross--left">+</span>
            <div className="kisa-loader__word">{'KISA'.split('').map((letter, index) => <span key={letter} style={{ animationDelay: `${index * 65}ms` }}>{letter}</span>)}</div>
            <span className="kisa-loader__cross kisa-loader__cross--right">+</span>
            <div className="kisa-loader__track"><span /></div>
            <p className="kisa-loader__caption">ГОТОВИМ ВАШЕ ПРОСТРАНСТВО<span>…</span></p>
        </div>
        <div className="kisa-loader__bottom" aria-hidden="true"><span>ЛИЧНОЕ. КАЖДЫЙ ДЕНЬ.</span><span className="kisa-loader__indicator" /></div>
    </div>
);
