export async function searchDocuments(query) {
    const response=await fetch(
        `http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) {
    throw new Error("Search failed");
  }
  const data = await response.json(); // ✅ read ONCE
  console.log(data);
  return data;
}