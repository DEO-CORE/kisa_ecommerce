export const sizes = ['XS', 'S', 'M', 'L', 'XL'] as const;
export type Size = typeof sizes[number];
export type Category = 'Худи' | 'Брюки' | 'Футболки';

export interface Product {
    id: string;
    apiId?: number;
    colorId?: number;
    name: string;
    category: Category;
    collection?: { slug: string; name: string };
    price: number;
    color: string;
    colorLabel: string;
    swatch: string;
    image: string;
    sizeChart: string;
    sku: string;
    isNew: boolean;
    stock: Record<Size, number>;
    description: string;
    composition: string;
    fit: string;
}

const descriptions: Record<Category, Pick<Product, 'description' | 'composition' | 'fit'>> = {
    'Худи': {
        description: 'Укороченное худи свободного силуэта из плотного хлопка. Объёмный капюшон, металлическая молния и вышитый логотип на груди.',
        composition: '100% хлопок, 420 г/м². Деликатная стирка при 30°C.',
        fit: 'Модель ростом 178 см носит размер S. Свободная посадка.',
    },
    'Брюки': {
        description: 'Брюки свободного силуэта с эластичным поясом и небольшим логотипом. Для повседневных образов и сочетаний с любимым худи.',
        composition: 'Хлопок. Деликатная стирка при 30°C.',
        fit: 'Свободная посадка. Выбирайте размер по таблице замеров.',
    },
    'Футболки': {
        description: 'Тру-фит футболка From Abusers с фирменным принтом. Лаконичная основа повседневного образа.',
        composition: 'Деликатная стирка при 30°C. Стирать с вещами похожих цветов.',
        fit: 'Прилегающий силуэт. Выбирайте размер по таблице замеров.',
    },
};

const createProduct = (
    id: string, category: Category, color: string, colorLabel: string, swatch: string, isNew = false,
): Product => ({
    id, category, color, colorLabel, swatch, isNew,
    name: category === 'Худи' ? 'Зип-худи From Abusers' : category === 'Брюки' ? 'Брюки Smile' : 'Тру-фит футболка From Abusers',
    price: category === 'Худи' ? 11990 : category === 'Брюки' ? 8990 : 3990,
    image: `/images/products/${id}.png`,
    sizeChart: `/images/products/${category === 'Худи' ? 'hoodie-grey' : category === 'Брюки' ? 'pants-grey' : 'tee-cream'}-sizes.png`,
    sku: `AAC/SS26/${category === 'Худи' ? 'ZH/FMA' : category === 'Брюки' ? 'PN/SM' : 'TFS/FMA'}/${colorLabel.replaceAll(' ', '-')}`,
    stock: { XS: category === 'Худи' ? 0 : 2, S: 5, M: 3, L: 4, XL: 2 },
    ...descriptions[category],
});

// Local catalogue for the supplied mockups; connect inventory here when the API is ready.
export const products: Product[] = [
    createProduct('hoodie-grey', 'Худи', 'Серый меланж', 'GREY MELANGE', '#c9c9c5', true),
    createProduct('hoodie-red', 'Худи', 'Красный', 'RED', '#ad1936'),
    createProduct('hoodie-black', 'Худи', 'Чёрный', 'BLACK', '#0c0c0c'),
    createProduct('pants-grey', 'Брюки', 'Серый меланж', 'GREY MELANGE', '#c9c9c5', true),
    createProduct('tee-cream', 'Футболки', 'Кремовый', 'CREAM', '#f1eee5'),
    createProduct('tee-pink', 'Футболки', 'Розовый', 'PINK', '#e9bacb'),
    createProduct('tee-burgundy', 'Футболки', 'Бордовый', 'BURGUNDY', '#61202e'),
    createProduct('tee-red', 'Футболки', 'Красный', 'RED', '#ad1936'),
    createProduct('pants-black', 'Брюки', 'Чёрный', 'BLACK', '#0c0c0c'),
];

// The mockup repeats the first four products in three rows.
export const catalogProducts = [
    ...products.slice(0, 4), ...products.slice(0, 4), ...products.slice(0, 4),
    ...products.slice(4, 8), ...products.slice(0, 4),
];
export const findProduct = (id: string | undefined) => products.find((product) => product.id === id);
export const formatPrice = (price: number) => `${new Intl.NumberFormat('ru-RU').format(price)} сом`;
