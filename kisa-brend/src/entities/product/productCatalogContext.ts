import { createContext, useContext } from 'react';
import type { Product } from './products';

export interface ProductCatalogValue {
    products: Product[];
    isRemote: boolean;
    error: Error | null;
}

export const ProductCatalogContext = createContext<ProductCatalogValue | null>(null);

export const useProductCatalog = () => {
    const context = useContext(ProductCatalogContext);
    if (!context) throw new Error('useProductCatalog requires ProductCatalogProvider');
    return context;
};