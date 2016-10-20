import sys
import shutil
import argparse
from pathlib import Path
from string import Formatter
from collections import namedtuple

from tinytag import TinyTag


def get_tag(dirname):
    path = Path(dirname)
    child_dirs = []
    media_files = []
    errors = []
    MediaFile = namedtuple('MediaFile', ('path', 'tags'))
    DetectionError = namedtuple('DetectionError', ('path', 'exception'))
    if not path.is_dir:
        raise Exception('The path is not a directory')
    for child in path.iterdir():
        if child.is_dir():
            child_dirs.append(child)
            continue
        else:
            try:
                mf = MediaFile(child, TinyTag.get(str(child)))
                media_files.append(mf)
            except Exception as e:
                errors.append(DetectionError(child, e))
    if not media_files and child_dirs:
        print("No media files found in source dir, trying nested directory")
        return get_tag(child_dirs[0])
    return media_files, child_dirs, errors


def get_dest_dir_name(tags, template):
    fields = [i[1] for i in Formatter().parse(template)]
    found = dict.fromkeys(fields)
    for tag in tags:
        for f in fields:
            found[f] = getattr(tag, f, None)
            if all(found[f] for f in fields):
                break
    return Path(template.format_map(found))


def move(paths, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        print('{} -> {}'.format(path, dest_dir))
        shutil.move(str(path), str(dest_dir))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-S', dest='source', help='source dir',
                        required=True)
    parser.add_argument('--dest', '-D', dest='dest',
                        help='destination root (default: source parent)')
    parser.add_argument('-t', '--template', dest='template',
                        default='{artist}/{artist} - {year} - {album}',
                        help='destination dir template (default: "%(default)s")')
    args = parser.parse_args()
    media_files, child_dirs, errors = get_tag(args.source)
    dest_dir_name = get_dest_dir_name((mf.tags for mf in media_files), args.template)
    dest_root = Path(args.dest) if args.dest else Path(args.source).parent
    dest_dir = dest_root.joinpath(dest_dir_name)
    if not (media_files or errors):
        print("Nothing to move")
        sys.exit(1)
    if (not media_files) and errors:
        print("Unsuported media files?")
        sys.exit(1)
    print('"{}" -> "{}"'.format(args.source, dest_dir))
    print("\nFollowing media files will be moved:")
    for mf in media_files:
        print('  {}'.format(mf.path))
    if errors:
        print("\nOther files that will be moved:")
        for e in errors:
            print('  {}'.format(e.path))
    if child_dirs:
        print('\nFollowing child dirs will be left as is:')
        for child in child_dirs:
            print('  {}'.format(child))
    answer = input('Continue? (y/n) ')
    if answer.lower().strip() == 'y':
        move((mf.path for mf in media_files), dest_dir)
        move((e.path for e in errors), dest_dir)
        if len(list(Path(args.source).iterdir())):
            print()
            print("WARNING: {} is not empty".format(args.source))
        else:
            shutil.rmtree(args.source)
            print('{} removed'.format(args.source))


if __name__ == '__main__':
    main()
