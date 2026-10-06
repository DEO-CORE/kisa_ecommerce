import type { ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getProducts } from './productApi';
import { ProductCatalogContext } from './productCatalogContext';

export const ProductCatalogProvider = ({ children }: { children: ReactNode }) => {
    const query = useQuery({
        queryKey: ['products'],
        queryFn: getProducts,
        staleTime: 0,
        retry: 1,
    });

    return (
        <ProductCatalogContext.Provider value={{
            products: query.data ?? [],
            isRemote: query.isFetched && !query.error,
            error: query.error,
        }}>
            {children}
        </ProductCatalogContext.Provider>
    );
};