# mmv
This is a small script to create a nice directory structure for my music collection.

## Installation
Only python3.4+ is supported:
`pip3 install git+git://github.com/andriykohut/mmv`

## Usage
`mmv -S some-weird-dir -t '{artist}/{artist} - {year} - {album}'` will create
following directory structure based on tags:
`SomeArtist/SomeArtist - 2016 - SomeAlbum`
Type `mmv -h` for more help.
