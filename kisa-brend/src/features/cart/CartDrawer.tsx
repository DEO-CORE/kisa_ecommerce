import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { Link, generatePath } from 'react-router-dom';
import { Minus, Plus, X } from 'lucide-react';
import { formatPrice } from '@/entities/product/products';
import { useProductCatalog } from '@/entities/product/productCatalogContext';
import { createOrder } from '@/entities/product/productApi';
import { paths } from '@/shared/constants/consts';
import { Modal } from '@/shared/ui/Modal';
import { useCart } from './cartContext';
import './cart.scss';
import { ProductCard } from '@/widgets/productCard/ProductCard';
import { Footer } from '@/widgets/footer/Footer';

export const CartDrawer = () => {
    const { items, isOpen, closeCart, changeQuantity, clearCart } = useCart();
    const { products } = useProductCatalog();
    const queryClient = useQueryClient();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState('');
    const [isOrderPlaced, setIsOrderPlaced] = useState(false);
    const [orderNumber, setOrderNumber] = useState('');
    const entries = items.flatMap((item) => {
        const product = products.find((candidate) => candidate.id === item.productId);
        return product ? [{ ...item, product }] : [];
    });
    const total = entries.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
    const handleClose = () => {
        closeCart();
        setIsOrderPlaced(false);
        setOrderNumber('');
        setSubmitError('');
    };
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (entries.some(({ product }) => !product.apiId || !product.colorId)) {
            setSubmitError('Каталог ещё не загружен. Попробуйте позже.');
            return;
        }
        const formData = new FormData(event.currentTarget);
        setIsSubmitting(true);
        setSubmitError('');
        try {
            const order = await createOrder({
                customer_name: String(formData.get('customer_name')),
                customer_phone: String(formData.get('customer_phone')),
                currency: 'KGS',
                items: entries.map(({ product, size, quantity }) => ({
                    product_id: product.apiId!,
                    color_id: product.colorId!,
                    size_name: size,
                    quantity,
                })),
            });
            clearCart();
            void queryClient.invalidateQueries({ queryKey: ["products"] });
            setOrderNumber(order.order_number ?? '');
            setIsOrderPlaced(true);
        } catch (error) {
            setSubmitError(error instanceof Error ? error.message : 'Не удалось отправить заказ. Попробуйте ещё раз.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Modal open={isOpen} onClose={handleClose} title="Ваш заказ" className="cart">
            <h2 className="cart__title">Ваш заказ:</h2>
            {isOrderPlaced ? (
                <div className="cart__success" role="status">
                    <p className="cart__success-title">Заказ принят</p>
                    {orderNumber && <p>Номер заказа: {orderNumber}</p>}
                    <button className="cart__checkout" type="button" onClick={handleClose}>Продолжить покупки</button>
                </div>
            ) : entries.length ? (
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
                        {submitError && <p className="cart__notice" role="alert">{submitError}</p>}
                        <button className="cart__checkout" type="submit" disabled={isSubmitting}>{isSubmitting ? 'Отправляем…' : 'Оформить заказ'}</button>
                    </form>
                    <p className="cart__delivery-note">Доставка рассчитывается после подтверждения заказа.<br />Безопасная оплата · Возврат в течение 14 дней</p>
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
