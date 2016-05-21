from django.db import models

import classifier.constants
from classifier import svm, compute_fingerprint, chunk
from classifier.util import generate_directory_name, get_interesting_fields
from celery import chord

class Author(models.Model):
    name = models.CharField(max_length=200)
    average_chunk = models.ForeignKey('Chunk', related_name='average_chunk_author', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s' % (self.name)

    def compute_own_average_chunk(self):
        from tasks import create_average_chunk
        create_average_chunk(self.id, type(self))

def create_text_upload_path(text, filename):
    author_name = generate_directory_name(text.author.name)
    text_name = generate_directory_name(text.name)
    path = classifier.constants.PLAINTEXT_PATH + "/".join([author_name, text_name])
    return path

class Text(models.Model):
    author = models.ForeignKey('Author')
    name = models.CharField(max_length=200)
    text_file = models.FileField(upload_to=create_text_upload_path, default=None, null=True, blank=True)
    average_chunk = models.ForeignKey('Chunk', related_name='average_chunk_text', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        is_new_chunk = False
        if not self.pk:
            is_new_chunk = True

        super(Text, self).save(*args, **kwargs)
        if not is_new_chunk:
            return

        from tasks import add_chunk, create_average_chunk
        print "Chunking text..."
        chunk_number = 0
        chunk_tasks = []
        for chunk_text in chunk.chunk_text(self.text_file.path):
            chunk_task = add_chunk.s(author_id=self.author.id, text_id=self.id, text_chunk_number=chunk_number, chunk_text=chunk_text)
            chunk_tasks.append(chunk_task)
            chunk_number+=1

        average_task = create_average_chunk.si(self.id, type(self))
        chunk_chord_res = chord(chunk_tasks)(average_task)
        chunk_chord_res.get()

        system_classifier = Classifier.objects.first()
        system_classifier.status = "untrained"
        system_classifier.save()
        print "Processed the text"

    def compute_own_average_chunk(self):
        from tasks import create_average_chunk
        create_average_chunk(self.id, type(self))

class Chunk(models.Model):
    author = models.ForeignKey('Author', null=True, blank=True)
    text = models.ForeignKey('Text', null=True, blank=True)
    text_chunk_number = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        if (self.text_chunk_number != None):
            return u'%s - %s (%s)' % (self.text, self.author, self.text_chunk_number)
        elif (self.text != None):
            return u'%s - average' % (self.text)
        elif (self.author != None):
            return u'%s - average' % (self.author)
        return u''

    def get_fingerprint_dict(self):
        return {field_name: getattr(self, field_name) for field_name in classifier.constants.CHUNK_MODEL_FINGERPRINT_FIELDS }

    def get_fingerprint_list(self):
        return [getattr(self, field_name) for field_name in classifier.constants.CHUNK_MODEL_FINGERPRINT_FIELDS]

    @classmethod
    def get_chunks(cls):
        return Chunk.objects.all().exclude(text_chunk_number__isnull=True)

    @classmethod
    def get_average_fingerprint_of_chunks(cls, chunks):
        chunks_length = len(chunks)
        if chunks_length == 0: return None

        average_chunk_fingerprint = {key: 0 for key in classifier.constants.CHUNK_MODEL_FINGERPRINT_FIELDS}

        for chunk in chunks:
            chunk_fingerprint_dict = chunk.get_fingerprint_dict()
            for key, value in chunk_fingerprint_dict.items():
                average_chunk_fingerprint[key]+=value

        for key, value in average_chunk_fingerprint.items():
            average_chunk_fingerprint[key]=float(value)/chunks_length

        return average_chunk_fingerprint

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

def add_pos_groups(fingerprint_dict):
    pos_category_dict = {key: 0 for key in classifier.constants.POS_TAG_CATEGORIES.keys()}
    fingerprint_dict.update(pos_category_dict)
    for pos_category, pos_list in classifier.constants.POS_TAG_CATEGORIES.items():
        for field_name in pos_list:
            fingerprint_dict[pos_category]+=fingerprint_dict[field_name]
    return fingerprint_dict

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
        classifier_id = self.id
        from tasks import train_classifier
        train_classifier.delay()

    def classify(self, input_text):
        result = {}

        fingerprint = compute_fingerprint.fingerprint_text(input_text)
        clf = svm.load_classifier()
        author_results = svm.classify_single_fingerprint(fingerprint, clf)
        for author_result in author_results:
            author = Author.objects.get(name=author_result['label'])
            if author.average_chunk:
                author_average_fingerprint = author.average_chunk.get_fingerprint_dict()
                author_average_fingerprint = add_pos_groups(author_average_fingerprint)
                author_result['fingerprint'] = get_interesting_fields(author_average_fingerprint)

        result['fingerprint'] = get_interesting_fields(add_pos_groups(fingerprint))
        result['input'] = input_text
        result['authors'] = author_results
        return result
