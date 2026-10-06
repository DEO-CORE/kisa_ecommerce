import { useEffect, useRef, useState } from 'react';
import { ArrowUpRight, ChevronDown, Plus, ShoppingBasket } from 'lucide-react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { paths } from '@/shared/constants/consts';
import { useCart } from '@/features/cart/cartContext';
import './header.scss';

const MobileNavigation = () => {
    const [isOpen, setIsOpen] = useState(false);
    const { pathname } = useLocation();
    const sectionLabel = pathname === paths.about ? 'О нас' : pathname === paths.news ? 'Новости' : 'Магазин';
    const rootRef = useRef<HTMLDivElement>(null);
    const buttonRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        if (!isOpen) return;

        const onPointerDown = (event: PointerEvent) => {
            if (!rootRef.current?.contains(event.target as Node)) setIsOpen(false);
        };
        const onKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                setIsOpen(false);
                buttonRef.current?.focus();
            }
        };

        document.addEventListener('pointerdown', onPointerDown);
        document.addEventListener('keydown', onKeyDown);
        return () => {
            document.removeEventListener('pointerdown', onPointerDown);
            document.removeEventListener('keydown', onKeyDown);
        };
    }, [isOpen]);

    return (
        <div
            className="header__mobile"
            ref={rootRef}
            onBlur={(event) => {
                if (!event.currentTarget.contains(event.relatedTarget)) setIsOpen(false);
            }}
        >
            <button
                className="header__toggle"
                type="button"
                ref={buttonRef}
                aria-expanded={isOpen}
                aria-controls="mobile-navigation"
                onClick={() => setIsOpen(!isOpen)}
            >
                {sectionLabel}
                <ChevronDown className="header__chevron" size={24} aria-hidden="true" />
            </button>
            <nav
                className="header__dropdown"
                id="mobile-navigation"
                aria-label="Мобильная навигация"
                hidden={!isOpen}
                onClick={() => setIsOpen(false)}
            >
                <NavLink className="header__dropdown-link" to={paths.catalog}>
                    Каталог
                    <ArrowUpRight className="header__dropdown-arrow" size={16} aria-hidden="true" />
                </NavLink>
                <NavLink className="header__dropdown-link" to={paths.about}>
                    О нас
                    <ArrowUpRight className="header__dropdown-arrow" size={16} aria-hidden="true" />
                </NavLink>
                <NavLink className="header__dropdown-link" to={paths.news}>
                    Новости
                    <ArrowUpRight className="header__dropdown-arrow" size={16} aria-hidden="true" />
                </NavLink>
            </nav>
        </div>
    );
};

export const Header = () => {
    const location = useLocation();
    const isHome = location.pathname === paths.main;
    const { items, openCart } = useCart();
    const count = items.reduce((sum, item) => sum + item.quantity, 0);

    return (
        <header className={`header${isHome ? ' header--overlay' : ''}`}>
            <div className="container header__container">
                <Link className="header__logo" to={paths.main} aria-label="KISA — главная">
                    KISA
                </Link>
                <nav className="header__nav" aria-label="Основная навигация">
                    <Link className="header__link" to={paths.catalog}>Магазин</Link>
                    <Link className="header__link" to={paths.about}>О нас</Link>
                    <Link className="header__link" to={paths.news}>Новости</Link>
                </nav>
                <MobileNavigation key={location.key} />
                <button className="header__cart" type="button" aria-label={`Корзина, товаров: ${count}`} onClick={openCart}>
                    <ShoppingBasket className="header__cart-icon" size={28} strokeWidth={1.5} aria-hidden="true" />
                    <Plus className="header__cart-plus" size={12} strokeWidth={1.5} aria-hidden="true" />
                    <span className="header__cart-count" aria-hidden="true">{count}</span>
                </button>
            </div>
        </header>
    );
};
