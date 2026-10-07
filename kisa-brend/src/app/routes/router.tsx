import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../layouts/Layout";
import { paths } from '@shared/constants/consts';
import { InfoPage } from '@/pages/info/InfoPage';
import { documents } from '@/pages/info/documents';
import {
    HomePage,
    AboutPage,
    ErrorPage,
    LoadingPage,
    CatalogPage,
    DetailCatalogPage,
    NewsPage,
} from "@pages/index";

export const router = createBrowserRouter([
    { path: "*", element: <ErrorPage notFound /> },
    {
        path: '/',
        element: <Layout />,
        errorElement: <ErrorPage />,
        children: [
            ...documents.map(document => ({ path: document.path, element: <InfoPage pageType={document.type} /> })),
            { path: paths.main, element: <HomePage /> },
            { path: paths.loading, element: <LoadingPage /> },
            { path: paths.about, element: <AboutPage /> },
            { path: paths.catalog, element: <CatalogPage /> },
            { path: paths.catalogDetail, element: <DetailCatalogPage /> },
            { path: paths.news, element: <NewsPage /> },
        ],
    },
]);
