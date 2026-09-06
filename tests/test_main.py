#Pytest for the main.py file
#06-09-2026 Manjunathan S - Started to write Pytest for the each functions
import pytest
import src.main as program
from unittest.mock import patch

def test_constants_file():
    #This function tests the Config file and Validates the email fields
    email_fields = program.read_constants_file()
    assert email_fields == {'sender_address': 'nathanm6716@gmail.com', \
                            'receiver_address': 'manjunathsg407@gmail.com', \
                            'subject': 'Computer Boot Up Activity Detected', \
                            'smtp_addr': 'smtp.gmail.com', 'imap_addr': 'imap.gmail.com'}

@patch('src.main.configparser')  
def test_constants_fike_negative_scenario(mocked_configparser):
    #This function tests the negative scenario of 
    mocked_configparser.ConfigParser.return_value.read.side_effect = FileNotFoundError
    with pytest.raises(SystemExit) as err_info:
        program.read_constants_file()
        assert err_info.value == "Something went wrong"
        assert err_info.value.code == 1

@pytest.fixture()
def constants_file_data_dictionary():
    #Defined a ficture to test sender and receiver domain_data
    fixture_dictionary = {'sender_address' : "smtp@test_gmail_domain.com", 
                          'receiver_address' : "imap@test_gmail_domain.com",
                          "subject": "Computer Boot Up Activity Detected"}
    yield fixture_dictionary

@patch('src.main.sys')
def test_email_setup(patch_sys, constants_file_data_dictionary):
    #This function will test the email setup configs
    patch_sys.platform = 'Linux'

    with patch.object(program, 'constant_file_data',constants_file_data_dictionary, create = True):
        program.setup_email()
        assert program.msg['Subject'] == constants_file_data_dictionary['subject']
        assert program.msg['From'] == constants_file_data_dictionary['sender_address']
        assert program.msg['To'] == constants_file_data_dictionary['receiver_address']

        body = program.msg.get_content()
        assert 'Linux' in body


        
