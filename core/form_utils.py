def lines_to_list(text):
    return [line.strip() for line in (text or '').splitlines() if line.strip()]


def list_to_lines(items):
    return '\n'.join(items or [])
