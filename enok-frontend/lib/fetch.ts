export default async function fetchApi(url: string, init?: RequestInit) {
    const r = await fetch(process.env.NEXT_PUBLIC_API_BASE + url, {
        credentials: "include",
        ...init,
    });
     if (!r.ok) {
        throw {url, resp: r};
    }

    return await r.json();
}
