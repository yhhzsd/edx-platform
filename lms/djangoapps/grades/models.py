from django.contrib.auth.models import User
from django.db import models

from xmodule_django.models import BlockTypeKeyField, CourseKeyField, UsageKeyField

class Grade(models.Model):
    """
    A django model tracking persistent grades at the subsection level.
    """

    class Meta(object):
        index_together = [
            ['user_id', 'course_id', 'content_type', 'is_valid'],
            ['course_id', 'updated'],
            ['updated'],
        ]

    # TODO: timestamp discussions - do we need all three of [created, updated, subtree_edited_date]?
    created = models.DateTimeField('creation timestamp', auto_now_add=True)
    updated = models.DateTimeField('latest updated timestamp', auto_now=True)
    subtree_edited_date = models.DateTimeField('last content edit timestamp')

    # TODO: is this the right way to store course edit version? make sure it matches up w/ what Nimisha's exposing in her PR
    course_version = models.CharField('guid of latest course version', max_length=255)

    user = models.ForeignKey(User)
    course_id = CourseKeyField(max_length=255)
    content_id = UsageKeyField(max_length=255)
    content_type = models.CharField('used to bucket grades by item type', max_length=255)
    total_weighted_raw_score = models.IntegerField()
    total_weighted_max_score = models.IntegerField()
    is_valid = models.BinaryField()
    visible_blocks = models.ManyToManyField(BlockRecord)  # see TODO below

# TODO - do we actually want this? Latest discussions are leaning towards "no".
class BlockRecord(models.Model):
    """
    A django model used to track the state of a block when used for grade calculation.
    """
    block_type = BlockTypeKeyField(max_length=255)
    block_id = UsageKeyField(max_length=255)
    block_version = models.IntegerField()
