import os
try:
    import textract
except ImportError:
    pass

from similarity.models import Author, Text

def load_dir(input_dir):
    from django.core.files import File

    if not(input_dir): return None

    if ("~" in input_dir):
        input_dir = os.path.expanduser(input_dir)
    print "loading files in directory: %s" % (input_dir)

    last_author = ''
    for current_dir, sub_dirs, files in os.walk(input_dir):
        if files:
            # get the author name from the directory currently in
            # if the value differs from the last time (to avoid unnecessary database queries)
            current_author = os.path.split(current_dir)[-1]
            if current_author != last_author:

                # check if author already in database and add if not
                author = None
                authors = Author.objects.filter(name=current_author)
                if len(authors) > 0: author = authors[0]
                if not(author):
                    print 'Adding author to db: ', current_author
                    author = Author(name=current_author)
                    author.save()
                else:
                    print "Author exists: ", current_author

            for text_file in files:
                text_name = os.path.splitext(text_file)[0]  # drop the extension
                if (text_name.startswith('.')): continue


                # get the file name and
                # pass text file to text extraction to convert if epub
                file_name = os.path.join(current_dir+'/'+text_file)
                processed_text_path = process_text_file(file_name)
                if not(processed_text_path): continue

                text_file_txt = File(open(processed_text_path))
                # check if text file already in db and avoid hidden files
                if not(Text.objects.filter(author=author, text_file=text_file_txt)):
                    print 'Adding text to db: ', text_name
                    text = Text(author=author, name=text_name, text_file=text_file_txt)
                    text.save()
                else:
                    print "Text exists, or is hidden: ", text_name

            last_author = current_author

def process_text_file(file_path):
    file_name, extension = os.path.splitext(file_path)
    print file_name, extension
    if (extension == ".txt"):
        return file_path
    elif (extension == '.epub'):
        print "Trying epub"
        try:
            text = textract.process(file_path)
            print "Processed epub: ", file_path
            output_path = file_name+'.txt'
            output_file = open(output_path, 'w')
            output_file.write(text)
            print "Converted epub: ", output_path
            return output_path
        except Exception as error:
            # TODO: textract raises own error so none isn't returned on try failure
            print error
            print 'Failed to convert epub: ', file_path
            return None
    elif (extension == ""):
        text_content = None
        try:
            with open(file_path) as input_file:
                text_content = input_file.read()
                if text_content:
                    print "Managed to read file: ", file_path
                    return file_path
        except IOError:
            print "Failed to read file: ", file_path
            return None
    else:
        print 'Unsupported file type: ', file_path
        return None
