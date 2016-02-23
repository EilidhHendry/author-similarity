from django.db import models

import classifier.constants
import classifier.clean_up
import classifier.chunk
import classifier.compute_fingerprint
import classifier.svm
from classifier.util import generate_directory_name


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % (self.name)


def create_text_preprocessed_path(self, filename=""):
    author_name = generate_directory_name(self.author.name)
    text_name = generate_directory_name(self.name)
    path = classifier.constants.PREPROCESSED_PATH + "/".join([author_name, text_name])
    return path

def create_text_upload_path(self, filename):
    author_name = generate_directory_name(self.author.name)
    text_name = generate_directory_name(self.name)
    path = classifier.constants.PLAINTEXT_PATH + "/".join([author_name, text_name])
    return path

class Text(models.Model):
    author = models.ForeignKey('Author')

    name = models.CharField(max_length=200)
    text_file = models.FileField(upload_to=create_text_upload_path, default=None, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        super(Text, self).save(*args, **kwargs)

        classifier.clean_up.clean_file(self.text_file.path, self.author.name, self.name)
        cleaned_text_path = create_text_preprocessed_path(self)
        classifier.chunk.chunk_text(cleaned_text_path, self.author.name, self.name)

        text_chunks_path = classifier.chunk.generate_chunk_path(self.author.name, self.name)
        fingerprints = classifier.compute_fingerprint.compute_all_fingerprints(text_chunks_path)
        for (chunk_number, fingerprint) in enumerate(fingerprints):
            theChunk = Chunk.create(self, chunk_number, fingerprint)
            theChunk.save()


def create_chunk_upload_path(self, filename=""):
    author_name = generate_directory_name(self.author.name)
    text_name = generate_directory_name(self.text.name)
    chunk_number = "{0:04d}.txt".format(self.text_chunk_number)
    path = classifier.constants.CHUNKS_PATH + "/".join([author_name, text_name, chunk_number])
    return path

class Chunk(models.Model):
    author = models.ForeignKey('Author')

    text = models.ForeignKey('Text')
    text_chunk_number = models.IntegerField(null=True)
    chunk_file = models.FileField(upload_to=create_chunk_upload_path, default=None, null=True, blank=True)

    def __unicode__(self):
        return u'%s (%i)' % (self.text, self.text_chunk_number)

    @classmethod
    def create(cls, text, chunk_number, fingerprint):
        chunk = cls(author=text.author, text=text, text_chunk_number=chunk_number)
        # set fingerprint, skip author column
        for key in fingerprint.keys():
            setattr(chunk, key, fingerprint[key])
        # set the FileField programatically, as it already exists on filesystem
        path = create_chunk_upload_path(chunk)
        chunk.chunk_file.name = path
        return chunk

    def get_fingerprint(self):
        fields = []
        for (field_index, field_name) in enumerate(classifier.constants.CHUNK_MODEL_FINGERPRINT_FIELDS):
            fields.append(getattr(self, field_name))
        return fields

    # fingerprint
    avg_word_length     = models.FloatField(null=True, blank=True)
    avg_sentence_length = models.FloatField(null=True, blank=True)
    lexical_diversity   = models.FloatField(null=True, blank=True)
    percentage_punctuation  = models.FloatField(null=True, blank=True)
    avg_word_length_syllables = models.FloatField(null=True, blank=True)

    # Function Words frequencies
    the_relative_frequency     = models.FloatField(null=True, blank=True)
    and_relative_frequency     = models.FloatField(null=True, blank=True)
    of_relative_frequency      = models.FloatField(null=True, blank=True)
    a_relative_frequency       = models.FloatField(null=True, blank=True)
    to_relative_frequency      = models.FloatField(null=True, blank=True)
    in_relative_frequency      = models.FloatField(null=True, blank=True)
    i_relative_frequency       = models.FloatField(null=True, blank=True)
    he_relative_frequency      = models.FloatField(null=True, blank=True)
    it_relative_frequency      = models.FloatField(null=True, blank=True)
    that_relative_frequency    = models.FloatField(null=True, blank=True)
    you_relative_frequency     = models.FloatField(null=True, blank=True)
    his_relative_frequency     = models.FloatField(null=True, blank=True)
    with_relative_frequency    = models.FloatField(null=True, blank=True)
    on_relative_frequency      = models.FloatField(null=True, blank=True)
    for_relative_frequency     = models.FloatField(null=True, blank=True)
    at_relative_frequency      = models.FloatField(null=True, blank=True)
    as_relative_frequency      = models.FloatField(null=True, blank=True)
    but_relative_frequency     = models.FloatField(null=True, blank=True)
    her_relative_frequency     = models.FloatField(null=True, blank=True)
    they_relative_frequency    = models.FloatField(null=True, blank=True)
    she_relative_frequency     = models.FloatField(null=True, blank=True)
    him_relative_frequency     = models.FloatField(null=True, blank=True)
    all_relative_frequency     = models.FloatField(null=True, blank=True)
    this_relative_frequency    = models.FloatField(null=True, blank=True)
    we_relative_frequency      = models.FloatField(null=True, blank=True)
    from_relative_frequency    = models.FloatField(null=True, blank=True)
    or_relative_frequency      = models.FloatField(null=True, blank=True)
    out_relative_frequency     = models.FloatField(null=True, blank=True)
    an_relative_frequency      = models.FloatField(null=True, blank=True)
    my_relative_frequency      = models.FloatField(null=True, blank=True)
    by_relative_frequency      = models.FloatField(null=True, blank=True)
    up_relative_frequency      = models.FloatField(null=True, blank=True)
    what_relative_frequency    = models.FloatField(null=True, blank=True)
    me_relative_frequency      = models.FloatField(null=True, blank=True)
    no_relative_frequency      = models.FloatField(null=True, blank=True)
    like_relative_frequency    = models.FloatField(null=True, blank=True)
    would_relative_frequency   = models.FloatField(null=True, blank=True)
    if_relative_frequency      = models.FloatField(null=True, blank=True)
    about_relative_frequency   = models.FloatField(null=True, blank=True)
    which_relative_frequency   = models.FloatField(null=True, blank=True)
    them_relative_frequency    = models.FloatField(null=True, blank=True)
    into_relative_frequency    = models.FloatField(null=True, blank=True)
    who_relative_frequency     = models.FloatField(null=True, blank=True)
    could_relative_frequency   = models.FloatField(null=True, blank=True)
    can_relative_frequency     = models.FloatField(null=True, blank=True)
    some_relative_frequency    = models.FloatField(null=True, blank=True)
    their_relative_frequency   = models.FloatField(null=True, blank=True)
    over_relative_frequency    = models.FloatField(null=True, blank=True)
    down_relative_frequency    = models.FloatField(null=True, blank=True)
    your_relative_frequency    = models.FloatField(null=True, blank=True)
    will_relative_frequency    = models.FloatField(null=True, blank=True)
    its_relative_frequency     = models.FloatField(null=True, blank=True)
    any_relative_frequency     = models.FloatField(null=True, blank=True)
    through_relative_frequency = models.FloatField(null=True, blank=True)
    after_relative_frequency   = models.FloatField(null=True, blank=True)
    off_relative_frequency     = models.FloatField(null=True, blank=True)
    than_relative_frequency    = models.FloatField(null=True, blank=True)
    our_relative_frequency     = models.FloatField(null=True, blank=True)
    us_relative_frequency      = models.FloatField(null=True, blank=True)
    around_relative_frequency  = models.FloatField(null=True, blank=True)
    these_relative_frequency   = models.FloatField(null=True, blank=True)
    because_relative_frequency = models.FloatField(null=True, blank=True)
    must_relative_frequency    = models.FloatField(null=True, blank=True)
    before_relative_frequency  = models.FloatField(null=True, blank=True)
    those_relative_frequency   = models.FloatField(null=True, blank=True)
    should_relative_frequency  = models.FloatField(null=True, blank=True)
    himself_relative_frequency = models.FloatField(null=True, blank=True)
    both_relative_frequency    = models.FloatField(null=True, blank=True)
    against_relative_frequency = models.FloatField(null=True, blank=True)
    may_relative_frequency     = models.FloatField(null=True, blank=True)
    might_relative_frequency   = models.FloatField(null=True, blank=True)
    shall_relative_frequency   = models.FloatField(null=True, blank=True)
    since_relative_frequency   = models.FloatField(null=True, blank=True)
    de_relative_frequency      = models.FloatField(null=True, blank=True)
    within_relative_frequency  = models.FloatField(null=True, blank=True)
    between_relative_frequency = models.FloatField(null=True, blank=True)
    each_relative_frequency    = models.FloatField(null=True, blank=True)
    under_relative_frequency   = models.FloatField(null=True, blank=True)
    until_relative_frequency   = models.FloatField(null=True, blank=True)
    toward_relative_frequency  = models.FloatField(null=True, blank=True)
    another_relative_frequency = models.FloatField(null=True, blank=True)
    myself_relative_frequency  = models.FloatField(null=True, blank=True)

    # Part of Speech relative frequencies
    PRP_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    VBG_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    VBD_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    VBN_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    POS_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    VBP_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    WDT_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    JJ_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    WP_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    VBZ_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    DT_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    RP_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    NN_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    FW_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    TO_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    PRP_possessive_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    RB_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    NNS_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    NNP_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    VB_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    WRB_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    CC_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    LS_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    PDT_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    RBS_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    RBR_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    CD_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    EX_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    IN_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    WP_possessive_pos_relative_frequency        = models.FloatField(null=True, blank=True)
    MD_pos_relative_frequency      = models.FloatField(null=True, blank=True)
    NNPS_pos_relative_frequency    = models.FloatField(null=True, blank=True)
    JJS_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    JJR_pos_relative_frequency     = models.FloatField(null=True, blank=True)
    UH_pos_relative_frequency      = models.FloatField(null=True, blank=True)


CLASSIFIER_STATUS_CHOICES = (
    ('untrained', 'untrained'),
    ('trained', 'trained'),
    ('training', 'training'),
)

class Classifier(models.Model):
    last_trained = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=CLASSIFIER_STATUS_CHOICES, default="untrained")

    def __unicode__(self):
        return u"Classifier"

    def train(self):
        self.status = "training"
        chunks = Chunk.objects.all()
        authors = []
        fingerprints = []
        for chunk in chunks:
            authors.append(chunk.author.name)
            fingerprints.append(chunks[0].get_fingerprint())
        clf = classifier.svm.train_svm(fingerprints, authors)
        classifier.svm.store_classifier(clf)
        self.status = "untrained"
