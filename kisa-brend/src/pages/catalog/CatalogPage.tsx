import { useState, type CSSProperties } from 'react';
import { useProductCatalog } from '@/entities/product/productCatalogContext';
import { ProductCard } from '@/widgets/productCard/ProductCard';
import './catalog.scss';

export const CatalogPage = () => {
    const { products, error, isRemote } = useProductCatalog();
    const [filtersOpen, setFiltersOpen] = useState(false);
    const [color, setColor] = useState('');
    const [category, setCategory] = useState('');
    const [collection, setCollection] = useState('');
    const [sort, setSort] = useState('');
    const [limit, setLimit] = useState(16);
    const catalog = products;
    const filtered = catalog.filter((product) =>
        (!color || product.color === color) && (!category || product.category === category) && (!collection || product.isNew));
    const sorted = [...filtered].sort((a, b) => sort === 'asc' ? a.price - b.price : sort === 'desc' ? b.price - a.price : 0);
    const visible = sorted.slice(0, limit);
    const hasFilters = !!(color || category || collection || sort);
    const adaptiveOrder = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 4, 9, 14, 15];
    const reset = () => { setColor(''); setCategory(''); setCollection(''); setSort(''); setLimit(16); };

    return (
        <section className="catalog" aria-label="Каталог одежды">
            {error && <p className="catalog__api-notice" role="status">Сервер каталога недоступен. Попробуйте обновить страницу.</p>}
            {!isRemote && !error && <p className="catalog__api-notice" role="status">Загрузка каталога…</p>}
            <div className="catalog__toolbar">
                <div className="catalog__mobile-toolbar">
                    <button type="button" aria-expanded={filtersOpen} aria-controls="catalog-filters" onClick={() => setFiltersOpen(!filtersOpen)}>Фильтры <span aria-hidden="true">⌄</span></button>
                    <select value={sort} onChange={(event) => setSort(event.target.value)} aria-label="Сортировка">
                        <option value="">Сортировка ⌄</option><option value="asc">Сначала дешевле</option><option value="desc">Сначала дороже</option>
                    </select>
                </div>
                <div className={`catalog__filters${filtersOpen ? ' catalog__filters--open' : ''}`} id="catalog-filters">
                    <select className="catalog__filter" value={color} onChange={(event) => setColor(event.target.value)} aria-label="Цвет">
                        <option className="catalog__option" value="">Цвет</option>
                        {[...new Set(products.map((product) => product.color))].map((value) => <option className="catalog__option" value={value} key={value}>{value}</option>)}
                    </select>
                    <select className="catalog__filter" value={sort} onChange={(event) => setSort(event.target.value)} aria-label="Цена">
                        <option className="catalog__option" value="">Цена</option>
                        <option className="catalog__option" value="asc">Сначала дешевле</option>
                        <option className="catalog__option" value="desc">Сначала дороже</option>
                    </select>
                    <select className="catalog__filter" value={category} onChange={(event) => setCategory(event.target.value)} aria-label="Категории">
                        <option className="catalog__option" value="">Категории</option>
                        {['Худи', 'Брюки', 'Футболки'].map((value) => <option className="catalog__option" value={value} key={value}>{value}</option>)}
                    </select>
                    <select className="catalog__filter" value={collection} onChange={(event) => setCollection(event.target.value)} aria-label="Коллекции">
                        <option className="catalog__option" value="">Коллекции</option>
                        <option className="catalog__option" value="new">Новинки</option>
                    </select>
                    {hasFilters && <button className="catalog__reset" type="button" onClick={reset}>Сбросить ×</button>}
                </div>
                <p className="catalog__count" aria-live="polite">{visible.length} товаров</p>
            </div>
            <div className="catalog__grid">
                {visible.map((product, index) => <div className="catalog__item" key={`${product.id}-${index}`} style={{ '--catalog-order': hasFilters ? index : adaptiveOrder[index] ?? index } as CSSProperties}><ProductCard product={product} /></div>)}
            </div>
            {!visible.length && <div className="catalog__empty"><p className="catalog__empty-text">Товары не найдены</p><button className="catalog__reset" type="button" onClick={reset}>Сбросить фильтры</button></div>}
            {visible.length < sorted.length && <button className="catalog__more" type="button" onClick={() => setLimit((value) => value + 4)}>Загрузить ещё</button>}
        </section>
    );
};
