#!/usr/bin/env python
#
# Copyright 2014 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr, gr_unittest, blocks, zeromq
import time

class qa_zeromq_pushpull (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001 (self):
        vlen = 10
        src_data = range(vlen)*100
        src = blocks.vector_source_f(src_data, False, vlen)
        zeromq_push_sink = zeromq.push_sink(gr.sizeof_float, vlen, "tcp://127.0.0.1:5557")
        zeromq_pull_source = zeromq.pull_source(gr.sizeof_float, vlen, "tcp://127.0.0.1:5557", 0)
        sink = blocks.vector_sink_f(vlen)
        self.tb.connect(src, zeromq_push_sink)
        self.tb.connect(zeromq_pull_source, sink)
        self.tb.start()
        time.sleep(0.25)
        self.tb.stop()
        self.tb.wait()
        self.assertFloatTuplesAlmostEqual(sink.data(), src_data)

if __name__ == '__main__':
    gr_unittest.run(qa_zeromq_pushpull)
