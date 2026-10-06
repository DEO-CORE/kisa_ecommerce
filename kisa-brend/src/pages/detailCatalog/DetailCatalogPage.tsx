import { useState } from 'react';
import { generatePath, Link, useParams } from 'react-router-dom';
import { Plus } from 'lucide-react';
import { formatPrice, sizes, type Product, type Size } from '@/entities/product/products';
import { useProductCatalog } from '@/entities/product/productCatalogContext';
import { useCart } from '@/features/cart/cartContext';
import { paths } from '@/shared/constants/consts';
import { Modal } from '@/shared/ui/Modal';
import { ProductCard } from '@/widgets/productCard/ProductCard';
import './detailCatalog.scss';

const ProductDetails = ({ product }: { product: Product }) => {
    const { products } = useProductCatalog();
    const [size, setSize] = useState<Size>('M');
    const [showSizes, setShowSizes] = useState(false);
    const [expanded, setExpanded] = useState<string[]>([]);
    const { addItem } = useCart();
    const variants = products.filter((item) => item.apiId === product.apiId);
    const gallery = [product, ...variants.filter((item) => item.id !== product.id)];
    const related = products.filter((item) => item.apiId !== product.apiId).slice(0, 3);
    const sections = [
        { title: 'Состав и уход', text: product.composition, extra: 'Стирать вывернутым наизнанку. Не отбеливать и не сушить в сушильной машине.' },
        { title: 'Посадка', text: product.fit, extra: 'Сравните замеры из таблицы с похожей вещью из вашего гардероба.' },
        { title: 'Доставка и возврат', text: 'Возврат неношеного товара возможен в течение 14 дней.', extra: 'Сохраните бирки и упаковку. Условия доставки можно уточнить при оформлении заказа.' },
    ];

    return (
        <article className="detailCatalog">
            <nav className="detailCatalog__breadcrumbs" aria-label="Хлебные крошки">
                <Link className="detailCatalog__breadcrumb" to={paths.catalog}>Магазин</Link>
                <span className="detailCatalog__separator">/</span>
                <Link className="detailCatalog__breadcrumb" to={paths.catalog}>{product.category}</Link>
                <span className="detailCatalog__separator">/</span>
                <span className="detailCatalog__breadcrumb" aria-current="page">{product.category === 'Брюки' ? 'Smile' : 'From Abusers'}</span>
            </nav>
            <div className="detailCatalog__layout">
                <div className="detailCatalog__gallery">
                    {gallery.map((item, index) => (
                        <img className="detailCatalog__image" src={item.image} alt={`${item.name}, ${item.color}`} key={item.id} loading={index < 2 ? 'eager' : 'lazy'} width={1680} height={2100} />
                    ))}
                </div>
                <div className="detailCatalog__info">
                    <p className="detailCatalog__eyebrow">SS’26 / {product.isNew ? 'Новинка' : 'Коллекция'}</p>
                    <div className="detailCatalog__heading">
                        <h1 className="detailCatalog__title">{product.name}</h1>
                        <p className="detailCatalog__price">{formatPrice(product.price)}</p>
                    </div>
                    <p className="detailCatalog__description">{product.description}</p>
                    <div className="detailCatalog__color-row">
                        <p className="detailCatalog__label">Цвет: {product.colorLabel}</p>
                        <div className="detailCatalog__colors" aria-label="Выбор цвета">
                            {variants.map((variant) => (
                                <Link className={`detailCatalog__swatch${variant.id === product.id ? ' detailCatalog__swatch--selected' : ''}`} style={{ backgroundColor: variant.swatch }} to={generatePath(paths.catalogDetail, { id: variant.id })} aria-label={variant.color} aria-current={variant.id === product.id ? 'true' : undefined} key={variant.id} />
                            ))}
                        </div>
                    </div>
                    <div className="detailCatalog__size-heading">
                        <p className="detailCatalog__label">Размер</p>
                        <button className="detailCatalog__size-guide" type="button" onClick={() => setShowSizes(true)}>Таблица размеров</button>
                    </div>
                    <div className="detailCatalog__sizes" role="group" aria-label="Размер">
                        {sizes.map((value) => <button className="detailCatalog__size" type="button" key={value} disabled={!product.stock[value]} aria-pressed={size === value} onClick={() => setSize(value)}>{value}</button>)}
                    </div>
                    <p className="detailCatalog__stock" aria-live="polite">Выбран размер {size} · осталось {product.stock[size]} шт.</p>
                    <button className="detailCatalog__buy" type="button" onClick={() => addItem(product, size)}>Добавить в корзину — {formatPrice(product.price)}</button>
                    <p className="detailCatalog__delivery">Доставка по России 2–7 дней. Бесплатно при заказе от 15 000.</p>
                    <div className="detailCatalog__accordions">
                        {sections.map(({ title, text, extra }, index) => (
                            <section className="detailCatalog__accordion" key={title}>
                                <button className="detailCatalog__accordion-toggle" type="button" aria-expanded={expanded.includes(title)} aria-controls={`product-info-${index}`} onClick={() => setExpanded((current) => current.includes(title) ? current.filter((item) => item !== title) : [...current, title])}>
                                    {title}<Plus className="detailCatalog__accordion-icon" size={16} strokeWidth={1.5} />
                                </button>
                                <p className="detailCatalog__accordion-summary">{text}</p>
                                <p className="detailCatalog__accordion-extra" id={`product-info-${index}`} hidden={!expanded.includes(title)}>{extra}</p>
                            </section>
                        ))}
                    </div>
                </div>
            </div>
            <section className="detailCatalog__statement" aria-label="Образ">
                <p className="detailCatalog__label">Образ / 01</p>
                <h2 className="detailCatalog__quote">Мягкая архитектура силуэта — вещь, рассчитанная на многослойность и движение.</h2>
            </section>
            <section className="detailCatalog__related" aria-labelledby="related-title">
                <div className="detailCatalog__related-heading">
                    <h2 className="detailCatalog__related-title" id="related-title">С этим носят</h2>
                    <Link className="detailCatalog__all" to={paths.catalog}>Смотреть все →</Link>
                </div>
                <div className="detailCatalog__related-grid">
                    {related.map((item) => <ProductCard product={item} compact key={item.id} />)}
                </div>
            </section>
            <Modal open={showSizes} onClose={() => setShowSizes(false)} title="Таблица размеров">
                <h2 className="detailCatalog__chart-title">Таблица размеров</h2>
                <img className="detailCatalog__chart" src={product.sizeChart} alt={`Таблица размеров — ${product.name}. Замеры изделия в сантиметрах.`} />
            </Modal>
        </article>
    );
};

export const DetailCatalogPage = () => {
    const { id } = useParams();
    const { products, isRemote, error } = useProductCatalog();
    if (!isRemote && !error) return <p role="status">Загрузка товара…</p>;
    if (error) return <p role="alert">Не удалось загрузить товар. Обновите страницу.</p>;
    const product = products.find((item) => item.id === (id === 'demo' ? 'hoodie-grey' : id));
    if (!product) return <section className="detailCatalog detailCatalog--missing"><h1 className="detailCatalog__title">Товар не найден</h1><Link className="detailCatalog__all" to={paths.catalog}>← Вернуться в каталог</Link></section>;
    return <ProductDetails product={product} key={product.id} />;
};
