import { useState } from 'react';
import { generatePath, Link } from 'react-router-dom';
import { formatPrice, sizes, type Product, type Size } from '@/entities/product/products';
import { useProductCatalog } from '@/entities/product/productCatalogContext';
import { useCart } from '@/features/cart/cartContext';
import { paths } from '@/shared/constants/consts';
import './productCard.scss';

const ProductImage = ({ src, alt }: { src: string; alt: string }) => {
    const [status, setStatus] = useState<'loading' | 'loaded' | 'error'>('loading');

    return (
        <div className={`productCard__picture productCard__picture--${status}`} aria-busy={status === 'loading'}>
            {status !== 'loaded' && <img className="productCard__placeholder" src="/images/products/loading.svg" alt="" aria-hidden="true" />}
            <img
                className="productCard__image"
                src={src}
                alt={alt}
                loading="lazy"
                decoding="async"
                width={1680}
                height={2100}
                onLoad={() => setStatus('loaded')}
                onError={() => setStatus('error')}
                ref={(image) => {
                    if (image?.complete && image.naturalWidth > 0) setStatus('loaded');
                }}
            />
            {status === 'error' && <span className="productCard__image-error">Фото недоступно</span>}
        </div>
    );
};

export const ProductCard = ({ product, compact = false }: { product: Product; compact?: boolean }) => {
    const [selectedId, setSelectedId] = useState(product.id);
    const [size, setSize] = useState<Size>('M');
    const { products } = useProductCatalog();
    const selected = products.find((item) => item.id === selectedId) ?? product;
    const variants = products.filter((item) => item.category === product.category);
    const { addItem } = useCart();
    const url = generatePath(paths.catalogDetail, { id: selected.id });

    return (
        <article className={`productCard${compact ? ' productCard--related' : ''}`}>
            <Link className="productCard__media" to={url} aria-label={`${selected.name}, ${selected.color}`}>
                <ProductImage key={selected.image} src={selected.image} alt={`${selected.name}, ${selected.color}`} />
                {selected.isNew && !compact && <span className="productCard__badge">NEW</span>}
            </Link>
            <Link className="productCard__name" to={url}>{selected.name}</Link>
            <p className="productCard__price">{formatPrice(selected.price)}</p>
            {!compact && <p className="productCard__color">{selected.color}</p>}
            {!compact && (
                <div className="productCard__options">
                    <select className="productCard__select" value={size} onChange={(event) => setSize(event.target.value as Size)} aria-label={`Размер: ${selected.name}`}>
                        {sizes.map((value) => <option className="productCard__option" value={value} key={value} disabled={!selected.stock[value]}>{value}</option>)}
                    </select>
                    <select className="productCard__select" value={selected.id} onChange={(event) => setSelectedId(event.target.value)} aria-label={`Цвет: ${selected.name}`}>
                        {variants.map((variant) => <option className="productCard__option" value={variant.id} key={variant.id}>{variant.color}</option>)}
                    </select>
                </div>
            )}
            <button className="productCard__buy" type="button" disabled={!selected.stock[size]} onClick={() => addItem(selected, size)}>В корзину</button>
        </article>
    );
};
