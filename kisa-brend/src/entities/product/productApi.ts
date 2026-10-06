import type { Category, Product, Size } from './products';

const apiBase = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '');

interface ApiPage<T> {
    next: string | null;
    results: T[];
}

interface ApiColor {
    id: number;
    name: string;
    slug: string;
    hex_code: string;
}

interface ApiStock {
    size: { name: string };
    color: ApiColor;
    quantity: number;
    available: number;
    is_out_of_stock: boolean;
}

interface ApiProductListItem {
    id: number;
    name: string;
    slug: string;
    drop: { name: string; slug: string } | null;
    price_rub: string;
    price_kgs: string;
    main_image_url: string | null;
    colors: ApiColor[];
    is_new: boolean;
    total_stock: number;
}

interface ApiProductDetail extends Omit<ApiProductListItem, 'colors'> {
    description: string;
    composition: string;
    fit_recommendation: string;
    main_image: string | null;
    stocks: ApiStock[];
    colors: Array<{ color: ApiColor; images?: Array<{ image: string }> }>;
}

const request = async <T>(path: string): Promise<T> => {
    const response = await fetch(`${apiBase}${path}`);
    if (!response.ok) throw new Error(`API вернул ${response.status}`);
    return response.json() as Promise<T>;
};

const getPaginated = async <T>(path: string): Promise<T[]> => {
    const results: T[] = [];
    let page = 1;
    let hasNext = true;

    while (hasNext) {
        const data = await request<ApiPage<T>>(`${path}?page=${page}`);
        results.push(...data.results);
        hasNext = Boolean(data.next);
        page += 1;
    }

    return results;
};

const getCategory = (name: string, dropName: string | undefined): Category => {
    const value = `${name} ${dropName ?? ''}`.toLocaleLowerCase('ru');
    if (value.includes('худи') || value.includes('hoodie')) return 'Худи';
    if (value.includes('брюк') || value.includes('pants')) return 'Брюки';
    return 'Футболки';
};

const imageUrl = (value: string | null | undefined) => {
    if (!value) return '';
    if (/^https?:\/\//.test(value)) return value;
    return `${apiBase.replace(/\/api$/, '')}${value.startsWith('/') ? '' : '/'}${value}`;
};

const toProduct = (source: ApiProductDetail, color: ApiColor): Product => {
    const stocks = source.stocks.filter((stock) => stock.color.id === color.id);
    const stock = Object.fromEntries(
        (['XS', 'S', 'M', 'L', 'XL'] as Size[]).map((size) => {
            const row = stocks.find((item) => item.size.name === size);
            return [size, row && !row.is_out_of_stock ? row.available : 0];
        }),
    ) as Record<Size, number>;
    const category = getCategory(source.name, source.drop?.name);
    const colorImages = source.colors.find((item) => item.color.id === color.id)?.images;
    const mainImage = colorImages?.[0]?.image ?? source.main_image ?? source.main_image_url;
    const sizeChartName = category === 'Худи' ? 'hoodie-grey' : category === 'Брюки' ? 'pants-grey' : 'tee-cream';

    return {
        id: `${source.slug}--${color.slug}`,
        apiId: source.id,
        colorId: color.id,
        name: source.name,
        category,
        collection: source.drop ?? undefined,
        price: Number(source.price_kgs),
        color: color.name,
        colorLabel: color.name.toLocaleUpperCase('ru'),
        swatch: color.hex_code || '#c9c9c5',
        image: imageUrl(mainImage) || `/images/products/${sizeChartName}.png`,
        sizeChart: `/images/products/${sizeChartName}-sizes.png`,
        sku: source.slug,
        isNew: source.is_new,
        stock,
        description: source.description,
        composition: source.composition,
        fit: source.fit_recommendation,
    };
};

export const getProducts = async (): Promise<Product[]> => {
    const list = await getPaginated<ApiProductListItem>('/catalog/products/');
    const details = await Promise.all(list.map((product) =>
        request<ApiProductDetail>(`/catalog/products/${encodeURIComponent(product.slug)}/`),
    ));

    return details.flatMap((product) => {
        const colors = product.stocks.map((stock) => stock.color)
            .filter((color, index, all) => all.findIndex((item) => item.id === color.id) === index);
        const availableColors = colors.length ? colors : product.colors.map((item) => item.color);
        return availableColors.map((color) => toProduct(product, color));
    });
};

export interface CreateOrderPayload {
    customer_name: string;
    customer_phone: string;
    currency: 'KGS';
    items: Array<{
        product_id: number;
        color_id: number;
        size_name: string;
        quantity: number;
    }>;
}

export const createOrder = async (payload: CreateOrderPayload) => {
    const response = await fetch(`${apiBase}/orders/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
    if (!response.ok) {
        const errors = await response.json().catch(() => null) as Record<string, unknown> | null;
        const message = errors ? Object.values(errors).flat().filter(value => typeof value === 'string').join(' ') : '';
        throw new Error(message || 'Не удалось оформить заказ. Проверьте данные и попробуйте ещё раз.');
    }
    return response.json() as Promise<{ order_number?: string }>;
};
