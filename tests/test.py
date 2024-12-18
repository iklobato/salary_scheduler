from datetime import datetime
from unittest.mock import patch
from app import (
    get_next_months,
    create_month_mapping,
    create_replace_request,
    process_text_element,
    parse_arguments
)

def test_get_next_months():
    current, next_month, following = get_next_months()
    assert isinstance(current, datetime)
    assert isinstance(next_month, datetime)
    assert isinstance(following, datetime)
    assert next_month.month == (current.month % 12 + 1)
    assert following.month == (next_month.month % 12 + 1)

def test_create_month_mapping():
    test_current = datetime(2024, 1, 1)
    test_next = datetime(2024, 2, 1)
    test_following = datetime(2024, 3, 1)
    
    mapping = create_month_mapping(test_current, test_next, test_following)
    
    assert mapping['January'] == 'February'
    assert mapping['February'] == 'March'
    assert mapping['Jan'] == 'Feb'
    assert mapping['Feb'] == 'Mar'

def test_create_replace_request():
    request = create_replace_request('old', 'new')
    
    assert request['replaceAllText']['containsText']['text'] == 'old'
    assert request['replaceAllText']['replaceText'] == 'new'
    assert request['replaceAllText']['containsText']['matchCase'] is True

def test_process_text_element():
    text = "January February"
    replacements = {'January': 'February', 'February': 'March'}
    
    requests = process_text_element(text, replacements)
    
    assert len(requests) == 2
    assert requests[0]['replaceAllText']['containsText']['text'] == 'January'
    assert requests[1]['replaceAllText']['containsText']['text'] == 'February'

def test_parse_arguments():
    with patch('sys.argv', ['script.py', '--doc-id', 'test123', '--run-once']):
        args = parse_arguments()
        
        assert args.doc_id == 'test123'
        assert args.run_once is True
        assert args.schedule_day == 15
        assert args.schedule_time == '00:00'

