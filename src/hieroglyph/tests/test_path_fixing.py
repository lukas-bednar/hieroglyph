import os.path
import re
from unittest import TestCase

from docutils import nodes

from hieroglyph.tests.util import (
    TestApp,
    make_document,
)

from hieroglyph.builder import SlideBuilder


class PostProcessImageTests(TestCase):

    def setUp(self):

        self.app = TestApp(buildername='slides')
        self.builder = SlideBuilder(self.app)
        self.document = make_document(
            'testing',
            """\
Title
-----

.. image:: %s/_static/image.png

""" % (self.builder.outdir,),
        )

        self.image_node = self.document.traverse(nodes.image)[0]
        self.image_node.attributes['candidates'] = {
            '*': None,
        }

    def test_absolute_paths_made_relative(self):

        self.assertEqual(
            self.image_node['uri'],
            '%s/_static/image.png' % (self.builder.outdir,),
        )

        self.document.attributes['source'] = '%s/index.rst' % (self.builder.srcdir,)
        self.builder.post_process_images(self.document)

        self.assertEqual(
            self.image_node['uri'],
            '_static/image.png',
        )

    def test_absolute_paths_subdir_made_relative(self):

        self.assertEqual(
            self.image_node['uri'],
            '%s/_static/image.png' % (self.builder.outdir,),
        )

        self.document.attributes['source'] = '%s/sub/dir/index.rst' % (
            self.builder.srcdir,
        )
        self.builder.post_process_images(self.document)

        self.assertEqual(
            self.image_node['uri'],
            '../../_static/image.png',
        )
