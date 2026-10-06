import { CartProvider } from '@/features/cart/CartProvider';
import { RouterProvider } from 'react-router-dom';
import { router } from '@app/routes/router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProductCatalogProvider } from '@/entities/product/ProductCatalogProvider';
import '@app/styles/global.scss';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ProductCatalogProvider>
        <CartProvider><RouterProvider router={router} /></CartProvider>
      </ProductCatalogProvider>
    </QueryClientProvider>
  );
}

export default App;