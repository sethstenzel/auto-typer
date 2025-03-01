from auto_typer.classes.data import *

test_texts = [
    "<<ctrl+1>>",
    "The quick<<shift+1>>brown fox <<ctrl+alt+a>>jumped over<<alt+win+f>>the lazy dog.",
    "<<ctrl-f>><<ctrl+1>><<alt.f>><<alt+f1>>",
    "A  cat  <<jumped>>  over  a dog?"
]

def test_text_to_string_tokens():
    correct_texts_string_tokens_lists = [
        ["<<ctrl+1>>"],
        ["The", "<<space>>", "quick", "<<shift+1>>", "brown", "<<space>>", "fox", "<<space>>", "<<ctrl+alt+a>>", "jumped", "<<space>>", "over", "<<alt+win+f>>", "the", "<<space>>", "lazy", "<<space>>", "dog."],
        ["<<ctrl-f>>","<<ctrl+1>>","<<alt.f>>","<<alt+f1>>"],
        ['A', '<<space>>', "<<space>>", 'cat', "<<space>>", "<<space>>", "<<jumped>>", "<<space>>", "<<space>>", "over", "<<space>>", "<<space>>", 'a', "<<space>>", 'dog?']
    ]
    atpt = TextData()
    assert atpt.text_to_string_tokens(test_texts[0]) == correct_texts_string_tokens_lists[0]
    assert atpt.text_to_string_tokens(test_texts[1]) == correct_texts_string_tokens_lists[1]
    assert atpt.text_to_string_tokens(test_texts[2]) == correct_texts_string_tokens_lists[2]
    assert atpt.text_to_string_tokens(test_texts[3]) == correct_texts_string_tokens_lists[3]

def test_parse_token_MultiKeys():
    test_string_tokens = ["<<ctrl+f4>>", "<<ctrl+alt+1>>","<<alt+f4+s+1+space>>", "<<alt+f1+space>>"]
    correct_tokens = [
        MultiKeys(keys=("ctrl", "f4")),
        MultiKeys(keys=("ctrl", "alt", "1")),
        MultiKeys(keys=("alt", "f4", "s", "1", "space")),
        MultiKeys(keys=("alt", "f1", "space")),
    ]
    results = []
    atpt = TextData()
    for string_token in test_string_tokens:
        results.append(atpt.parse_string_token_to_command_token(string_token))   

    assert results[0] == correct_tokens[0]

def test_parse_token_multikeys():
    test_string_tokens = ["<<ctrl+f4>>", "<<ctrl+alt+1>>","<<alt+f4+s+1+space>>", "<<alt+f1+space>>"]
    correct_tokens = [
        MultiKeys(keys=("ctrl", "f4")),
        MultiKeys(keys=("ctrl", "alt", "1")),
        MultiKeys(keys=("alt", "f4", "s", "1", "space")),
        MultiKeys(keys=("alt", "f1", "space")),
    ]
    results = []
    atpt = TextData()
    for string_token in test_string_tokens:
        results.append(atpt.parse_string_token_to_command_token(string_token))   

    assert results[0] == correct_tokens[0]
    assert results[1] == correct_tokens[1]
    assert results[2] == correct_tokens[2]
    assert results[3] == correct_tokens[3]

def test_parse_token_single_key():
    test_string_tokens = ["<<ctrl>>", "<<alt>>","<<space>>", "<<f2>>"]
    correct_tokens = [
        SingleKey(key="ctrl"),
        SingleKey(key="alt"),
        SingleKey(key="space"),
        SingleKey(key="f2"),
    ]
    results = []
    atpt = TextData()
    for string_token in test_string_tokens:
        results.append(atpt.parse_string_token_to_command_token(string_token))   

    assert results[0] == correct_tokens[0]
    assert results[1] == correct_tokens[1]
    assert results[2] == correct_tokens[2]
    assert results[3] == correct_tokens[3]

def test_parse_token_timed_pause():
    test_string_tokens = ["<<pause=2>>", "<<pause=5>>", "<<pause=0>>"]
    correct_tokens = [
        TimedPause(time=2),
        TimedPause(time=5),
        TimedPause(time=0),
    ]
    results = []
    atpt = TextData()
    for string_token in test_string_tokens:
        results.append(atpt.parse_string_token_to_command_token(string_token))   

    assert results[0] == correct_tokens[0]
    assert results[1] == correct_tokens[1]
    assert results[2] == correct_tokens[2]

def test_parse_token_scrollup_scrolldown():
    test_string_tokens = [
        "<<scrollup=2>>",
        "<<scrollup=5>>",
        "<<scrolldown=1>>",
        "<<scrolldown=30>>",
    ]
    correct_tokens = [
        MouseScroll(scroll_count=2, scroll_direction=0),
        MouseScroll(scroll_count=5, scroll_direction=0),
        MouseScroll(scroll_count=1, scroll_direction=1),
        MouseScroll(scroll_count=30, scroll_direction=1),
    ]
    results = []
    atpt = TextData()
    for string_token in test_string_tokens:
        results.append(atpt.parse_string_token_to_command_token(string_token)) 
    
    assert results[0] == correct_tokens[0]
    assert results[1] == correct_tokens[1]
    assert results[2] == correct_tokens[2]
    assert results[3] == correct_tokens[3]

def test_parse_text_to_tokens():
    test_string = "The quick<<shift+1>>brown <<pause=12>>fox <<f4>>jumped over<<alt+win+f>>the lazy dog.<<scrollup=1>>"
    correct_tokens = [
        "The",
        SingleKey(key="space"),
        "quick",
        MultiKeys(keys=("shift","1")),
        "brown",
        SingleKey(key="space"),
        TimedPause(time=12),
        "fox",
        SingleKey(key="space"),
        SingleKey(key="f4"),
        "jumped",
        SingleKey(key="space"),
        "over",
        MultiKeys(keys=("alt","win","f")),
        "the",
        SingleKey(key="space"),
        "lazy",
        SingleKey(key="space"),
        "dog.",
        MouseScroll(scroll_count=1, scroll_direction=0),
    ]
    atpt = TextData(text_to_type=test_string)    
    assert atpt.text_tokens == correct_tokens