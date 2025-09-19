#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.argparser import ArgParser
from lib.models import Models

def test_default_args():
    parser = ArgParser()
    args = parser.parse_args([])

    assert args.message == '', f'Expected empty string, but got {args.message}'
    assert args.interactive == False, f'Expected "False" but got {args.interactive}'
    assert args.clear == False, f'Expected "False" but got {args.clear}'
    assert args.model == Models.default, f'Expected {Models.default} but got {args.model}'
