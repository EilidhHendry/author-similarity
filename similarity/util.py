import os

from similarity.models import Author, Text

def load_dir(input_dir):
    last_author = ''

    for current_dir, sub_dirs, files in os.walk(input_dir):
        if files:
            # loop through files in directory
            for text_file in files:

                # get the author name from the directory currently in
                # if the value differs from the last time (to avoid unnecessary database queries)
                current_author = os.path.split(current_dir)[-1]
                if current_author != last_author:

                    # check if author already in database and add if not
                    if not Author.objects.filter(name=current_author):
                        print 'Adding author to db: ', current_author
                        author = Author(name=current_author)
                        author.save()

                    print 'Author in db: ', current_author
                    author = Author.objects.get(name=current_author)

                    # get the file name and drop the extension
                    file_name = os.path.join(current_dir+'/'+text_file)
                    text_name = os.path.splitext(text_file)[0]
                    print file_name
                    print text_name

                    # check if text file already in db and avoid hidden files
                    if not text_name.startswith('.') and not Text.objects.filter(author=author, text_file=text_file):
                        print 'Adding text to db: ', text_name
                        text = Text(author=author, name=text_name, text_file=text_file)
                        text.save()

                    print 'Text in db: ', text_name

                last_author = current_author
