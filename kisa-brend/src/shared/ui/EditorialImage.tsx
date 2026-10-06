interface EditorialImageProps {
    name: string;
    alt: string;
    className?: string;
    width: number;
    height: number;
    loading?: 'lazy' | 'eager';
}

export const EditorialImage = ({ name, alt, className, width, height, loading }: EditorialImageProps) => (
    <picture className={className}>
        <source media="(max-width: 640px)" srcSet={`/images/editorial/${name}-mobile.png`} />
        <source media="(max-width: 1100px)" srcSet={`/images/editorial/${name}-tablet.png`} />
        <img src={`/images/editorial/${name}.png`} alt={alt} width={width} height={height} loading={loading} />
    </picture>
);
