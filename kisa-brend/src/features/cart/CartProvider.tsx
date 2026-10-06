import { useEffect, useState, type ReactNode } from 'react';
import { sizes, type Product, type Size } from '@/entities/product/products';
import { useProductCatalog } from '@/entities/product/productCatalogContext';
import { CartContext, type CartItem } from './cartContext';

const storageKey = 'kisa-cart-v1';

const readCart = (): CartItem[] => {
    try {
        const saved: unknown = JSON.parse(localStorage.getItem(storageKey) ?? '[]');
        if (!Array.isArray(saved)) return [];
        return saved.flatMap((item) => {
            if (!item || typeof item.productId !== 'string' || !sizes.includes(item.size as Size)) return [];
            if (!Number.isInteger(item.quantity) || item.quantity < 1) return [];
            return [{ productId: item.productId, size: item.size as Size, quantity: item.quantity }];
        });
    } catch {
        return [];
    }
};

export const CartProvider = ({ children }: { children: ReactNode }) => {
    const { products } = useProductCatalog();
    const [items, setItems] = useState<CartItem[]>(readCart);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        try { localStorage.setItem(storageKey, JSON.stringify(items)); } catch { /* Cart still works without storage. */ }
    }, [items]);

    const addItem = (product: Product, size: Size) => {
        if (!product.stock[size]) return;
        setItems((current) => {
            const existing = current.find((item) => item.productId === product.id && item.size === size);
            return existing
                ? current.map((item) => item === existing ? { ...item, quantity: Math.min(item.quantity + 1, product.stock[size]) } : item)
                : [...current, { productId: product.id, size, quantity: 1 }];
        });
        setIsOpen(true);
    };

    const changeQuantity = (productId: string, size: Size, quantity: number) => {
        const stock = products.find((product) => product.id === productId)?.stock[size] ?? 0;
        setItems((current) => current
            .map((item) => item.productId === productId && item.size === size ? { ...item, quantity: Math.min(quantity, stock) } : item)
            .filter((item) => item.quantity > 0));
    };

    return (
        <CartContext.Provider value={{ items, isOpen, openCart: () => setIsOpen(true), closeCart: () => setIsOpen(false), addItem, changeQuantity, clearCart: () => setItems([]) }}>
            {children}
        </CartContext.Provider>
    );
};
