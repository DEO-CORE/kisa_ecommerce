import { Link } from 'react-router-dom';
import './stateScreen.scss';

type Props = {
    code: string;
    label: string;
    title: string;
    description: string;
    action?: { label: string; onClick: () => void; busy?: boolean };
    compact?: boolean;
};

export const StateScreen = ({ code, label, title, description, action, compact = false }: Props) => (
    <section className={`state-screen${compact ? ' state-screen--compact' : ''}`} aria-label={title}>
        <div className="state-screen__art" aria-hidden="true">
            <span className="state-screen__coordinate">KISA / {label}</span>
            <div className="state-screen__number">{code}</div>
            <div className="state-screen__tag"><span>KISA</span><i /><small>ВНЕ КОЛЛЕКЦИИ<br />HANDLE WITH CARE</small><b>↗</b></div>
            <span className="state-screen__seam" />
            <span className="state-screen__edition">ЛИЧНОЕ. КАЖДЫЙ ДЕНЬ.</span>
        </div>
        <div className="state-screen__content">
            <p className="state-screen__label">{label}</p>
            <h1>{title}</h1>
            <p className="state-screen__description">{description}</p>
            <div className="state-screen__actions">
                {action ? <button type="button" disabled={action.busy} onClick={action.onClick}>{action.busy ? 'Загружаем…' : action.label}<span aria-hidden="true">↻</span></button> : <Link to="/catalog">В магазин<span aria-hidden="true">↗</span></Link>}
                <Link className="state-screen__secondary" to="/">На главную<span aria-hidden="true">↗</span></Link>
            </div>
            <p className="state-screen__footnote">Новый маршрут — тоже часть вашего стиля.</p>
        </div>
    </section>
);
