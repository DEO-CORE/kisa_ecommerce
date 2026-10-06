type Entry = {
    product: { id: string; name: string; sku: string; color: string; price: number };
    size: string;
    quantity: number;
};

export function buildWhatsAppUrl(phone: string, entries: Entry[], customer: {
    name: string; phone: string; delivery: string; comment: string;
}, origin: string): string {
    const recipient = phone.replace(/[\s()+-]/g, '');
    if (!/^[1-9]\d{7,14}$/.test(recipient)) throw new Error('Номер WhatsApp магазина пока недоступен. Обратитесь через страницу «Контакты».');
    if (!entries.length || !customer.name || !customer.phone) throw new Error('Укажите имя, телефон и добавьте товары в корзину.');
    const money = (value: number) => `${new Intl.NumberFormat('ru-RU').format(value)} сом (KGS)`;
    const lines = ['Здравствуйте! Хочу оформить заказ в KISA.', '', `Имя: ${customer.name}`, `Телефон: ${customer.phone}`];
    if (customer.delivery) lines.push(`Город / получение: ${customer.delivery}`);
    lines.push('', 'Состав заказа:');
    entries.forEach(({ product, size, quantity }, index) => {
        lines.push('', `${index + 1}. ${product.name}`, `Артикул: ${product.sku}`, `Цвет: ${product.color} · Размер: ${size}`, `Количество: ${quantity} × ${money(product.price)} = ${money(product.price * quantity)}`, `${origin}/catalog/${encodeURIComponent(product.id)}`);
    });
    lines.push('', `Итого за товары: ${money(entries.reduce((sum, entry) => sum + entry.product.price * entry.quantity, 0))}`, 'Доставка рассчитывается отдельно. Прошу подтвердить наличие и условия оплаты.');
    if (customer.comment) lines.push('', `Комментарий: ${customer.comment}`);
    return `https://wa.me/${recipient}?text=${encodeURIComponent(lines.join('\n'))}`;
}
