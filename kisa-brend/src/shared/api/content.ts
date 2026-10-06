import { useQuery } from '@tanstack/react-query';
const base = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '');
export async function readApi<T>(path: string): Promise<T> {
    const response = await fetch(`${base}${path}`);
    if (!response.ok) throw new Error('Не удалось загрузить данные. Попробуйте позже.');
    return response.json();
}
export function useContent<T>(path: string) {
    return useQuery({ queryKey: ['content', path], queryFn: () => readApi<T>(path) });
}
export function useList<T>(path: string) {
    return useQuery({ queryKey: ['content', path], queryFn: async () => {
        const rows: T[] = [];
        let page = 1;
        while (true) {
            const data = await readApi<{ results: T[]; next: string | null }>(`${path}?page=${page}`);
            rows.push(...data.results);
            if (!data.next) return rows;
            page++;
        }
    }});
}

export async function subscribe(email: string): Promise<string> {
    const response = await fetch(`${base}/newsletter/subscribe/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email }),
    });
    if (!response.ok) throw new Error('Не удалось подписаться. Проверьте email и попробуйте позже.');
    const data = await response.json() as { message: string };
    return data.message;
}
