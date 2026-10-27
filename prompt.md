# Khmer Legal Article Extraction — CSV Format

Read the uploaded Khmer legal document carefully and extract every law article.

Return **only CSV content**. Do not include Markdown code fences, JSON, explanations, or additional text.

## Extraction Rules

1. Preserve the original Khmer text exactly as much as possible.
2. Do not translate, summarize, rewrite, or omit any content.
3. Detect article headings such as `មាត្រា ១`, `មាត្រាទី ១`, and `Article 1`.
4. Each article continues until the next article heading.
5. Replace line breaks inside article text with spaces.
6. Preserve Khmer characters, punctuation, numbers, and symbols.
7. Keep articles in their original document order.
8. Do not invent missing articles or text.
9. Use empty CSV fields when information cannot be identified.
10. Extract every article, including long articles.
11. An article may continue across multiple pages. Continue its text until the next article heading, even when the page changes.
12. A 10-page upload is only a chunk of the document. Do not treat the beginning or end of a chunk as the beginning or end of an article.
13. If the first text in this chunk continues an article from an earlier chunk, use the same article number and mark `continues_from_previous_chunk` as `true`.
14. If the last article in this chunk continues into the next chunk, mark `continues_in_next_chunk` as `true`.

## Required CSV Columns

`article_number,article_title,article_text,continues_from_previous_chunk,continues_in_next_chunk`

## CSV Formatting Rules

- Include the header row exactly once.
- Use commas as delimiters.
- Enclose every field in double quotes.
- Escape double quotes inside fields by doubling them.
- Each article must occupy one logical CSV record.
- Do not include literal line breaks inside article fields.
- Do not add any content before or after the CSV.

## Expected Output

```csv
article_number,article_title,article_text,continues_from_previous_chunk,continues_in_next_chunk
"១","","មាត្រា ១ ខ្លឹមសារច្បាប់...","false","false"
"២","","មាត្រា ២ ខ្លឹមសារច្បាប់...","false","true"
"២","","អត្ថបទបន្តរបស់មាត្រា ២...","true","false"
```

If the document is too long to extract completely, do not claim the extraction is complete. Clearly report the limitation instead of silently omitting articles.

## Chunk-Merging Rule

After all chunks are extracted, merge consecutive rows with the same `article_number` in document order. Join their `article_text` values with a single space, keep the article title from the first row, and set the final continuation flags to `false`.
