def create_templates_from_file(filename, separator):
    templates = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() != '' and not line.startswith('#'):
                name, template, code = line.strip().split(separator)
                templates[name] = [template, int(code)]
    return templates