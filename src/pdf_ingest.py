import io, re
import pymupdf

def is_heading(line):
    s = " ".join(line.split()).strip()
    if not s or len(s) > 150: return False
    if re.match(r"^(CHAPTER\s+[\w.-]+|PART\s+[A-Z0-9IVX]+)", s, re.I): return True
    if re.match(r"^(?:\d+\.){0,4}\d+\s+[A-Z]", s): return True
    letters = [c for c in s if c.isalpha()]
    return len(letters) > 5 and sum(c.isupper() for c in letters) / len(letters) > .82

def ingest_pdf_bytes(data, filename, max_chars=2200, overlap=220):
    doc = pymupdf.open(stream=io.BytesIO(data), filetype="pdf")
    chunks, section, buf, pages = [], "", [], []
    def flush():
        nonlocal buf, pages
        txt = "\n".join(buf).strip()
        if txt:
            chunks.append({"source": filename, "page_start": min(pages), "page_end": max(pages),
                           "section": section, "text": f"Source: {filename}\nSection context: {section or 'Not detected'}\n\n{txt}"})
        buf, pages = [], []
    for pno, page in enumerate(doc, 1):
        for raw in page.get_text("text", sort=True).splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if not line: continue
            if is_heading(line):
                flush()
                section = line
            if buf and sum(map(len, buf)) + len(line) > max_chars:
                old, oldpage = "\n".join(buf), pages[-1]
                flush()
                buf, pages = [old[-overlap:]], [oldpage]
            buf.append(line); pages.append(pno)
    flush()
    doc.close()
    return chunks

def search_chunks(query, chunks, limit=6):
    terms = [x.lower() for x in re.findall(r"\w+", query) if len(x) > 2]
    ranked = []
    for c in chunks:
        txt = c["text"].lower()
        score = sum(txt.count(t) for t in terms)
        if score: ranked.append((score, c))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in ranked[:limit]]
