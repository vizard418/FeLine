#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# test_argparser.py
import pytest
from lib.argparser import Argparser
from lib.models import Models

# Fixture to provide an Argparser instance for each test
@pytest.fixture
def parser():
    return Argparser()


def test_argparser_default_values(parser):
    # Test 1: Check critical default values using the imported Models data
    args = parser.parse_args([])
    assert args.message == ''
    assert args.interactive is False
    assert args.model == Models.default
    assert args.role == ''


def test_argparser_positional_message(parser):
    # Test 2: Check handling of the positional message argument
    test_msg = 'Test message for the AI'
    args = parser.parse_args([test_msg])
    assert args.message == test_msg


def test_argparser_model_and_role_options(parser):
    # Test 3: Check two key optional arguments: model and role
    # Use one of the available models (e.g., the second key)
    test_model = list(Models.availables.keys())[1]  # 'gemini-flash'
    test_role = 'Custom Role'
    args = parser.parse_args(['-m', test_model, '--role', test_role])
    assert args.model == test_model
    assert args.role == test_role


def test_argparser_boolean_flags(parser):
    # Test 4: Check boolean flags using their short forms (-i and -v)
    args = parser.parse_args(['-i', '-v'])
    assert args.interactive is True
    assert args.verbose is True
    assert args.clear is False  # Ensure non-passed flags are False


def test_argparser_model_invalid_choice(parser):
    # Test 5: Ensure model choice validation is working (raises SystemExit)
    with pytest.raises(SystemExit):
        parser.parse_args(['--model', 'invalid-model'])
