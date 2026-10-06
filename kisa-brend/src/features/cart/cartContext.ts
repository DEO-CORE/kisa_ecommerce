import { createContext, useContext } from 'react';
import type { Product, Size } from '@/entities/product/products';

export interface CartItem {
    productId: string;
    size: Size;
    quantity: number;
}

interface CartContextValue {
    items: CartItem[];
    isOpen: boolean;
    openCart: () => void;
    closeCart: () => void;
    addItem: (product: Product, size: Size) => void;
    changeQuantity: (productId: string, size: Size, quantity: number) => void;
    clearCart: () => void;
}

export const CartContext = createContext<CartContextValue | null>(null);
export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) throw new Error('useCart requires CartProvider');
    return context;
};
