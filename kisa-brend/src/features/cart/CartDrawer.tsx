import { useState } from 'react';
import { useContent } from '@/shared/api/content';
import { buildWhatsAppUrl } from './whatsapp';
import { Link, generatePath } from 'react-router-dom';
import { Minus, Plus, X } from 'lucide-react';
import { formatPrice } from '@/entities/product/products';
import { useProductCatalog } from '@/entities/product/productCatalogContext';
import { paths } from '@/shared/constants/consts';
import { Modal } from '@/shared/ui/Modal';
import { useCart } from './cartContext';
import './cart.scss';
import { ProductCard } from '@/widgets/productCard/ProductCard';
import { Footer } from '@/widgets/footer/Footer';

export const CartDrawer = () => {
    const { items, isOpen, closeCart, changeQuantity } = useCart();
    const { products } = useProductCatalog();
    const contacts = useContent<{ phone: string }>('/footer/contacts/');
    const [submitError, setSubmitError] = useState('');
    const entries = items.flatMap((item) => {
        const product = products.find((candidate) => candidate.id === item.productId);
        return product ? [{ ...item, product }] : [];
    });
    const total = entries.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
    const handleClose = () => {
        closeCart();
        setSubmitError('');
    };
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setSubmitError('');
        if (entries.length !== items.length || !entries.length || entries.some(({ product, size, quantity }) => quantity > product.stock[size])) {
            setSubmitError('Наличие товаров изменилось. Проверьте количество и размеры в корзине.');
            return;
        }
        const formData = new FormData(event.currentTarget);
        try {
            const url = buildWhatsAppUrl(contacts.data?.phone ?? '', entries, {
                name: String(formData.get('customer_name') ?? '').trim(),
                phone: String(formData.get('customer_phone') ?? '').trim(),
                delivery: String(formData.get('delivery') ?? '').trim(),
                comment: String(formData.get('comment') ?? '').trim(),
            }, window.location.origin);
            window.location.assign(url);
        } catch (error) {
            setSubmitError(error instanceof Error ? error.message : 'Не удалось открыть WhatsApp.');
        }
    };

    return (
        <Modal open={isOpen} onClose={handleClose} title="Ваш заказ" className="cart">
            <h2 className="cart__title">Ваш заказ:</h2>
            {entries.length ? (
                <>
                    <ul className="cart__items">
                        {entries.map(({ product, size, quantity }) => (
                            <li className="cart__item" key={`${product.id}-${size}`}>
                                <Link className="cart__image-link" to={generatePath(paths.catalogDetail, { id: product.id })} onClick={closeCart}>
                                    <img className="cart__image" src={product.image} alt={product.name} />
                                </Link>
                                <div className="cart__info">
                                    <Link className="cart__name" to={generatePath(paths.catalogDetail, { id: product.id })} onClick={closeCart}>{product.name}</Link>
                                    <p className="cart__option">Размер: {size}</p>
                                    <p className="cart__option">Цвет: {product.color}</p>
                                    <p className="cart__sku">{product.sku}</p>
                                </div>
                                <div className="cart__quantity" aria-label={`Количество: ${product.name}, ${size}`}>
                                    <button className="cart__step" type="button" aria-label="Уменьшить количество" onClick={() => changeQuantity(product.id, size, quantity - 1)}><Minus className="cart__step-icon" size={12} /></button>
                                    <span className="cart__quantity-value">{quantity}</span>
                                    <button className="cart__step" type="button" aria-label="Увеличить количество" disabled={quantity >= product.stock[size]} onClick={() => changeQuantity(product.id, size, quantity + 1)}><Plus className="cart__step-icon" size={12} /></button>
                                </div>
                                <p className="cart__price">{formatPrice(product.price * quantity)}</p>
                                <button className="cart__remove" type="button" aria-label={`Удалить ${product.name}, ${size}`} onClick={() => changeQuantity(product.id, size, 0)}><X className="cart__remove-icon" size={14} /></button>
                            </li>
                        ))}
                    </ul>
                    <div className="cart__total" aria-live="polite"><span className="cart__total-label">Сумма</span><span className="cart__total-value">{formatPrice(total)}</span></div>
                    <form className="cart__form" onSubmit={handleSubmit}>
                        <label className="cart__field">Имя<input name="customer_name" autoComplete="name" required maxLength={100} /></label>
                        <label className="cart__field">Телефон<input name="customer_phone" type="tel" autoComplete="tel" required maxLength={20} /></label>
                        <label className="cart__field">Город / способ получения (необязательно)<input name="delivery" autoComplete="address-level2" maxLength={200} /></label>
                        <label className="cart__field">Комментарий (необязательно)<input name="comment" maxLength={500} /></label>
                        <p className="cart__notice">Откроется WhatsApp с составом заказа. Нажмите «Отправить» в чате, чтобы магазин получил заявку. Наличие, доставка и оплата согласуются в переписке. Корзина сохранится.</p>
                        <p className="cart__notice">Перед отправкой ознакомьтесь с <Link to="/terms" onClick={closeCart}>условиями покупки</Link> и <Link to="/privacy" onClick={closeCart}>политикой конфиденциальности</Link>. Отправка заказа не списывает деньги.</p>
                        {contacts.isError && <p className="cart__notice" role="alert">Не удалось загрузить контакт магазина. <button type="button" onClick={() => void contacts.refetch()}>Повторить</button></p>}
                        {submitError && <p className="cart__notice" role="alert">{submitError}</p>}
                        <button className="cart__checkout" type="submit" disabled={contacts.isPending}>{contacts.isPending ? 'Загружаем контакты…' : 'Продолжить в WhatsApp'}</button>
                    </form>
                    <p className="cart__delivery-note"><Link to="/delivery" onClick={closeCart}>Доставка</Link> рассчитывается при подтверждении заказа.<br /><Link to="/payment" onClick={closeCart}>Оплата</Link> · <Link to="/returns" onClick={closeCart}>Возврат и обмен</Link></p>
                </>
            ) : (
                <div className="cart__empty">
                    <p className="cart__empty-title">Ваша корзина пока пуста</p>
                    <Link className="cart__checkout" to={paths.catalog} onClick={closeCart}>Перейти в каталог</Link>
                </div>
            )}
            <div className="cart__mobile-after">
                <section className="cart__recommendations" aria-labelledby="cart-recommendations-title">
                    <div className="cart__recommendations-heading"><h2 id="cart-recommendations-title">ВАМ МОЖЕТ ПОНРАВИТЬСЯ</h2><span>06</span></div>
                    <div className="cart__recommendations-grid">{products.slice(0, 6).map((product) => <ProductCard key={product.id} product={product} />)}</div>
                </section>
                <Footer shop />
            </div>
        </Modal>
    );
};
