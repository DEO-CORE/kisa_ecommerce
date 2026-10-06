import { CartDrawer } from '@/features/cart/CartDrawer';
import { Header, Footer } from '@widgets/index';
import { LoadingPage } from '@/pages';
import { Suspense } from 'react';
import { useAppLoading } from '@/shared/hooks/useAppLoading';
import { Outlet, useLocation } from 'react-router-dom';
import { paths } from '@/shared/constants/consts';
import { CookieBanner } from '@/features/cookies/CookieBanner';
import '../styles/editorial.scss';
import '../styles/responsive.scss';

export const Layout = () => {
    const { isLoading } = useAppLoading(800);
    const { pathname } = useLocation();
    const isHome = pathname === paths.main;
    const isEditorial = pathname === paths.about || pathname === paths.news;

    if (isLoading) {
        return <LoadingPage />;
    }

    return (
        <div className={`app${isEditorial ? ' app--editorial' : ''}`}>
            <Header />
            <main className={isHome || isEditorial ? 'main' : 'main container'}>
                <Suspense fallback={<LoadingPage />}>
                    <Outlet />
                </Suspense>
            </main>
            <Footer />
            <CartDrawer />
            <CookieBanner />
        </div>
    );
};
