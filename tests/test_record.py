from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

# Make Py2's str equivalent to Py3's
str = type('')

import io
import os
import time
import tempfile
import picamera
import pytest


# Run tests with a variety of file suffixes and expected formats
@pytest.fixture(scope='module', params=(
    (),
    (('profile', 'baseline'),),
    (('profile', 'main'),),
    (('profile', 'high'),),
    (('profile', 'constrained'),),
    (('bitrate', 0), ('quantization', 10)),
    (('bitrate', 0), ('quantization', 20)),
    (('bitrate', 0), ('quantization', 30)),
    (('bitrate', 0), ('quantization', 40)),
    (('bitrate', 10000000), ('intra_period', 10)),
    (('bitrate', 10000000), ('inline_headers', True)),
    (('bitrate', 15000000),),
    (('bitrate', 20000000), ('profile', 'main')),
    ))
def h264_options(request):
    return dict(request.param)


# TODO We don't yet test that the recordings are actually valid in any way, so
# at the moment this is little more than making sure exceptions don't occur

def test_record_to_file(camera, previewing, resolution, h264_options):
    if resolution == (2592, 1944):
        pytest.xfail('Cannot encode video at max resolution')
    filename = tempfile.mkstemp(suffix='.h264')[1]
    try:
        camera.start_recording(filename, **h264_options)
        try:
            camera.wait_recording(1)
        finally:
            camera.stop_recording()
        # TODO verify the stream
    finally:
        os.unlink(filename)

def test_capture_to_stream(camera, previewing, resolution, h264_options):
    if resolution == (2592, 1944):
        pytest.xfail('Cannot encode video at max resolution')
    stream = io.BytesIO()
    camera.start_recording(stream, 'h264', **h264_options)
    try:
        camera.wait_recording(1)
    finally:
        camera.stop_recording()
    stream.seek(0)
    # TODO verify the stream

