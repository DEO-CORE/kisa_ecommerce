export interface InfoDocument { page_type: string; title: string; content: string; updated_at: string }
export interface StoreContacts { seller_name: string; country: string; registration_number: string; tax_id: string; legal_address: string; email: string; phone: string; address: string; telegram_url: string; work_hours: string }
export const documents = [
    { type: 'privacy', path: '/privacy', title: 'Политика конфиденциальности', label: 'Конфиденциальность' },
    { type: 'cookies', path: '/cookies', title: 'Политика cookie', label: 'Политика cookie' },
    { type: 'terms', path: '/terms', title: 'Условия покупки и использования', label: 'Условия покупки' },
    { type: 'delivery', path: '/delivery', title: 'Доставка', label: 'Доставка' },
    { type: 'payment', path: '/payment', title: 'Оплата', label: 'Оплата' },
    { type: 'returns', path: '/returns', title: 'Возврат и обмен', label: 'Возврат и обмен' },
    { type: 'contacts', path: '/contacts', title: 'Контакты и реквизиты', label: 'Контакты и реквизиты' },
    { type: 'documents', path: '/documents', title: 'Документы магазина', label: 'Документы' },
] as const;
export const isPublicEmail = (email?: string) => Boolean(email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email));
