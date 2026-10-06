import type { FC } from 'react';
import './homePage.scss';
import { useContent } from '@/shared/api/content';

export const HomePage: FC = () => {
    const main = useContent<{ slogan: string; hero_video_url: string | null }>('/about/main-page/');
    return (
        <div className="homePage">
            <section className="homePage__banner" aria-labelledby="collection-title">
                {main.data?.hero_video_url && <video src={main.data.hero_video_url} autoPlay muted loop playsInline style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover" }} />}
                <div className="container homePage__banner-content">
                    <h1 className="homePage__banner-title" id="collection-title">
                        {main.data?.slogan || "KISA"}
                    </h1>
                </div>
            </section>
        </div>
    )
}
