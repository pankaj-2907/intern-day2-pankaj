def chunk_document(document: dict, chunk_size: int = 300, chunk_overlap: int = 50) -> list[dict]:
    """
    Splits a document's content into smaller chunks while preserving source metadata.
    
    Args:
        document (dict): Dictionary containing 'id', 'title', and 'content'.
        chunk_size (int): Maximum character length per chunk.
        chunk_overlap (int): Number of overlapping characters between consecutive chunks.
        
    Returns:
        list[dict]: List of chunk dictionaries containing chunk_id, document_id, title, and content.
    """
    doc_id = document.get("id")
    title = document.get("title", "")
    content = document.get("content", "").strip()

    # Handle empty or invalid documents
    if not content:
        return []

    chunks = []
    start = 0
    content_length = len(content)
    chunk_counter = 1

    while start < content_length:
        end = start + chunk_size
        chunk_text = content[start:end].strip()

        if chunk_text:
            chunk_id = f"{doc_id}_chunk_{chunk_counter:03d}"
            chunks.append({
                "chunk_id": chunk_id,
                "document_id": doc_id,
                "title": title,
                "content": chunk_text
            })
            chunk_counter += 1

        # Move start pointer considering overlap
        if end >= content_length:
            break
        start += chunk_size - chunk_overlap

    return chunks