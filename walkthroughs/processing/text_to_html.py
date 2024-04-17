import re

input_file = 'Slider Walkthrough.txt'
output_file = 'slider_walkthrough_out.txt'

file_in = open(input_file, 'r', encoding="utf8")
file_out = open(output_file, 'w')

is_in_code_block = False
MAX_FOLDOUTS = 3
is_in_foldout = dict([(i, False) for i in range(1, MAX_FOLDOUTS + 1)])

indent_level = 0

SECTION_START = '''<div class="row animate-box">\n\t<div class="col-md-8 col-md-offset-2">'''
SECTION_END = '''\t</div>\n</div>\n'''

HTML_SPOILER_START = '<span class="spoiler">'
HTML_SPOILER_END = '</span>'

def indent():
    global indent_level

    return '\t' * indent_level

def unindent():
    global indent_level

    indent_level -= 1
    return '\t' * indent_level

def new_line():
    return '\n' + indent()

def new_line_indent():
    global indent_level

    indent_level += 1
    return new_line()

def new_line_unindent():
    global indent_level

    indent_level -= 1
    return new_line()

def start_foldout(file_out, level):
    global indent_level, SECTION_START

    if level == 1:
        indent_level += 2
        file_out.write(SECTION_START + new_line())

    file_out.write(new_line() + '<details>' + new_line_indent())

def end_foldout(file_out, level):
    global indent_level, SECTION_END

    file_out.write(new_line_unindent() + '</details>' + new_line())

    if level == 1:
        indent_level -= 1
        file_out.write(new_line_unindent() + SECTION_END + new_line())

def try_close_foldouts(file_out, end_level):
    global MAX_FOLDOUTS, is_in_foldout
    
    for i in range(MAX_FOLDOUTS, end_level - 1, -1):
        if is_in_foldout[i]:
            is_in_foldout[i] = False
            end_foldout(file_out, i)






for line in file_in.readlines():
    if len(line.strip()) == 0:
        continue
    
    if is_in_code_block:
        if re.search('```', line):
            is_in_code_block = False
            continue

        file_out.write(line)
        continue
        

    # Comment
    # if re.search('^\[\/\/\]: #', line):
    if re.search('\[\/\/\]: #', line):
        continue

    # Generated new-page breaks
    if re.search('^________________', line):
        continue

    # Generated document comments
    if re.search('^\[[a-z]\]', line):
        continue

    # Code blocks
    if re.search('```', line):
        is_in_code_block = not is_in_code_block
        continue

    # Code segments don't really matter for now I dont think
    line = re.sub('`', '', line)

    # Foldouts
    foldout_match = re.search('^#{1,3} ', line)
    if foldout_match:
        foldout_level = foldout_match.group().count('#')
        line = line[foldout_match.span()[1]:]

        # Force exit foldout
        if line.strip() == '[END]':
            if is_in_foldout[foldout_level]:
                is_in_foldout[foldout_level] = False
                end_foldout(file_out, foldout_level)
                continue
            else:
                print('Force ended foldout', foldout_level, 'when I wasn\'t in one.')
                continue

        try_close_foldouts(file_out, foldout_level)
        
        is_in_foldout[foldout_level] = True
        start_foldout(file_out, foldout_level)
        # <summary class="header-2">Slider 2</summary>
        line = '<summary class="header-%i">%s</summary>\n' % (foldout_level, line.strip())
        file_out.write(line)
        continue

    # p tag
    line = new_line() + '<p>' + new_line_indent() + line

    # Spoiler
    while re.search('.*\|\|.+\|\|.*', line):
        line = re.sub('\|\|', new_line() + HTML_SPOILER_START + new_line_indent(), line, 1)
        line = re.sub('\|\|', new_line_unindent() + HTML_SPOILER_END, line, 1)
    
    line =  line + unindent() + '</p>'
    
    file_out.write(line)

try_close_foldouts(file_out, 1)

file_in.close()