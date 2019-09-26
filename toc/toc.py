import os
from glob import glob

from contingent.projectlib import Project
from contingent.io import looping_wait_on


project = Project()
task = project.task

@task
def read_text_file(path):
    with open(path) as f:
        return f.read()

@task
def filename_of(path):
    return str(path)

@task
def sorted_files(paths):
    return sorted(paths, key=filename_of)

@task
def filetype_of(path):
    return path[-3:]

@task
def source_of(path):
    return path[:-3] + 'txt'

@task
def parse(path):
    source = read_text_file(path)
    lines = source.splitlines()
    title = lines[0][4:-1]
    bullets = []
    line = 1
    flag = True
    if len(lines) == 1:
        flag = False
    while flag and line < len(lines):
        l = lines[line]
        if l[:3] == '`b:':
            bullets.append(lines[line][4:-1])
            line += 1
        else:
            flag = False
    body = ''
    lines = lines[line:]
    for line in lines:
        body += '\n' + line

    return {'title': title, 'bullets': bullets, 'body': body}

@task
def title_of(path):
    info = parse(path)
    return info['title'] + '\n'

@task
def bullets_of(path):
    info = parse(path)
    bullets = info['bullets']
    b = ''
    for bullet in bullets:
        b += '* ' + title_of(bullet) + '\n'
    return b

@task
def body_of(path):
    info = parse(path)
    return info['body']


@task
def render(path):
    if filetype_of(path) == 'out':
        source_path = source_of(path)
        title = title_of(source_path)
        bullets = bullets_of(source_path)
        body = body_of(source_path)
        text = '{}\n{}{}'.format(title, bullets, body)
        print(text)
        return text
    else:
        return read_text_file(path)


def main():
    thisdir = os.path.dirname(__file__)

    paths = tuple(glob(os.path.join(thisdir, '*.txt')) + glob(os.path.join(thisdir, '*.out')))

    print(paths)

    for path in sorted_files(paths):
        render(path)

    project.verbose = True

    count = 0

    while count < 1:
        count += 1
        print('=' * 72)
        print('Watching for files to change')
        changed_paths = looping_wait_on(paths)
        print('=' * 72)
        print('Reloading:', ' '.join(changed_paths))
        with project.cache_off():
            for path in changed_paths:
                read_text_file(path)
        project.rebuild()


if __name__ == '__main__':
    main()
