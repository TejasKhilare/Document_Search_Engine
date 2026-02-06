export async function fetchDocuments() {
  const response = await fetch("http://127.0.0.1:8000/documents");
  if (!response.ok) {
    throw new Error("Failed to fetch documents");
  }
  return response.json();
}

export async function deleteDocument(docId) {
  const response = await fetch(
    `http://127.0.0.1:8000/documents/${docId}`,
    { method: "DELETE" }
  );

  if (!response.ok) {
    throw new Error("Delete failed");
  }

  return response.json();
}
