"""Small exact source excerpts; never synthesize a quote."""
import json


def document_bounds(text):
    bounds={}
    decoder=json.JSONDecoder()
    def skip(pos):
        while pos<len(text) and text[pos].isspace():pos+=1
        return pos
    def walk(pos,path):
        pos=skip(pos);start=pos
        if text[pos]=='{':
            pos=skip(pos+1)
            while text[pos]!='}':
                key,end=decoder.raw_decode(text,pos);pos=walk(skip(end)+1,path+(str(key),));pos=skip(pos)
                if text[pos]!=',':break
                pos=skip(pos+1)
            pos+=1
        elif text[pos]=='[':
            pos=skip(pos+1);n=0
            while text[pos]!=']':
                pos=skip(walk(pos,path+(str(n),)));n+=1
                if text[pos]!=',':break
                pos=skip(pos+1)
            pos+=1
        else:_,pos=decoder.raw_decode(text,pos)
        bounds[path]=(start,pos)
        return pos
    try:walk(0,())
    except (ValueError,IndexError,TypeError):return {}
    return bounds


def pointer_bounds(text, pointer, bounds=None):
    if not pointer.startswith("/") or "*" in pointer:
        return None
    wanted = tuple(p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/")[1:])
    if bounds is not None:return bounds.get(wanted)
    decoder = json.JSONDecoder()
    result = None
    def skip(pos):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        return pos
    def walk(pos, path):
        nonlocal result
        pos = skip(pos)
        start = pos
        if text[pos] == "{":
            pos = skip(pos + 1)
            while text[pos] != "}":
                key, end = decoder.raw_decode(text, pos)
                pos = skip(end)
                pos = walk(pos + 1, path + (str(key),))
                pos = skip(pos)
                if text[pos] == ",":
                    pos = skip(pos + 1)
                else:
                    break
            pos += 1
        elif text[pos] == "[":
            pos, index = skip(pos + 1), 0
            while text[pos] != "]":
                pos = walk(pos, path + (str(index),))
                index += 1
                pos = skip(pos)
                if text[pos] == ",":
                    pos = skip(pos + 1)
                else:
                    break
            pos += 1
        else:
            _, pos = decoder.raw_decode(text, pos)
        if path == wanted:
            result = (start, pos)
        return pos
    try:
        walk(0, ())
    except (ValueError, IndexError, TypeError):
        return None
    return result


def excerpt(body: bytes, value=None, locator="", limit=300,document=None):
    text = document[0] if document else body.decode("utf-8", errors="replace")
    bounds = pointer_bounds(text, locator,document[1] if document else None) if text.lstrip().startswith(("{", "[")) else None
    if bounds:
        start, end = bounds
        if end - start > limit:
            return text[start:start + limit]
        start = max(0, start - min(50, limit - (end - start)))
        return text[start:start + limit]
    # CSV snapshots consist of their header and one exact record. Search only
    # the record, never a numeric suffix in a column name.
    offset = text.find("\n") + 1 if locator.startswith("row:") else 0
    tokens = []
    def visit(v):
        if isinstance(v, dict):
            for key in ("name", "navn", "kode", "adresse", "role_type"):
                if key in v:
                    visit(v[key])
            for item in v.values():
                visit(item)
        elif isinstance(v, list):
            for item in v:
                visit(item)
        elif v is not None:
            tokens.extend([str(v), json.dumps(v, ensure_ascii=False), json.dumps(v, ensure_ascii=True)])
    visit(value)
    for token in tokens:
        index = text.find(token, offset)
        if index >= 0 and len(token) <= limit:
            start = max(offset, index - min(60, limit - len(token)))
            return text[start:start + limit]
    # Absence/compound values may need an item locator rather than a literal
    # normalized value. The excerpt still comes verbatim from source bytes.
    key = locator.rstrip("/").split("/")[-1].replace("column:", "")
    index = max(0, text.find(key))
    return text[max(0, index - 40):max(0, index - 40) + limit]
